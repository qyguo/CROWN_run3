#ifndef GUARD_REWEIGHTING_H
#define GUARD_REWEIGHTING_H

#include "../include/basefunctions.hxx"
#include "../include/utility/Logger.hxx"
#include "../include/utility/RooFunctorThreadsafe.hxx"
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TFile.h"
#include "TH1.h"
#include "correction.h"
#include <Math/Vector4D.h>
#include <algorithm>
#include <cmath>
#include <stdexcept>

/// namespace used for reweighting related functions
namespace reweighting {
bool hasColumn(ROOT::RDF::RNode df, const std::string &column) {
    const auto columns = df.GetColumnNames();
    return std::find(columns.begin(), columns.end(), column) != columns.end();
}

/**
 * @brief Function used to read out pileup weights
 *
 * @param df The input dataframe
 * @param weightname name of the derived weight
 * @param truePUMean name of the column containing the true PU mean of simulated
 * events
 * @param filename path to the rootfile
 * @param histogramname name of the histogram stored in the rootfile
 * @return a new dataframe containing the new column
 */
ROOT::RDF::RNode puweights(ROOT::RDF::RNode df, const std::string &weightname,
                           const std::string &truePUMean,
                           const std::string &filename,
                           const std::string &histogramname) {

    float bin_density = 1.0;
    std::vector<float> puweights;
    Logger::get("puweights")
        ->debug("Loading pile-up weights from {}", filename);
    {
        TFile inputfile(filename.c_str(), "READ");
        TH1D *puhist = (TH1D *)inputfile.Get(histogramname.c_str());
        for (int i = 0; i <= puhist->GetNbinsX(); ++i) {
            puweights.push_back(puhist->GetBinContent(i));
        }
        bin_density = 1.0 / puhist->GetBinWidth(1);
        delete puhist;
        inputfile.Close();
    }

    auto puweightlambda = [bin_density, puweights](const float pu) {
        size_t puBin = static_cast<size_t>(pu * bin_density);
        return puBin < puweights.size() ? puweights[puBin] : 1.0;
    };
    auto df1 = df.Define(weightname, puweightlambda, {truePUMean});
    return df1;
}

/**
 * @brief Function used to read out pileup weights from JSON files
 *
 * @param df The input dataframe
 * @param weightname name of the derived weight
 * @param truePU name of the column containing the true PU of simulated
 * events
 * @param filename path to the JSON file
 * @param eraname name of the era specified in the JSON file
 * @param variation systematic variations: nominal, up, down
 */
ROOT::RDF::RNode puweights(ROOT::RDF::RNode df, const std::string &weightname,
                           const std::string &truePU,
                           const std::string &filename,
                           const std::string &eraname,
                           const std::string &variation) {
    auto evaluator =
        correction::CorrectionSet::from_file(filename)->at(eraname);
    auto df1 =
        df.Define(weightname,
                  [evaluator, variation](const float &pu) {
                      double weight = evaluator->evaluate({pu, variation});
                      return weight;
                  },
                  {truePU});
    return df1;
}

/**
 * @brief Function used to calculate top pt reweighting
 *
 * @param df The input dataframe
 * @param weightname name of the derived weight
 * @param gen_pdgids name of the column containing the PDG-IDs of the generator
 * particles
 * @param gen_status name of the column containing the status flags of the
 * generator particles, where bit 13 contains the isLastCopy flag
 * @param gen_pt name of the column containing the pt of the generator particles
 * @return a new dataframe containing the new column
 */
ROOT::RDF::RNode topptreweighting(ROOT::RDF::RNode df,
                                  const std::string &weightname,
                                  const std::string &gen_pdgids,
                                  const std::string &gen_status,
                                  const std::string &gen_pt) {

    auto ttbarreweightlambda = [](const ROOT::RVec<int> pdgid,
                                  const ROOT::RVec<int> status,
                                  const ROOT::RVec<float> pt) {
        std::vector<float> top_pts;
        for (size_t i = 0; i < pdgid.size(); i++) {
            if (std::abs(pdgid[i]) == 6 && ((status[i] >> 13) & 1) == 1)
                top_pts.push_back(pt[i]);
        }
        if (top_pts.size() != 2) {
            std::cout << top_pts.size();
            Logger::get("topptreweighting")
                ->error("TTbar reweighting applied to event with not exactly "
                        "two top quarks. Probably due to wrong sample type.");
            throw std::runtime_error("Bad number of top quarks.");
        }
        if (top_pts[0] > 472.0)
            top_pts[0] = 472.0;
        if (top_pts[1] > 472.0)
            top_pts[1] = 472.0;
        const float parameter_a = 0.088;
        const float parameter_b = -0.00087;
        const float parameter_c = 0.00000092;
        return sqrt(exp(parameter_a + parameter_b * top_pts[0] +
                        parameter_c * top_pts[0] * top_pts[0]) *
                    exp(parameter_a + parameter_b * top_pts[1] +
                        parameter_c * top_pts[1] * top_pts[1]));
    };
    auto df1 = df.Define(weightname, ttbarreweightlambda,
                         {gen_pdgids, gen_status, gen_pt});
    return df1;
}

/**
 * @brief Function used to evaluate Z pt mass weights
 *
 * @param df The input dataframe
 * @param weightname name of the generated weight
 * @param gen_boson name of the column that contains a pair of Lorentzvectors,
 * where the first one is the one of the genboson
 * @param workspace_file path to the file which contains the workspace to be
 * read
 * @param functor_name name of the function from the workspace
 * @param argset arguments of the function
 * @return a new dataframe containing the new column
 */
ROOT::RDF::RNode zPtMassReweighting(ROOT::RDF::RNode df,
                                    const std::string &weightname,
                                    const std::string &gen_boson,
                                    const std::string &workspace_file,
                                    const std::string &functor_name,
                                    const std::string &argset) {

    // retrieve pt and mass of gen boson reconstructed with the method used by
    // recoil corrections; resulting quantities are only for the purpose of this
    // method
    auto df1 = df.Define(gen_boson + "_pt",
                         [](const std::pair<ROOT::Math::PtEtaPhiMVector,
                                            ROOT::Math::PtEtaPhiMVector> &p4) {
                             return (float)p4.first.pt();
                         },
                         {gen_boson});
    auto df2 = df1.Define(gen_boson + "_mass",
                          [](const std::pair<ROOT::Math::PtEtaPhiMVector,
                                             ROOT::Math::PtEtaPhiMVector> &p4) {
                              return (float)p4.first.mass();
                          },
                          {gen_boson});

    // set up workspace
    Logger::get("zPtMassReweighting")
        ->debug("Setting up functions for zPtMassReweighting");
    Logger::get("zPtMassReweighting")
        ->debug("zPtMassReweighting - Function {} // argset {}", functor_name,
                argset);

    const std::shared_ptr<RooFunctorThreadsafe> weight_function =
        loadFunctor(workspace_file, functor_name, argset);
    auto df3 = basefunctions::evaluateWorkspaceFunction(
        df2, weightname, weight_function, gen_boson + "_mass",
        gen_boson + "_pt");
    return df3;
}
/**
 * @brief This function is used to evaluate the parton shower (PS) weight of an event. 
 * The weights are stored in the nanoAOD files and defined as 
 * \f$w_{variation}\f$ / \f$w_{nominal}\f$. The nominal weight is already applied, 
 * therefore, the main use of this function is to get the initial state radiation (ISR) 
 * and final state radiation (FSR) variations to the nominal PS weight.
 *
 * Depending on the selected ISR and FSR value, a specific index has to be identified. 
 * The mapping between the index and the ISR and FSR values is:
 *  ISR       | FSR        | index
 * -----------|------------|---------
 *  2.0       | 1.0        | 0
 *  1.0       | 2.0        | 1
 *  0.5       | 1.0        | 2
 *  1.0       | 0.5        | 3
 *
 * @note For some simulated samples this mapping might be defined differently, 
 * therefore, it is advisable to check the documentation of the `PSWeight` 
 * branch in the nanoAOD files of the samples if issues occur.
 *
 * @param df input dataframe
 * @param outputname name of the output column containing the ISR/FSR event weight
 * @param ps_weights name of the column containing the parton shower (ISR/FSR) weights
 * @param isr value of the ISR variation, possible values are 0.5, 1.0, 2.0
 * @param fsr value of the FSR variation, possible values are 0.5, 1.0, 2.0
 *
 * @return a new dataframe containing the new column
 */
ROOT::RDF::RNode PartonShower(ROOT::RDF::RNode df,
                            const std::string &outputname,
                            const std::string &ps_weights,
                            const float isr, const float fsr) {
    // find the index we have to use, first check if the isr and fsr values are
    // valid, only 0.5, 1.0, 2.0 are allowed
    std::vector<float> allowed_values = {0.5, 1.0, 2.0};
    if (std::find(allowed_values.begin(), allowed_values.end(), isr) ==
        allowed_values.end()) {
        Logger::get("event::reweighting::PartonShower")
            ->error("Invalid value for isr: {}", isr);
        throw std::runtime_error("Invalid value for isr");
    }
    if (std::find(allowed_values.begin(), allowed_values.end(), fsr) ==
        allowed_values.end()) {
        Logger::get("event::reweighting::PartonShower")
            ->error("Invalid value for fsr: {}", fsr);
        throw std::runtime_error("Invalid value for fsr");
    }
    
    auto ps_weights_lambda =
        [isr, fsr](const ROOT::RVec<float> ps_weights) {
            if (isr == 1.0 && fsr == 1.0) {
                // if the ISR and FSR are both 1.0, we return the nominal weight
                return (float)1.0;
            }
            // now find the index
            std::map<std::pair<const float, const float>, int> index_map;
            if (ps_weights.size() == 4) {
                index_map = {
                    {{2.0, 1.0}, 0}, {{1.0, 2.0}, 1}, 
                    {{0.5, 1.0}, 2}, {{1.0, 0.5}, 3}
                };
            } else {
                Logger::get("event::reweighting::PartonShower")
                    ->error("Invalid number of PS weights: {}",
                            ps_weights.size());
                throw std::runtime_error("Invalid number of PS weights");
            }
            std::pair<const float, const float> variations = {isr, fsr};
            int index = index_map[variations];
            return ps_weights.at(index);
        };
    auto df1 =
        df.Define(outputname, ps_weights_lambda, {ps_weights});
    return df1;
}
/**
 * @brief This function is used to evaluate the LHE scale weight of an event. The weights
 * are stored in the nanoAOD files and defined as \f$w_{variation}\f$ / \f$w_{nominal}\f$. 
 * The nominal weight is already applied, therefore, the main use of this function is 
 * to get the factorization and renormalization scale variations to the nominal scale 
 * weight.
 *
 * Depending on the selected \f$\mu_R\f$ and \f$\mu_F\f$ value, a specific index has 
 * to be identified. The mapping between the index and the \f$\mu_R\f$ and \f$\mu_F\f$ 
 * values is:
 *  mu_f       | mu_r        | index
 * ------------|-------------|---------
 *  0.5        | 0.5         | 0
 *  1.0        | 0.5         | 1
 *  2.0        | 0.5         | 2
 *  0.5        | 1.0         | 3
 *  1.0        | 1.0         | 4 (not always included)
 *  2.0        | 1.0         | 5 (4)
 *  0.5        | 2.0         | 6 (5)
 *  1.0        | 2.0         | 7 (6)
 *  2.0        | 2.0         | 8 (7)
 *
 * @note For some simulated samples this mapping might be defined differently, 
 * therefore, it is advisable to check the documentation of the `LHEScaleWeight` 
 * branch in the nanoAOD files of the samples if issues occur.
 *
 * @param df input dataframe
 * @param outputname name of the output column containing the LHE scale event weight
 * @param lhe_scale_weights name of the column containing the LHE scale weights
 * @param mu_r value of \f$\mu_R\f$ variation, possible values are 0.5, 1.0, 2.0
 * @param mu_f value of \f$\mu_F\f$ variation, possible values are 0.5, 1.0, 2.0
 *
 * @return a new dataframe containing the new column
 */
ROOT::RDF::RNode LHEscale(ROOT::RDF::RNode df,
                            const std::string &outputname,
                            const std::string &lhe_scale_weights,
                            const std::string &variation) {
    
    auto lhe_scale_weights_lambda =
        [variation](const ROOT::RVec<float> scale_weights) {
            // now find the index
            constexpr int idx[7] = {0, 1, 3, 4, 6, 7};
            if (variation == "up") {
                float maxv = 1.0f;
                for (int i = 0; i < 6; ++i) {
                    maxv = std::max(maxv, scale_weights[idx[i]]);
                }
                return maxv;
            }
            else if (variation == "down") {
                float minv = 1.0f;
                for (int i = 0; i < 6; ++i) {
                    minv = std::min(minv, scale_weights[idx[i]]);
                }
                return minv;
            } else {
                Logger::get("event::reweighting::LHEscale")
                    ->error("Invalid variation: {}", variation);
                throw std::runtime_error("Invalid variation for LHE scale weights");
            }
        };
    auto df1 =
        df.Define(outputname, lhe_scale_weights_lambda, {lhe_scale_weights});
    return df1;
}

/**
 * @brief This function is used to evaluate the LHE PDF weight of an event. The weights
 * are stored in the nanoAOD files and defined as \f$w_{variation}\f$ / \f$w_{nominal}\f$. 
 * The nominal weight is already applied, therefore, the main use of this function is 
 * to get the variation of the PDF weights to the nominal PDF weight.
 *
 * The PDF weights consist of 101 weights, where the first weight is the nominal weight 
 * and the remaining 100 weights correspond to alternative PDF sets. 
 *
 * @note The proper procedure is to use each alternative PDF set as an independent 
 * systematic vatiation. However, in case of this function, a simplified approach is used 
 * to calculate a single PDF weight variation. The standard deviation of the 100 
 * alternative PDF weights is calculated and used to define the up and down variations as 
 * follows: \f$w_{up/down} = 1 \pm \sqrt{\sum_{i=1}^{100} (w_i - 1)^2}\f$
 *
 * @param df input dataframe
 * @param outputname name of the output column containing the LHE PDF event weight
 * @param lhe_pdf_weights name of the column containing the LHE PDF weights
 * @param variation name of the variation that should be evaluated, possible values 
 * are "nominal", "up", "down"
 *
 * @return a new dataframe containing the new column
 */
ROOT::RDF::RNode LHEpdf(ROOT::RDF::RNode df,
                        const std::string &outputname,
                        const std::string &lhe_pdf_weights,
                        const std::string &variation) {
    auto lhe_pdf_weights_lambda =
        [variation](const ROOT::RVec<float> pdf_weights) {
            // the nominal weight is already applied, so we can return 1.0
            if (variation == "nominal") {
                return (float)1.0;
            }
            const int n_pdfs = pdf_weights.size();
            if (n_pdfs == 101 || n_pdfs == 103) {
                float sum = 0.0;
                for (size_t i = 1; i < n_pdfs; i++) {
                    float diff = pdf_weights[i] - 1;
                    sum += diff * diff;        
                }
                if (variation == "up") {
                    return (float)(1.0 + std::sqrt(sum));
                } else if (variation == "down") {
                    return (float)(1.0 - std::sqrt(sum));
                } else {
                    Logger::get("event::reweighting::LHEpdf")
                        ->error("Invalid variation: {}", variation);
                    throw std::runtime_error("Invalid variation for LHE PDF weights");
                }
            } else {
                Logger::get("event::reweighting::LHEpdf")
                    ->error("Invalid number of LHE PDF weights: {}",
                            n_pdfs);
                throw std::runtime_error("Invalid number of LHE PDF weights");
            }
        };

    auto df1 =
        df.Define(outputname, lhe_pdf_weights_lambda, {lhe_pdf_weights});
    return df1;
}

ROOT::RDF::RNode LHEpdfUncertainty(ROOT::RDF::RNode df,
                                   const std::string &outputname,
                                   const std::string &lhe_pdf_weights) {
    if (!hasColumn(df, lhe_pdf_weights)) {
        Logger::get("event::reweighting::LHEpdfUncertainty")
            ->warn("Column {} is missing, setting {} to 0",
                   lhe_pdf_weights, outputname);
        return df.Define(outputname, []() { return 0.0f; });
    }

    auto lhe_pdf_uncertainty_lambda = [](const ROOT::RVec<float> pdf_weights) {
        const int n_pdfs = pdf_weights.size();
        if (n_pdfs != 101 && n_pdfs != 103) {
            Logger::get("event::reweighting::LHEpdfUncertainty")
                ->error("Invalid number of LHE PDF weights: {}", n_pdfs);
            throw std::runtime_error("Invalid number of LHE PDF weights");
        }

        float sum = 0.0f;
        for (int i = 1; i <= 100; ++i) {
            const float diff = pdf_weights[i] - 1.0f;
            sum += diff * diff;
        }
        return std::sqrt(sum);
    };

    auto df1 =
        df.Define(outputname, lhe_pdf_uncertainty_lambda, {lhe_pdf_weights});
    return df1;
}

ROOT::RDF::RNode LHEalphaSUncertainty(ROOT::RDF::RNode df,
                                      const std::string &outputname,
                                      const std::string &lhe_pdf_weights) {
    if (!hasColumn(df, lhe_pdf_weights)) {
        Logger::get("event::reweighting::LHEalphaSUncertainty")
            ->warn("Column {} is missing, setting {} to 0",
                   lhe_pdf_weights, outputname);
        return df.Define(outputname, []() { return 0.0f; });
    }

    auto lhe_alpha_s_uncertainty_lambda = [](const ROOT::RVec<float> pdf_weights) {
        const int n_pdfs = pdf_weights.size();
        if (n_pdfs == 101) {
            return 0.0f;
        }
        if (n_pdfs != 103) {
            Logger::get("event::reweighting::LHEalphaSUncertainty")
                ->error("Invalid number of LHE PDF weights: {}", n_pdfs);
            throw std::runtime_error("Invalid number of LHE PDF weights");
        }
        return 0.5f * std::abs(pdf_weights[102] - pdf_weights[101]);
    };

    auto df1 =
        df.Define(outputname, lhe_alpha_s_uncertainty_lambda, {lhe_pdf_weights});
    return df1;
}

ROOT::RDF::RNode LHEscaleEnvelope(ROOT::RDF::RNode df,
                                  const std::string &output_up,
                                  const std::string &output_down,
                                  const std::string &lhe_scale_weights) {
    if (!hasColumn(df, lhe_scale_weights)) {
        Logger::get("event::reweighting::LHEscaleEnvelope")
            ->warn("Column {} is missing, setting {} and {} to 1",
                   lhe_scale_weights, output_up, output_down);
        auto df1 = df.Define(output_up, []() { return 1.0f; });
        auto df2 = df1.Define(output_down, []() { return 1.0f; });
        return df2;
    }

    auto scale_unc_up_lambda = [](const ROOT::RVec<float> scale_weights) {
        constexpr int scale_indices[] = {0, 1, 3, 4, 6, 7};
        if (scale_weights.size() <= scale_indices[5]) {
            Logger::get("event::reweighting::LHEscaleEnvelope")
                ->error("Invalid number of LHE scale weights: {}",
                        scale_weights.size());
            throw std::runtime_error("Invalid number of LHE scale weights");
        }

        float maxv = 1.0f;
        for (int index : scale_indices) {
            maxv = std::max(maxv, scale_weights[index]);
        }
        return maxv;
    };

    auto scale_unc_down_lambda = [](const ROOT::RVec<float> scale_weights) {
        constexpr int scale_indices[] = {0, 1, 3, 4, 6, 7};
        if (scale_weights.size() <= scale_indices[5]) {
            Logger::get("event::reweighting::LHEscaleEnvelope")
                ->error("Invalid number of LHE scale weights: {}",
                        scale_weights.size());
            throw std::runtime_error("Invalid number of LHE scale weights");
        }

        float minv = 1.0f;
        for (int index : scale_indices) {
            minv = std::min(minv, scale_weights[index]);
        }
        return minv;
    };

    auto df1 = df.Define(output_up, scale_unc_up_lambda, {lhe_scale_weights});
    auto df2 = df1.Define(output_down, scale_unc_down_lambda, {lhe_scale_weights});
    return df2;
}
} // namespace reweighting
#endif /* GUARD_REWEIGHTING_H */
