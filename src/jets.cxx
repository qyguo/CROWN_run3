#ifndef GUARDJETS_H
#define GUARDJETS_H

#include "../include/basefunctions.hxx"
#include "../include/defaults.hxx"
#include "../include/utility/Logger.hxx"
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TRandom3.h"
#include "correction.h"
#include <Math/Vector3D.h>
#include <Math/Vector4D.h>
#include <Math/VectorUtil.h>
#include <cmath>
#include <typeinfo>

namespace jet {

/// write by mingtao
///function to calculate the dijet mass and delta eta

ROOT::RDF::RNode 
Calculate_JetMass(ROOT::RDF::RNode df, const std::string &outputname,
                                 const std::string &particle_pts,
                                 const std::string &particle_etas,
                                 const std::string &particle_phis,
                                 const std::string &particle_masses,
                                 const std::string &goodjets_index) {
    auto mass_calculation = [](const ROOT::RVec<float> &particle_pts,
                               const ROOT::RVec<float> &particle_etas,
                               const ROOT::RVec<float> &particle_phis,
                               const ROOT::RVec<float> &particle_masses,
                               const ROOT::RVec<int> &goodjets_index) {
                                 std::vector<ROOT::Math::PtEtaPhiMVector> p4;
                                 for (unsigned int k = 0; k < 2; ++k) {
                                    try {
                                        p4.push_back(ROOT::Math::PtEtaPhiMVector(particle_pts.at(goodjets_index[k]), 
                                                                         particle_etas.at(goodjets_index[k]),
                                                                         particle_phis.at(goodjets_index[k]),
                                                                         particle_masses.at(goodjets_index[k])));
                                    } catch (const std::out_of_range &e) {
                                        p4.push_back(ROOT::Math::PtEtaPhiMVector(default_float, default_float,default_float, default_float));
                                    }
                                 }
                                 auto dijetsystem = p4[0] + p4[1];
                                 return dijetsystem.mass();
                             };
    auto df1 = 
        df.Define(outputname, mass_calculation, {particle_pts, particle_etas, particle_phis, particle_masses, goodjets_index});
    return df1;
}

ROOT::RDF::RNode 
Calculate_JetDeltaEta(ROOT::RDF::RNode df, const std::string &outputname,
                                 const std::string &particle_pts,
                                 const std::string &particle_etas,
                                 const std::string &particle_phis,
                                 const std::string &particle_masses,
                                 const std::string &goodjets_index) {
    auto delta_eta_calculation = [](const ROOT::RVec<float> &particle_pts,
                               const ROOT::RVec<float> &particle_etas,
                               const ROOT::RVec<float> &particle_phis,
                               const ROOT::RVec<float> &particle_masses,
                               const ROOT::RVec<int> &goodjets_index) {
                                 std::vector<float> etas;
                                 for (unsigned int k = 0; k < 2; ++k) {
                                    try {
                                        etas.push_back(particle_etas.at(goodjets_index[k]));
                                    } catch (const std::out_of_range &e) {
                                        etas.push_back(default_float);
                                    }
                                 }
                                 auto delta_eta = abs(etas[0]-etas[1]);
                                 return delta_eta;
                             };
    auto df1 = 
        df.Define(outputname, delta_eta_calculation, {particle_pts, particle_etas, particle_phis, particle_masses, goodjets_index});
    return df1;
}

///end write

// vhmm extend to N particle overlap removal
/// Function to veto jets overlapping with particle candidates
///
/// \param[in] df the input dataframe
/// \param[out] output_col the name of the produced mask \param[in] jet_eta name
/// of the jet etas \param[in] jet_phi name of the jet phis \param[in] p4_1 four
/// vector of the first particle candidate \param[in] p4_2 four vector of the
/// second particle candidate \param[in] deltaRmin minimum required distance in
/// dR between jets and particle candidates
///
/// \return a dataframe containing the new mask
ROOT::RDF::RNode
VetoOverlappingJets(ROOT::RDF::RNode df, const std::string &output_col,
                    const std::string &jet_eta, const std::string &jet_phi,
                    const std::string &muon_eta, const std::string &muon_phi, const std::string &muon_mask,
                    const float &deltaRmin) {
    auto df1 = df.Define(
        output_col,
        [deltaRmin](const ROOT::RVec<float> &jet_eta,
                    const ROOT::RVec<float> &jet_phi,
                    const ROOT::RVec<float> &muon_eta,
                    const ROOT::RVec<float> &muon_phi,
                    const ROOT::RVec<int> &muon_mask) {
            Logger::get("VetoOverlappingJets (N particles)")
                ->debug("Checking jets");
            ROOT::RVec<int> mask(jet_eta.size(), 1);
            for (std::size_t idx = 0; idx < mask.size(); ++idx) {
                ROOT::Math::RhoEtaPhiVectorF jet(0, jet_eta.at(idx),
                                                 jet_phi.at(idx));
                Logger::get("VetoOverlappingJets (N particles)")
                    ->debug("Jet {}:  Eta: {} Phi: {} ", idx, jet.Eta(), jet.Phi());
                int _mdx = 0;
                for(std::size_t mdx = 0; mdx < muon_mask.size(); ++mdx){
                    if( muon_mask[mdx] == 0 ) continue; // only check with the selected muons
                    ROOT::Math::RhoEtaPhiVectorF muon(0, muon_eta.at(mdx), muon_phi.at(mdx));
                    Logger::get("VetoOverlappingJets (N particles)")
                        ->debug("Lepton {}:  Eta: {} Phi: {} ", _mdx, muon.Eta(), muon.Phi());
                    auto deltaR = ROOT::Math::VectorUtil::DeltaR(jet, muon);
                    Logger::get("VetoOverlappingJets (N particles)")
                        ->debug("DeltaR {}", deltaR);
                    mask[idx] = mask[idx]&&(deltaR > deltaRmin);
                    ++_mdx;
                }
            }
            Logger::get("VetoOverlappingJets (N particles)")
                ->debug("vetomask due to overlap: {}", mask);
            return mask;
        },
        {jet_eta, jet_phi, muon_eta, muon_phi, muon_mask});
    return df1;
}

/////###$$$
/// Function to veto jets overlapping with particle candidates
///
/// \param[in] df the input dataframe
/// \param[out] output_col the name of the produced mask
/// \param[in] jet_eta name of the jet etas
/// \param[in] jet_phi name of the jet phis
/// \param[in] p4_1 four vector of the first particle candidate
/// \param[in] p4_2 four vector of the second particle candidate
/// \param[in] deltaRmin minimum required distance in dR between jets and
/// particle candidates
///
/// \return a dataframe containing the new mask
ROOT::RDF::RNode
VetoOverlappingJets(ROOT::RDF::RNode df, const std::string &output_col,
                    const std::string &jet_eta, const std::string &jet_phi,
                    const std::string &p4_1, const std::string &p4_2,
                    const float &deltaRmin) {
    auto df1 = df.Define(
        output_col,
        [deltaRmin](const ROOT::RVec<float> &jet_eta,
                    const ROOT::RVec<float> &jet_phi,
                    const ROOT::Math::PtEtaPhiMVector &p4_1,
                    const ROOT::Math::PtEtaPhiMVector &p4_2) {
            Logger::get("VetoOverlappingJets (2 particles)")
                ->debug("Checking jets");
            ROOT::RVec<int> mask(jet_eta.size(), 1);
            for (std::size_t idx = 0; idx < mask.size(); ++idx) {
                ROOT::Math::RhoEtaPhiVectorF jet(0, jet_eta.at(idx),
                                                 jet_phi.at(idx));
                Logger::get("VetoOverlappingJets (2 particles)")
                    ->debug("Jet:  Eta: {} Phi: {} ", jet.Eta(), jet.Phi());
                Logger::get("VetoOverlappingJets (2 particles)")
                    ->debug("Letpon 1 {}:  Eta: {} Phi: {}, Pt{}", p4_1,
                            p4_1.Eta(), p4_1.Phi(), p4_1.Pt());
                Logger::get("VetoOverlappingJets (2 particles)")
                    ->debug("Lepton 2 {}:  Eta: {} Phi: {}, Pt{}", p4_2,
                            p4_2.Eta(), p4_2.Phi(), p4_2.Pt());
                auto deltaR_1 = ROOT::Math::VectorUtil::DeltaR(jet, p4_1);
                auto deltaR_2 = ROOT::Math::VectorUtil::DeltaR(jet, p4_2);
                Logger::get("VetoOverlappingJets (2 particles)")
                    ->debug("DeltaR 1 {}", deltaR_1);
                Logger::get("VetoOverlappingJets (2 particles)")
                    ->debug("DeltaR 2 {}", deltaR_2);
                mask[idx] = (deltaR_1 > deltaRmin && deltaR_2 > deltaRmin);
            }
            Logger::get("VetoOverlappingJets (2 particles)")
                ->debug("vetomask due to overlap: {}", mask);
            return mask;
        },
        {jet_eta, jet_phi, p4_1, p4_2});
    return df1;
}

/// Function to veto jets overlapping with particle candidates
///
/// \param[in] df the input dataframe
/// \param[out] output_col the name of the produced mask
/// \param[in] jet_eta name of the jet etas
/// \param[in] jet_phi name of the jet phis
/// \param[in] p4_1 four vector of the first particle candidate
/// \param[in] deltaRmin minimum required distance in dR between jets and
/// particle candidates
///
/// \return a dataframe containing the new mask
ROOT::RDF::RNode
VetoOverlappingJets(ROOT::RDF::RNode df, const std::string &output_col,
                    const std::string &jet_eta, const std::string &jet_phi,
                    const std::string &p4_1, const float &deltaRmin) {
    auto df1 = df.Define(
        output_col,
        [deltaRmin](const ROOT::RVec<float> &jet_eta,
                    const ROOT::RVec<float> &jet_phi,
                    const ROOT::Math::PtEtaPhiMVector &p4_1) {
            Logger::get("VetoOverlappingJets")->debug("Checking jets");
            ROOT::RVec<int> mask(jet_eta.size(), 1);
            for (std::size_t idx = 0; idx < mask.size(); ++idx) {
                ROOT::Math::RhoEtaPhiVectorF jet(0, jet_eta.at(idx),
                                                 jet_phi.at(idx));
                Logger::get("VetoOverlappingJets")
                    ->debug("Jet:  Eta: {} Phi: {} ", jet.Eta(), jet.Phi());
                Logger::get("VetoOverlappingJets")
                    ->debug("Letpon 1 {}:  Eta: {} Phi: {}, Pt{}", p4_1,
                            p4_1.Eta(), p4_1.Phi(), p4_1.Pt());
                auto deltaR_1 = ROOT::Math::VectorUtil::DeltaR(jet, p4_1);
                Logger::get("VetoOverlappingJets")
                    ->debug("DeltaR 1 {}", deltaR_1);
                mask[idx] = (deltaR_1 > deltaRmin);
            }
            Logger::get("VetoOverlappingJets")
                ->debug("vetomask due to overlap: {}", mask);
            return mask;
        },
        {jet_eta, jet_phi, p4_1});
    return df1;
}

/// Function to veto jets overlapping with particle candidates (with isolation
/// condition)
///
/// \param[in] df the input dataframe
/// \param[out] output_col the name of the produced mask
/// \param[in] jet_eta name of the jet etas
/// \param[in] jet_phi name of the jet phis
/// \param[in] p4_1 four vector of the first particle candidate
/// \param[in] lep_is_iso isolation condition of the first particle candidate
/// \param[in] deltaRmin minimum required  distance in dR between jets and
/// particle candidates
///
/// \return a dataframe containing the new mask
ROOT::RDF::RNode VetoOverlappingJetsIsoLepOnly(ROOT::RDF::RNode df,
                                               const std::string &output_col,
                                               const std::string &jet_eta,
                                               const std::string &jet_phi,
                                               const std::string &p4_1,
                                               const std::string &lep_is_iso,
                                               const float &deltaRmin) {
    auto df1 = df.Define(
        output_col,
        [deltaRmin](
            const ROOT::RVec<float> &jet_eta, const ROOT::RVec<float> &jet_phi,
            const ROOT::Math::PtEtaPhiMVector &p4_1, const int &lep_is_iso) {
            Logger::get("VetoOverlappingJets")->debug("Checking jets");
            ROOT::RVec<int> mask(jet_eta.size(), 1);
            for (std::size_t idx = 0; idx < mask.size(); ++idx) {
                ROOT::Math::RhoEtaPhiVectorF jet(0, jet_eta.at(idx),
                                                 jet_phi.at(idx));
                Logger::get("VetoOverlappingJets")
                    ->debug("Jet:  Eta: {} Phi: {} ", jet.Eta(), jet.Phi());
                Logger::get("VetoOverlappingJets")
                    ->debug("Letpon 1 {}:  Eta: {} Phi: {}, Pt{}", p4_1,
                            p4_1.Eta(), p4_1.Phi(), p4_1.Pt());
                auto deltaR_1 = ROOT::Math::VectorUtil::DeltaR(jet, p4_1);
                Logger::get("VetoOverlappingJets")
                    ->debug("DeltaR 1 {}", deltaR_1);
                if (lep_is_iso == +1)
                    mask[idx] = (deltaR_1 > deltaRmin);
            }
            Logger::get("VetoOverlappingJets")
                ->debug("vetomask due to overlap: {}", mask);
            return mask;
        },
        {jet_eta, jet_phi, p4_1, lep_is_iso});
    return df1;
}

/// Function to determine pt order of jets
///
/// \param[in] df the input dataframe
/// \param[out] output_col the name of the produced mask
/// \param[in] jet_pt name of the jet pts
/// \param[in] jetmask_name name of the mask marking all valid
/// jets to be considered
///
/// \return a dataframe containing a list of jet indices sorted by pt
ROOT::RDF::RNode OrderJetsByPt(ROOT::RDF::RNode df,
                               const std::string &output_col,
                               const std::string &jet_pt,
                               const std::string &jetmask_name) {
    auto df1 = df.Define(
        output_col,
        [output_col, jetmask_name](const ROOT::RVec<int> &jetmask,
                                   const ROOT::RVec<float> &jet_pt) {
            Logger::get("OrderJetsByPt")
                ->debug("Ordering good jets from {} by pt, output stored in {}",
                        jetmask_name, output_col);
            Logger::get("OrderJetsByPt")->debug("Jetpt before {}", jet_pt);
            Logger::get("OrderJetsByPt")->debug("Mask {}", jetmask);
            auto good_jets_pt =
                ROOT::VecOps::Where(jetmask > 0, jet_pt, (float)0.);
            Logger::get("OrderJetsByPt")->debug("Jetpt after {}", good_jets_pt);
            // we have to convert the result into an RVec of ints since argsort
            // gives back an unsigned long vector
            auto temp = ROOT::VecOps::Intersect(
                ROOT::VecOps::Argsort(good_jets_pt,
                                      [](double x, double y) { return x > y; }),
                ROOT::VecOps::Nonzero(good_jets_pt));
            Logger::get("OrderJetsByPt")->debug("jet Indices {}", temp);
            ROOT::RVec<int> result(temp.size());
            std::transform(temp.begin(), temp.end(), result.begin(),
                           [](unsigned long int x) { return (int)x; });
            Logger::get("OrderJetsByPt")->debug("jet Indices int {}", result);
            return result;
        },
        {jetmask_name, jet_pt});
    return df1;
}
} // end namespace jet

namespace physicsobject {
namespace jet {

/// Function to cut jets based on the jet ID
///
/// \param[in] df the input dataframe
/// \param[out] maskname the name of the new mask to be added as column to the
/// dataframe
/// \param[in] nameID name of the ID column in the NanoAOD
/// \param[in] idxID bitvalue of the WP the has to be passed
///
/// \return a dataframe containing the new mask
ROOT::RDF::RNode CutID(ROOT::RDF::RNode df, const std::string &maskname,
                       const std::string &nameID, const int &idxID) {
    auto df1 = df.Define(maskname, basefunctions::FilterJetID(idxID), {nameID});
    return df1;
}

ROOT::RDF::RNode CutID(ROOT::RDF::RNode df, const std::string &maskname,
                       const std::string &nameID, const UChar_t &idxID) {
    auto df1 = df.Define(maskname, basefunctions::FilterJetID(idxID), {nameID});
    return df1;
}

ROOT::RDF::RNode JetIdTightLepVeto_Cut(ROOT::RDF::RNode df,
                                       const std::string &output_col,
                                       const std::string &jet_eta,
                                       const std::string &jet_jetId,
                                       const std::string &jet_neHEF,
                                       const std::string &jet_neEmEF,
                                       const std::string &jet_muEF,
                                       const std::string &jet_chEmEF)
{
    // Define a new column in the dataset, "output_col", using the provided column names
    auto df1 = df.Define(
        output_col,
        [](const ROOT::RVec<float> &Jet_eta,
           const ROOT::RVec<int>   &Jet_jetId,
           const ROOT::RVec<float> &Jet_neHEF,
           const ROOT::RVec<float> &Jet_neEmEF,
           const ROOT::RVec<float> &Jet_muEF,
           const ROOT::RVec<float> &Jet_chEmEF)
        {
            // The output will be a boolean vector, one entry per jet.
            ROOT::RVec<int> PassJetId_FailTightLepVeto(Jet_eta.size(), 0);

            for (size_t i = 0; i < Jet_eta.size(); ++i) {
                // 1) Compute Jet_passJetIdTight
                bool jet_passTight = false;
                float absEta = std::abs(Jet_eta[i]);

                // Check 2nd bit of jetId: (1 << 1) means bit index 1 (a value of 2)
                if (absEta <= 2.7) {
                    jet_passTight = (Jet_jetId[i] & (1 << 1));
                }
                else if (absEta <= 3.0) {
                    jet_passTight = ((Jet_jetId[i] & (1 << 1)) && (Jet_neHEF[i] < 0.99));
                }
                else {
                    // absEta > 3.0
                    jet_passTight = ((Jet_jetId[i] & (1 << 1)) && (Jet_neEmEF[i] < 0.4));
                }

                // 2) Compute Jet_passJetIdTightLepVeto
                bool jet_passTightLepVeto = false;
                if (absEta <= 2.7) {
                    jet_passTightLepVeto = jet_passTight &&
                                           (Jet_muEF[i]  < 0.8) &&
                                           (Jet_chEmEF[i] < 0.8);
                } else {
                    jet_passTightLepVeto = jet_passTight;
                }

                //PassJetId_FailTightLepVeto[i] = (jet_passTight && (!jet_passTightLepVeto));
                PassJetId_FailTightLepVeto[i] = jet_passTight;
            }

            return PassJetId_FailTightLepVeto; // RVec<bool>
        },
        // Columns that the lambda above depends on
        {jet_eta, jet_jetId, jet_neHEF, jet_neEmEF, jet_muEF, jet_chEmEF}
    );

    // Return the updated RNode
    return df1;
}
////////
/// Function to cut jets based on the jet pileup ID
///
/// \param[in] df the input dataframe
/// \param[out] maskname the name of the new mask to be added as column to the
/// dataframe
/// \param[in] nameID name of the ID column in the NanoAOD
/// \param[in] idxID bitvalue of the WP the has to be passed
/// \param[in] jet_pt name of the input jet pts
/// \param[in] jet_pt_cut threshold for the input jet pts
///
/// \return a dataframe containing the new mask
ROOT::RDF::RNode CutPUID(ROOT::RDF::RNode df, const std::string &maskname,
                         const std::string &nameID, const std::string &jet_pt,
                         const int &idxID, const float &jet_pt_cut) {
    auto df1 =
        df.Define(maskname, basefunctions::FilterJetPUID(idxID, jet_pt_cut),
                  {nameID, jet_pt});
    return df1;
}

/// Function to shift and smear jet pt for MC
///
/// \param[in] df the input dataframe
/// \param[out] corrected_jet_pt the name of the shifted and smeared jet pts
/// \param[in] jet_pt name of the input jet pts
/// \param[in] jet_eta name of the jet etas
/// \param[in] jet_phi name of the jet phis
/// \param[in] jet_area name of the jet catchment area
/// \param[in] jet_rawFactor name of the raw factor for jet pt
/// \param[in] jet_ID name of the jet ID
/// \param[in] gen_jet_pt name of the gen jet pts
/// \param[in] gen_jet_eta name of the gen jet etas
/// \param[in] gen_jet_phi name of the gen jet phis
/// \param[in] rho name of the pileup density
/// \param[in] reapplyJES boolean for reapplying the JES correction
/// \param[in] jes_shift_sources vector of JEC unc source names to be applied
/// in one group
/// \param[in] jes_shift parameter to control jet energy
/// scale shift: 0 - nominal; 1 - Up; -1 - Down
/// \param[in] jer_shift parameter to control jet energy resolution
/// shift: "nom"; "up"; "down"
/// \param[in] jec_file path to the file with JES/JER information
/// \param[in] jer_tag era dependent tag for JER
/// \param[in] jes_tag era dependent tag for JES
/// \param[in] jec_algo algorithm used for jets e.g. AK4PFchs
///
/// \return a dataframe containing the modified jet pts
ROOT::RDF::RNode
JetPtCorrection(ROOT::RDF::RNode df, const std::string &corrected_jet_pt,
                const std::string &jet_pt, const std::string &jet_eta,
                const std::string &jet_phi, const std::string &jet_area,
                const std::string &jet_rawFactor, const std::string &jet_ID,
                const std::string &gen_jet_pt, const std::string &gen_jet_eta,
                const std::string &gen_jet_phi, const std::string &rho,
                bool reapplyJES,
                const std::vector<std::string> &jes_shift_sources,
                const int &jes_shift, const std::string &jer_shift,
                const std::string &jec_file, const std::string &jer_tag,
                const std::string &jes_tag, const std::string &jec_algo) {
    // identifying jet radius from algorithm
    float jet_dR = 0.4;
    if (jec_algo.find("AK8") != std::string::npos) {
        jet_dR = 0.8;
    }
    // loading JES variations
    std::vector<std::shared_ptr<const correction::Correction>>
        JetEnergyScaleShifts;
    for (const auto &source : jes_shift_sources) {
        // check if any JES shift is chosen
        if (source != "" && source != "HEMIssue") {
            auto JES_source_evaluator =
                correction::CorrectionSet::from_file(jec_file)->at(
                    jes_tag + "_" + source + "_" + jec_algo);
            JetEnergyScaleShifts.push_back(JES_source_evaluator);
        }
    };
    // loading jet energy correction scale factor evaluation function
    auto JES_evaluator =
        correction::CorrectionSet::from_file(jec_file)->compound().at(
            jes_tag + "_L1L2L3Res_" + jec_algo);
    auto JetEnergyScaleSF = [JES_evaluator](const float area, const float eta,
                                            const float pt, const float rho) {
        return JES_evaluator->evaluate({area, eta, pt, rho});
    };
    // loading relative pT resolution evaluation function
    auto JER_resolution_evaluator =
        correction::CorrectionSet::from_file(jec_file)->at(
            jer_tag + "_PtResolution_" + jec_algo);
    auto JetEnergyResolution = [JER_resolution_evaluator](const float eta,
                                                          const float pt,
                                                          const float rho) {
        return JER_resolution_evaluator->evaluate({eta, pt, rho});
    };
    // loading JER scale factor evaluation function
    auto JER_SF_evaluator = correction::CorrectionSet::from_file(jec_file)->at(
        jer_tag + "_ScaleFactor_" + jec_algo);
    auto JetEnergyResolutionSF =
        [JER_SF_evaluator](const float eta, const std::string jer_shift) {
            return JER_SF_evaluator->evaluate({eta, jer_shift});
        };
    // lambda run with dataframe
    auto JetEnergyCorrectionLambda = [reapplyJES, JetEnergyScaleShifts,
                                      JetEnergyScaleSF, JetEnergyResolution,
                                      JetEnergyResolutionSF, jes_shift_sources,
                                      jes_shift, jer_shift, jet_dR](
                                         const ROOT::RVec<float> &pt_values,
                                         const ROOT::RVec<float> &eta_values,
                                         const ROOT::RVec<float> &phi_values,
                                         const ROOT::RVec<float> &area_values,
                                         const ROOT::RVec<float>
                                             &rawFactor_values,
                                         const ROOT::RVec<int> &ID_values,
                                         const ROOT::RVec<float> &gen_pt_values,
                                         const ROOT::RVec<float>
                                             &gen_eta_values,
                                         const ROOT::RVec<float>
                                             &gen_phi_values,
                                         const float &rho_value) {
        // random value generator for jet smearing
        TRandom3 randm = TRandom3(0);

        ROOT::RVec<float> pt_values_corrected;
        for (int i = 0; i < pt_values.size(); i++) {
            float corr_pt = pt_values.at(i);
            if (reapplyJES) {
                // reapplying the JES correction
                float raw_pt = pt_values.at(i) * (1 - rawFactor_values.at(i));
                float corr = JetEnergyScaleSF(
                    area_values.at(i), eta_values.at(i), raw_pt, rho_value);
                corr_pt = raw_pt * corr;
                Logger::get("JetEnergyScale")
                    ->debug("reapplying JE scale: orig. jet pt {} to raw "
                            "jet pt {} to recorr. jet pt {}",
                            pt_values.at(i), raw_pt, corr_pt);
            }
            pt_values_corrected.push_back(corr_pt);

            // apply jet energy smearing - hybrid method as described in
            // https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetResolution
            float reso = JetEnergyResolution(
                eta_values.at(i), pt_values_corrected.at(i), rho_value);
            float resoSF = JetEnergyResolutionSF(eta_values.at(i), jer_shift);
            Logger::get("JetEnergyResolution")
                ->debug("Calculate JER {}:  SF: {} resolution: {} ", jer_shift,
                        resoSF, reso);
            // gen jet matching algorithm for JER
            ROOT::Math::RhoEtaPhiVectorF jet(
                pt_values_corrected.at(i), eta_values.at(i), phi_values.at(i));
            float genjetpt = -1.0;
            Logger::get("JetEnergyResolution")
                ->debug("Going to smear jet:  Eta: {} Phi: {} ", jet.Eta(),
                        jet.Phi());
            double min_dR = std::numeric_limits<double>::infinity();
            for (int j = 0; j < gen_pt_values.size(); j++) {
                ROOT::Math::RhoEtaPhiVectorF genjet(gen_pt_values.at(j),
                                                    gen_eta_values.at(j),
                                                    gen_phi_values.at(j));
                Logger::get("JetEnergyResolution")
                    ->debug("Checking gen Jet:  Eta: {} Phi: {}", genjet.Eta(),
                            genjet.Phi());
                auto deltaR = ROOT::Math::VectorUtil::DeltaR(jet, genjet);
                if (deltaR > min_dR)
                    continue;
                if (deltaR < (jet_dR / 2.) &&
                    std::abs(pt_values_corrected.at(i) - gen_pt_values.at(j)) <
                        (3.0 * reso * pt_values_corrected.at(i))) {
                    min_dR = deltaR;
                    genjetpt = gen_pt_values.at(j);
                }
            }
            // if jet matches a gen jet scaling method is applied,
            // otherwise stochastic method
            if (genjetpt > 0.0) {
                Logger::get("JetEnergyResolution")
                    ->debug("Found gen jet for hybrid smearing method");
                double shift = (resoSF - 1.0) *
                               (pt_values_corrected.at(i) - genjetpt) /
                               pt_values_corrected.at(i);
                pt_values_corrected.at(i) *= std::max(0.0, 1.0 + shift);
            } else {
                Logger::get("JetEnergyResolution")
                    ->debug("No gen jet found. Applying stochastic smearing.");
                double shift = randm.Gaus(0, reso) *
                               std::sqrt(std::max(resoSF * resoSF - 1., 0.0));
                pt_values_corrected.at(i) *= std::max(0.0, 1.0 + shift);
            }
            Logger::get("JetEnergyResolution")
                ->debug("Shifting jet pt from {} to {} ", corr_pt,
                        pt_values_corrected.at(i));

            // apply uncertainty shifts related to the jet energy scale
            // mostly following
            // https://github.com/cms-nanoAOD/nanoAOD-tools/blob/master/python/postprocessing/modules/jme/jetmetUncertainties.py
            float pt_scale_sf = 1.0;
            if (jes_shift != 0.0) {
                if (jes_shift_sources.at(0) != "HEMIssue") {
                    // Differentiate between single source and combined source
                    // for reduced scheme
                    if (JetEnergyScaleShifts.size() == 1) {
                        pt_scale_sf =
                            1. +
                            jes_shift * JetEnergyScaleShifts.at(0)->evaluate(
                                            {eta_values.at(i),
                                             pt_values_corrected.at(i)});
                        Logger::get("JetEnergyScaleShift")
                            ->debug("Shifting jet pt by {} for single source "
                                    "with SF {}",
                                    jes_shift, pt_scale_sf);
                    } else {
                        float quad_sum = 0.;
                        for (const auto &evaluator : JetEnergyScaleShifts) {
                            quad_sum +=
                                std::pow(evaluator->evaluate(
                                             {eta_values.at(i),
                                              pt_values_corrected.at(i)}),
                                         2.0);
                        }
                        pt_scale_sf = 1. + jes_shift * std::sqrt(quad_sum);
                        Logger::get("JetEnergyScaleShift")
                            ->debug("Shifting jet pt by {} for multiple "
                                    "sources with SF {}",
                                    jes_shift, pt_scale_sf);
                    }
                }
                // for reference:
                // https://hypernews.cern.ch/HyperNews/CMS/get/JetMET/2000.html
                else if (jes_shift_sources.at(0) == "HEMIssue") {
                    if (jes_shift == (-1.) && pt_values_corrected.at(i) > 15. &&
                        phi_values.at(i) > (-1.57) &&
                        phi_values.at(i) < (-0.87) && ID_values.at(i) == 2) {
                        if (eta_values.at(i) > (-2.5) &&
                            eta_values.at(i) < (-1.3))
                            pt_scale_sf = 0.8;
                        else if (eta_values.at(i) > (-3.) &&
                                 eta_values.at(i) <= (-2.5))
                            pt_scale_sf = 0.65;
                    }
                }
            }
            pt_values_corrected.at(i) *= pt_scale_sf;
            Logger::get("JetEnergyScaleShift")
                ->debug("Shifting jet pt from {} to {} ",
                        pt_values_corrected.at(i) / pt_scale_sf,
                        pt_values_corrected.at(i));

            // if (pt_values_corrected.at(i)>15.0), this
            // correction should be propagated to MET
            // (requirement for type I corrections)
        }
        return pt_values_corrected;
    };
    auto df1 = df.Define(corrected_jet_pt, JetEnergyCorrectionLambda,
                         {jet_pt, jet_eta, jet_phi, jet_area, jet_rawFactor,
                          jet_ID, gen_jet_pt, gen_jet_eta, gen_jet_phi, rho});
    return df1;
}
/// Function to shift and smear jet pt for MC
///
/// \param[in] df the input dataframe
/// \param[out] corrected_jet_pt the name of the shifted and smeared jet pts
/// \param[in] jet_pt name of the input jet pts
/// \param[in] jet_eta name of the jet etas
/// \param[in] jet_phi name of the jet phis
/// \param[in] jet_area name of the jet catchment area
/// \param[in] jet_rawFactor name of the raw factor for jet pt
/// \param[in] jet_ID name of the jet ID
/// \param[in] gen_jet_pt name of the gen jet pts
/// \param[in] gen_jet_eta name of the gen jet etas
/// \param[in] gen_jet_phi name of the gen jet phis
/// \param[in] rho name of the pileup density
/// \param[in] reapplyJES boolean for reapplying the JES correction
/// \param[in] jes_shift_sources vector of JEC unc source names to be applied
/// in one group
/// \param[in] jes_shift parameter to control jet energy
/// scale shift: 0 - nominal; 1 - Up; -1 - Down
/// \param[in] jer_shift parameter to control jet energy resolution
/// shift: "nom"; "up"; "down"
/// \param[in] jec_file path to the file with JES/JER information
/// \param[in] jer_tag era dependent tag for JER
/// \param[in] jes_tag era dependent tag for JES
/// \param[in] jec_algo algorithm used for jets e.g. AK4PFchs
///
/// \return a dataframe containing the modified jet pts
ROOT::RDF::RNode
JetPtCorrection_2022(ROOT::RDF::RNode df, const std::string &corrected_jet_pt,
                const std::string &jet_pt, const std::string &jet_eta,
                const std::string &jet_phi, const std::string &jet_area,
                const std::string &jet_rawFactor, const std::string &jet_ID,
                const std::string &gen_jet_pt, const std::string &gen_jet_eta,
                const std::string &gen_jet_phi, const std::string &rho,
                bool reapplyJES,
                const std::vector<std::string> &jes_shift_sources,
                const int &jes_shift, const std::string &jer_shift,
                const std::string &jec_file, const std::string &jer_tag,
                const std::string &jes_tag, const std::string &jec_algo) {
    // identifying jet radius from algorithm
    float jet_dR = 0.4;
    if (jec_algo.find("AK8") != std::string::npos) {
        jet_dR = 0.8;
    }
    // loading JES variations
    std::vector<std::shared_ptr<const correction::Correction>>
        JetEnergyScaleShifts;
    for (const auto &source : jes_shift_sources) {
        // check if any JES shift is chosen
        if (source != "" && source != "HEMIssue") {
            auto JES_source_evaluator =
                correction::CorrectionSet::from_file(jec_file)->at(
                    jes_tag + "_" + source + "_" + jec_algo);
            JetEnergyScaleShifts.push_back(JES_source_evaluator);
        }
    };
    // loading jet energy correction scale factor evaluation function
    auto JES_evaluator =
        correction::CorrectionSet::from_file(jec_file)->compound().at(
            jes_tag + "_L1L2L3Res_" + jec_algo);
    auto JetEnergyScaleSF = [JES_evaluator](const float area, const float eta,
                                            const float pt, const float rho) {
        return JES_evaluator->evaluate({area, eta, pt, rho});
    };
    // loading relative pT resolution evaluation function
    auto JER_resolution_evaluator =
        correction::CorrectionSet::from_file(jec_file)->at(
            jer_tag + "_PtResolution_" + jec_algo);
    auto JetEnergyResolution = [JER_resolution_evaluator](const float eta,
                                                          const float pt,
                                                          const float rho) {
        return JER_resolution_evaluator->evaluate({eta, pt, rho});
    };
    // loading JER scale factor evaluation function
    auto JER_SF_evaluator = correction::CorrectionSet::from_file(jec_file)->at(
        jer_tag + "_ScaleFactor_" + jec_algo);
    auto JetEnergyResolutionSF =
        [JER_SF_evaluator](const float eta, const float pt, const std::string jer_shift) {
            return JER_SF_evaluator->evaluate({eta, pt, jer_shift});
        };
    // lambda run with dataframe
    auto JetEnergyCorrectionLambda = [reapplyJES, JetEnergyScaleShifts,
                                      JetEnergyScaleSF, JetEnergyResolution,
                                      JetEnergyResolutionSF, jes_shift_sources,
                                      jes_shift, jer_shift, jet_dR](
                                         const ROOT::RVec<float> &pt_values,
                                         const ROOT::RVec<float> &eta_values,
                                         const ROOT::RVec<float> &phi_values,
                                         const ROOT::RVec<float> &area_values,
                                         const ROOT::RVec<float>
                                             &rawFactor_values,
                                         const ROOT::RVec<int> &ID_values,
                                         const ROOT::RVec<float> &gen_pt_values,
                                         const ROOT::RVec<float>
                                             &gen_eta_values,
                                         const ROOT::RVec<float>
                                             &gen_phi_values,
                                         const float &rho_value) {
        // random value generator for jet smearing
        TRandom3 randm = TRandom3(0);

        ROOT::RVec<float> pt_values_corrected;
        for (int i = 0; i < pt_values.size(); i++) {
            float corr_pt = pt_values.at(i);
            if (reapplyJES) {
                // reapplying the JES correction
                float raw_pt = pt_values.at(i) * (1 - rawFactor_values.at(i));
                float corr = JetEnergyScaleSF(
                    area_values.at(i), eta_values.at(i), raw_pt, rho_value);
                corr_pt = raw_pt * corr;
                Logger::get("JetEnergyScale")
                    ->debug("reapplying JE scale: orig. jet pt {} to raw "
                            "jet pt {} to recorr. jet pt {}",
                            pt_values.at(i), raw_pt, corr_pt);
            }
            pt_values_corrected.push_back(corr_pt);

            // apply jet energy smearing - hybrid method as described in
            // https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetResolution
            float reso = JetEnergyResolution(
                eta_values.at(i), pt_values_corrected.at(i), rho_value);
            float resoSF = JetEnergyResolutionSF(eta_values.at(i), pt_values_corrected.at(i), jer_shift);
            Logger::get("JetEnergyResolution")
                ->debug("Calculate JER {}:  SF: {} resolution: {} ", jer_shift,
                        resoSF, reso);
            // gen jet matching algorithm for JER
            ROOT::Math::RhoEtaPhiVectorF jet(
                pt_values_corrected.at(i), eta_values.at(i), phi_values.at(i));
            float genjetpt = -1.0;
            Logger::get("JetEnergyResolution")
                ->debug("Going to smear jet:  Eta: {} Phi: {} ", jet.Eta(),
                        jet.Phi());
            double min_dR = std::numeric_limits<double>::infinity();
            for (int j = 0; j < gen_pt_values.size(); j++) {
                ROOT::Math::RhoEtaPhiVectorF genjet(gen_pt_values.at(j),
                                                    gen_eta_values.at(j),
                                                    gen_phi_values.at(j));
                Logger::get("JetEnergyResolution")
                    ->debug("Checking gen Jet:  Eta: {} Phi: {}", genjet.Eta(),
                            genjet.Phi());
                auto deltaR = ROOT::Math::VectorUtil::DeltaR(jet, genjet);
                if (deltaR > min_dR)
                    continue;
                if (deltaR < (jet_dR / 2.) &&
                    std::abs(pt_values_corrected.at(i) - gen_pt_values.at(j)) <
                        (3.0 * reso * pt_values_corrected.at(i))) {
                    min_dR = deltaR;
                    genjetpt = gen_pt_values.at(j);
                }
            }
            // if jet matches a gen jet scaling method is applied,
            // otherwise stochastic method
            if (genjetpt > 0.0) {
                Logger::get("JetEnergyResolution")
                    ->debug("Found gen jet for hybrid smearing method");
                double shift = (resoSF - 1.0) *
                               (pt_values_corrected.at(i) - genjetpt) /
                               pt_values_corrected.at(i);
                pt_values_corrected.at(i) *= std::max(0.0, 1.0 + shift);
            } else {
                Logger::get("JetEnergyResolution")
                    ->debug("No gen jet found. Applying stochastic smearing.");
                double shift = randm.Gaus(0, reso) *
                               std::sqrt(std::max(resoSF * resoSF - 1., 0.0));
                pt_values_corrected.at(i) *= std::max(0.0, 1.0 + shift);
            }
            Logger::get("JetEnergyResolution")
                ->debug("Shifting jet pt from {} to {} ", corr_pt,
                        pt_values_corrected.at(i));

            // apply uncertainty shifts related to the jet energy scale
            // mostly following
            // https://github.com/cms-nanoAOD/nanoAOD-tools/blob/master/python/postprocessing/modules/jme/jetmetUncertainties.py
            float pt_scale_sf = 1.0;
            if (jes_shift != 0.0) {
                if (jes_shift_sources.at(0) != "HEMIssue") {
                    // Differentiate between single source and combined source
                    // for reduced scheme
                    if (JetEnergyScaleShifts.size() == 1) {
                        pt_scale_sf =
                            1. +
                            jes_shift * JetEnergyScaleShifts.at(0)->evaluate(
                                            {eta_values.at(i),
                                             pt_values_corrected.at(i)});
                        Logger::get("JetEnergyScaleShift")
                            ->debug("Shifting jet pt by {} for single source "
                                    "with SF {}",
                                    jes_shift, pt_scale_sf);
                    } else {
                        float quad_sum = 0.;
                        for (const auto &evaluator : JetEnergyScaleShifts) {
                            quad_sum +=
                                std::pow(evaluator->evaluate(
                                             {eta_values.at(i),
                                              pt_values_corrected.at(i)}),
                                         2.0);
                        }
                        pt_scale_sf = 1. + jes_shift * std::sqrt(quad_sum);
                        Logger::get("JetEnergyScaleShift")
                            ->debug("Shifting jet pt by {} for multiple "
                                    "sources with SF {}",
                                    jes_shift, pt_scale_sf);
                    }
                }
                // for reference:
                // https://hypernews.cern.ch/HyperNews/CMS/get/JetMET/2000.html
                else if (jes_shift_sources.at(0) == "HEMIssue") {
                    if (jes_shift == (-1.) && pt_values_corrected.at(i) > 15. &&
                        phi_values.at(i) > (-1.57) &&
                        phi_values.at(i) < (-0.87) && ID_values.at(i) == 2) {
                        if (eta_values.at(i) > (-2.5) &&
                            eta_values.at(i) < (-1.3))
                            pt_scale_sf = 0.8;
                        else if (eta_values.at(i) > (-3.) &&
                                 eta_values.at(i) <= (-2.5))
                            pt_scale_sf = 0.65;
                    }
                }
            }
            pt_values_corrected.at(i) *= pt_scale_sf;
            Logger::get("JetEnergyScaleShift")
                ->debug("Shifting jet pt from {} to {} ",
                        pt_values_corrected.at(i) / pt_scale_sf,
                        pt_values_corrected.at(i));

            // if (pt_values_corrected.at(i)>15.0), this
            // correction should be propagated to MET
            // (requirement for type I corrections)
        }
        return pt_values_corrected;
    };
    auto df1 = df.Define(corrected_jet_pt, JetEnergyCorrectionLambda,
                         {jet_pt, jet_eta, jet_phi, jet_area, jet_rawFactor,
                          jet_ID, gen_jet_pt, gen_jet_eta, gen_jet_phi, rho});
    return df1;
}
///from Zhiyuan Li
ROOT::RDF::RNode
JetPtCorrection_2022(ROOT::RDF::RNode df, const std::string &corrected_jet_pt,
                const std::string &jet_pt, const std::string &jet_eta,
                const std::string &jet_phi, const std::string &jet_area,
                const std::string &jet_rawFactor, const std::string &jet_ID,
                const std::string &gen_jet_pt, const std::string &gen_jet_eta,
                const std::string &gen_jet_phi, const std::string &rho,
                bool reapplyJES,
                const std::vector<std::string> &jes_shift_sources,
                const int &jes_shift, const std::string &jer_shift,
                const std::string &jec_file, const std::string &jer_tag,
                const std::string &jes_tag, const std::string &jec_algo, 
                const std::string &jet_veto_map, const std::string &jet_veto_tag) {
    // identifying jet radius from algorithm
    float jet_dR = 0.4;
    if (jec_algo.find("AK8") != std::string::npos) {
        jet_dR = 0.8;
    }
    // loading JES variations
    std::vector<std::shared_ptr<const correction::Correction>>
        JetEnergyScaleShifts;
    for (const auto &source : jes_shift_sources) {
        // check if any JES shift is chosen
        if (source != "" && source != "HEMIssue") {
            auto JES_source_evaluator =
                correction::CorrectionSet::from_file(jec_file)->at(
                    jes_tag + "_" + source + "_" + jec_algo);
            JetEnergyScaleShifts.push_back(JES_source_evaluator);
        }
    };
    // loading jet energy correction scale factor evaluation function
    // 2022 (with python): >>> list(ceval.compound.keys())
    // ['Summer22_22Sep2023_RunCD_V2_DATA_L1L2L3Res_AK4PFPuppi', 'Summer22_22Sep2023_V2_MC_L1L2L3Res_AK4PFPuppi']
    auto JES_evaluator =
        correction::CorrectionSet::from_file(jec_file)->compound().at(
            jes_tag + "_L1L2L3Res_" + jec_algo);
    auto JetEnergyScaleSF = [JES_evaluator](const float area, const float eta,
                                            const float pt, const float rho) {
        if (std::abs(eta) < 4.7) return JES_evaluator->evaluate({area, eta, pt, rho});
        else return 1.0;
    };
    // loading relative pT resolution evaluation function
    auto JER_resolution_evaluator =
        correction::CorrectionSet::from_file(jec_file)->at(
            jer_tag + "_PtResolution_" + jec_algo);
    auto JetEnergyResolution = [JER_resolution_evaluator](const float eta,
                                                          const float pt,
                                                          const float rho) {
        if (std::abs(eta) < 4.7) return JER_resolution_evaluator->evaluate({eta, pt, rho});
        else return 1.0;
    };
    // loading JER scale factor evaluation function
    auto JER_SF_evaluator = correction::CorrectionSet::from_file(jec_file)->at(
        jer_tag + "_ScaleFactor_" + jec_algo);
    auto JetEnergyResolutionSF =
        [JER_SF_evaluator](const float eta, float pt, const std::string jer_shift) {
            try{ 
                // annoyingly the 2022 EE has 3 inputs, 
                // 2022 post EE has 2 inputs
                if (std::abs(eta) < 4.7) return JER_SF_evaluator->evaluate({eta, pt, jer_shift});    
                else return 1.0;
            }
            catch (const std::exception&) {
            if (std::abs(eta) < 4.7) return JER_SF_evaluator->evaluate({eta,  jer_shift});
            else return 1.0;
        }
    };
    // loading jet veto maps
    auto jet_veto_map_evaluator = correction::CorrectionSet::from_file(jet_veto_map)->at(
        jet_veto_tag);
    auto jet_veto_SF =
        [jet_veto_map_evaluator](const float eta, const float phi) {
            auto tmp_phi  = phi;
            if (phi > 3.141592653589793) tmp_phi = phi - (3.141592653589793 * 2);
            if (phi < -3.141592653589793) tmp_phi = phi + (3.141592653589793 * 2);
            if (std::abs(eta) < 5.19) return jet_veto_map_evaluator->evaluate({ "jetvetomap", eta,  tmp_phi});  // the bin edge is 5.1  , 3.0 should be enough
            else return 1.0;
    };

    // lambda run with dataframe
    auto JetEnergyCorrectionLambda = [reapplyJES, JetEnergyScaleShifts,
                                      JetEnergyScaleSF, JetEnergyResolution,
                                      JetEnergyResolutionSF, jes_shift_sources,
                                      jes_shift, jer_shift, jet_dR,jet_veto_SF ](
                                         const ROOT::RVec<float> &pt_values,
                                         const ROOT::RVec<float> &eta_values,
                                         const ROOT::RVec<float> &phi_values,
                                         const ROOT::RVec<float> &area_values,
                                         const ROOT::RVec<float>
                                             &rawFactor_values,
                                         const ROOT::RVec<UChar_t> &ID_values,
                                         const ROOT::RVec<float> &gen_pt_values,
                                         const ROOT::RVec<float>
                                             &gen_eta_values,
                                         const ROOT::RVec<float>
                                             &gen_phi_values,
                                         const float &rho_value) {
        // random value generator for jet smearing
        TRandom3 randm = TRandom3(12345);
        float pt_veto = -999.0;
        ROOT::RVec<float> pt_values_corrected;
        // // apply jet veto map. If any jet lies within jet veto map, reject the events. 
        // // at the object level it's not straightforward to veto the events, so we return a RVec of pt -999 for all jets 
        
        // Flag to check if any non-zero jet_veto_sf_value is found
        bool non_zero_veto = false;
        // Loop to check if any non-zero jet_veto_sf_value exists
        for (int i = 0; i < pt_values.size(); i++) {

            Logger::get("JetEnergyResolution")
                ->debug("checking jet veto map for index {} ", i);
            float jet_veto_sf_value = jet_veto_SF(eta_values.at(i), phi_values.at(i));
            if (jet_veto_sf_value != 0) {
                non_zero_veto = true;
            }
        }
        if (non_zero_veto) {
            for (int i = 0; i < pt_values.size(); i++) {
                // do jet veto here:         
                // If any non-zero jet_veto_sf_value was found, return a vector filled with -999
                Logger::get("JetEnergyResolution")
                    ->debug("checking jet veto map for index {} ", i);
                pt_values_corrected.push_back(pt_veto);
            }
            return pt_values_corrected;
        }            

        for (int i = 0; i < pt_values.size(); i++) {
            float corr_pt = pt_values.at(i);
            if (reapplyJES) {
                // reapplying the JES correction
                float raw_pt = pt_values.at(i) * (1 - rawFactor_values.at(i));
                float corr = JetEnergyScaleSF(
                    area_values.at(i), eta_values.at(i), raw_pt, rho_value);
                corr_pt = raw_pt * corr;
                Logger::get("JetEnergyScale")
                    ->debug("reapplying JE scale: orig. jet pt {} to raw "
                            "jet pt {} to recorr. jet pt {}",
                            pt_values.at(i), raw_pt, corr_pt);
            }
            pt_values_corrected.push_back(corr_pt);

            // apply jet energy smearing - hybrid method as described in
            // https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetResolution
            float reso = JetEnergyResolution(
                eta_values.at(i), pt_values_corrected.at(i), rho_value);
            float resoSF = JetEnergyResolutionSF(eta_values.at(i), pt_values.at(i),jer_shift);
            Logger::get("JetEnergyResolution")
                ->debug("Calculate JER {}:  SF: {} resolution: {} ", jer_shift,
                        resoSF, reso);
            // gen jet matching algorithm for JER
            ROOT::Math::RhoEtaPhiVectorF jet(
                pt_values_corrected.at(i), eta_values.at(i), phi_values.at(i));
            float genjetpt = -1.0;
            Logger::get("JetEnergyResolution")
                ->debug("Going to smear jet:  Eta: {} Phi: {} ", jet.Eta(),
                        jet.Phi());
            double min_dR = std::numeric_limits<double>::infinity();
            for (int j = 0; j < gen_pt_values.size(); j++) {
                ROOT::Math::RhoEtaPhiVectorF genjet(gen_pt_values.at(j),
                                                    gen_eta_values.at(j),
                                                    gen_phi_values.at(j));
                Logger::get("JetEnergyResolution")
                    ->debug("Checking gen Jet:  Eta: {} Phi: {}", genjet.Eta(),
                            genjet.Phi());
                auto deltaR = ROOT::Math::VectorUtil::DeltaR(jet, genjet);
                if (deltaR > min_dR)
                    continue;
                if (deltaR < (jet_dR / 2.) &&
                    std::abs(pt_values_corrected.at(i) - gen_pt_values.at(j)) <
                        (3.0 * reso * pt_values_corrected.at(i))) {
                    min_dR = deltaR;
                    genjetpt = gen_pt_values.at(j);
                }
            }
            // if jet matches a gen jet scaling method is applied,
            // otherwise stochastic method
            if (genjetpt > 0.0) {
                Logger::get("JetEnergyResolution")
                    ->debug("Found gen jet for hybrid smearing method");
                double shift = (resoSF - 1.0) *
                               (pt_values_corrected.at(i) - genjetpt) /
                               pt_values_corrected.at(i);
                pt_values_corrected.at(i) *= std::max(0.0, 1.0 + shift);
            } else {
                Logger::get("JetEnergyResolution")
                    ->debug("No gen jet found. Applying stochastic smearing.");
                double shift = randm.Gaus(0, reso) *
                               std::sqrt(std::max(resoSF * resoSF - 1., 0.0));
                pt_values_corrected.at(i) *= std::max(0.0, 1.0 + shift);
            }
            Logger::get("JetEnergyResolution")
                ->debug("Shifting jet pt from {} to {} ", corr_pt,
                        pt_values_corrected.at(i));

            // apply uncertainty shifts related to the jet energy scale
            // mostly following
            // https://github.com/cms-nanoAOD/nanoAOD-tools/blob/master/python/postprocessing/modules/jme/jetmetUncertainties.py
            float pt_scale_sf = 1.0;
            if (jes_shift != 0.0) {
                if (jes_shift_sources.at(0) != "HEMIssue") {
                    // Differentiate between single source and combined source
                    // for reduced scheme
                    float JetEnergyScaleShifts_sf;
                    if (JetEnergyScaleShifts.size() == 1) {     
                        if (std::abs(eta_values.at(i)) < 4.7) {
                            JetEnergyScaleShifts_sf=JetEnergyScaleShifts.at(0)->evaluate(
                                {eta_values.at(i),
                                pt_values_corrected.at(i)});}
                        else JetEnergyScaleShifts_sf =1.0;


                        pt_scale_sf =
                            1. + jes_shift * JetEnergyScaleShifts_sf;
                        Logger::get("JetEnergyScaleShift")
                            ->debug("Shifting jet pt by {} for single source "
                                    "with SF {}",
                                    jes_shift, pt_scale_sf);
                    } else {
                        float quad_sum = 0.;
                        for (const auto &evaluator : JetEnergyScaleShifts) {
                            if (std::abs(eta_values.at(i)) < 4.7) {
                                JetEnergyScaleShifts_sf = evaluator->evaluate(
                                    {eta_values.at(i),
                                    pt_values_corrected.at(i)});
                            }
                            else JetEnergyScaleShifts_sf = 1.0;
                            quad_sum +=
                                std::pow(JetEnergyScaleShifts_sf,
                                         2.0);
                        }
                        pt_scale_sf = 1. + jes_shift * std::sqrt(quad_sum);
                        Logger::get("JetEnergyScaleShift")
                            ->debug("Shifting jet pt by {} for multiple "
                                    "sources with SF {}",
                                    jes_shift, pt_scale_sf);
                    }
                }
                // for reference:
                // https://hypernews.cern.ch/HyperNews/CMS/get/JetMET/2000.html
                else if (jes_shift_sources.at(0) == "HEMIssue") {
                    if (jes_shift == (-1.) && pt_values_corrected.at(i) > 15. &&
                        phi_values.at(i) > (-1.57) &&
                        phi_values.at(i) < (-0.87) && ID_values.at(i) == 2) {
                        if (eta_values.at(i) > (-2.5) &&
                            eta_values.at(i) < (-1.3))
                            pt_scale_sf = 0.8;
                        else if (eta_values.at(i) > (-3.) &&
                                 eta_values.at(i) <= (-2.5))
                            pt_scale_sf = 0.65;
                    }
                }
            }
            pt_values_corrected.at(i) *= pt_scale_sf;
            Logger::get("JetEnergyScaleShift")
                ->debug("Shifting jet pt from {} to {} ",
                        pt_values_corrected.at(i) / pt_scale_sf,
                        pt_values_corrected.at(i));

            // if (pt_values_corrected.at(i)>15.0), this
            // correction should be propagated to MET
            // (requirement for type I corrections)


        }
        return pt_values_corrected;
    };
    auto df1 = df.Define(corrected_jet_pt, JetEnergyCorrectionLambda,
                         {jet_pt, jet_eta, jet_phi, jet_area, jet_rawFactor,
                          jet_ID, gen_jet_pt, gen_jet_eta, gen_jet_phi, rho});
    return df1;
}
//////Not applt the JER with the gen-not-match jets
//////Modified by Qianying
ROOT::RDF::RNode
JetPtCorrection_2022_GenMatch(ROOT::RDF::RNode df, const std::string &corrected_jet_pt,
                const std::string &jet_pt, const std::string &jet_eta,
                const std::string &jet_phi, const std::string &jet_area,
                const std::string &jet_rawFactor, const std::string &jet_ID,
                const std::string &gen_jet_pt, const std::string &gen_jet_eta,
                const std::string &gen_jet_phi, const std::string &rho,
                bool reapplyJES,
                const std::vector<std::string> &jes_shift_sources,
                const int &jes_shift, const std::string &jer_shift,
                const std::string &jec_file, const std::string &jer_tag,
                const std::string &jes_tag, const std::string &jec_algo, 
                const std::string &jet_veto_map, const std::string &jet_veto_tag) {
    // identifying jet radius from algorithm
    float jet_dR = 0.4;
    if (jec_algo.find("AK8") != std::string::npos) {
        jet_dR = 0.8;
    }
    // loading JES variations
    std::vector<std::shared_ptr<const correction::Correction>>
        JetEnergyScaleShifts;
    for (const auto &source : jes_shift_sources) {
        // check if any JES shift is chosen
        if (source != "" && source != "HEMIssue") {
            auto JES_source_evaluator =
                correction::CorrectionSet::from_file(jec_file)->at(
                    jes_tag + "_" + source + "_" + jec_algo);
            JetEnergyScaleShifts.push_back(JES_source_evaluator);
        }
    };
    // loading jet energy correction scale factor evaluation function
    // 2022 (with python): >>> list(ceval.compound.keys())
    // ['Summer22_22Sep2023_RunCD_V2_DATA_L1L2L3Res_AK4PFPuppi', 'Summer22_22Sep2023_V2_MC_L1L2L3Res_AK4PFPuppi']
    auto JES_evaluator =
        correction::CorrectionSet::from_file(jec_file)->compound().at(
            jes_tag + "_L1L2L3Res_" + jec_algo);
    auto JetEnergyScaleSF = [JES_evaluator](const float area, const float eta,
                                            const float pt, const float rho) {
        if (std::abs(eta) < 4.7) return JES_evaluator->evaluate({area, eta, pt, rho});
        else return 1.0;
    };
    // loading relative pT resolution evaluation function
    auto JER_resolution_evaluator =
        correction::CorrectionSet::from_file(jec_file)->at(
            jer_tag + "_PtResolution_" + jec_algo);
    auto JetEnergyResolution = [JER_resolution_evaluator](const float eta,
                                                          const float pt,
                                                          const float rho) {
        if (std::abs(eta) < 4.7) return JER_resolution_evaluator->evaluate({eta, pt, rho});
        else return 1.0;
    };
    // loading JER scale factor evaluation function
    auto JER_SF_evaluator = correction::CorrectionSet::from_file(jec_file)->at(
        jer_tag + "_ScaleFactor_" + jec_algo);
    auto JetEnergyResolutionSF =
        [JER_SF_evaluator](const float eta, float pt, const std::string jer_shift) {
            try{ 
                // annoyingly the 2022 EE has 3 inputs, 
                // 2022 post EE has 2 inputs
                if (std::abs(eta) < 4.7) return JER_SF_evaluator->evaluate({eta, pt, jer_shift});    
                else return 1.0;
            }
            catch (const std::exception&) {
            if (std::abs(eta) < 4.7) return JER_SF_evaluator->evaluate({eta,  jer_shift});
            else return 1.0;
        }
    };
    // loading jet veto maps
    auto jet_veto_map_evaluator = correction::CorrectionSet::from_file(jet_veto_map)->at(
        jet_veto_tag);
    auto jet_veto_SF =
        [jet_veto_map_evaluator](const float eta, const float phi) {
            auto tmp_phi  = phi;
            if (phi > 3.141592653589793) tmp_phi = phi - (3.141592653589793 * 2);
            if (phi < -3.141592653589793) tmp_phi = phi + (3.141592653589793 * 2);
            if (std::abs(eta) < 5.19) return jet_veto_map_evaluator->evaluate({ "jetvetomap", eta,  tmp_phi});  // the bin edge is 5.1  , 3.0 should be enough
            else return 1.0;
    };

    // lambda run with dataframe
    auto JetEnergyCorrectionLambda = [reapplyJES, JetEnergyScaleShifts,
                                      JetEnergyScaleSF, JetEnergyResolution,
                                      JetEnergyResolutionSF, jes_shift_sources,
                                      jes_shift, jer_shift, jet_dR,jet_veto_SF ](
                                         const ROOT::RVec<float> &pt_values,
                                         const ROOT::RVec<float> &eta_values,
                                         const ROOT::RVec<float> &phi_values,
                                         const ROOT::RVec<float> &area_values,
                                         const ROOT::RVec<float>
                                             &rawFactor_values,
                                         const ROOT::RVec<UChar_t> &ID_values,
                                         const ROOT::RVec<float> &gen_pt_values,
                                         const ROOT::RVec<float>
                                             &gen_eta_values,
                                         const ROOT::RVec<float>
                                             &gen_phi_values,
                                         const float &rho_value) {
        // random value generator for jet smearing
        TRandom3 randm = TRandom3(12345);
        float pt_veto = -999.0;
        ROOT::RVec<float> pt_values_corrected;
        // // apply jet veto map. If any jet lies within jet veto map, reject the events. 
        // // at the object level it's not straightforward to veto the events, so we return a RVec of pt -999 for all jets 
        
        // Flag to check if any non-zero jet_veto_sf_value is found
        bool non_zero_veto = false;
        // Loop to check if any non-zero jet_veto_sf_value exists
        for (int i = 0; i < pt_values.size(); i++) {

            Logger::get("JetEnergyResolution")
                ->debug("checking jet veto map for index {} ", i);
            float jet_veto_sf_value = jet_veto_SF(eta_values.at(i), phi_values.at(i));
            if (jet_veto_sf_value != 0) {
                non_zero_veto = true;
            }
        }
        if (non_zero_veto) {
            for (int i = 0; i < pt_values.size(); i++) {
                // do jet veto here:         
                // If any non-zero jet_veto_sf_value was found, return a vector filled with -999
                Logger::get("JetEnergyResolution")
                    ->debug("checking jet veto map for index {} ", i);
                pt_values_corrected.push_back(pt_veto);
            }
            return pt_values_corrected;
        }            

        for (int i = 0; i < pt_values.size(); i++) {
            float corr_pt = pt_values.at(i);
            if (reapplyJES) {
                // reapplying the JES correction
                float raw_pt = pt_values.at(i) * (1 - rawFactor_values.at(i));
                float corr = JetEnergyScaleSF(
                    area_values.at(i), eta_values.at(i), raw_pt, rho_value);
                corr_pt = raw_pt * corr;
                Logger::get("JetEnergyScale")
                    ->debug("reapplying JE scale: orig. jet pt {} to raw "
                            "jet pt {} to recorr. jet pt {}",
                            pt_values.at(i), raw_pt, corr_pt);
            }
            pt_values_corrected.push_back(corr_pt);

            // apply jet energy smearing - hybrid method as described in
            // https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetResolution
            float reso = JetEnergyResolution(
                eta_values.at(i), pt_values_corrected.at(i), rho_value);
            float resoSF = JetEnergyResolutionSF(eta_values.at(i), pt_values.at(i),jer_shift);
            Logger::get("JetEnergyResolution")
                ->debug("Calculate JER {}:  SF: {} resolution: {} ", jer_shift,
                        resoSF, reso);
            // gen jet matching algorithm for JER
            ROOT::Math::RhoEtaPhiVectorF jet(
                pt_values_corrected.at(i), eta_values.at(i), phi_values.at(i));
            float genjetpt = -1.0;
            Logger::get("JetEnergyResolution")
                ->debug("Going to smear jet:  Eta: {} Phi: {} ", jet.Eta(),
                        jet.Phi());
            double min_dR = std::numeric_limits<double>::infinity();
            for (int j = 0; j < gen_pt_values.size(); j++) {
                ROOT::Math::RhoEtaPhiVectorF genjet(gen_pt_values.at(j),
                                                    gen_eta_values.at(j),
                                                    gen_phi_values.at(j));
                Logger::get("JetEnergyResolution")
                    ->debug("Checking gen Jet:  Eta: {} Phi: {}", genjet.Eta(),
                            genjet.Phi());
                auto deltaR = ROOT::Math::VectorUtil::DeltaR(jet, genjet);
                if (deltaR > min_dR)
                    continue;
                if (deltaR < (jet_dR / 2.) &&
                    std::abs(pt_values_corrected.at(i) - gen_pt_values.at(j)) <
                        (3.0 * reso * pt_values_corrected.at(i))) {
                    min_dR = deltaR;
                    genjetpt = gen_pt_values.at(j);
                }
            }
            // if jet matches a gen jet scaling method is applied,
            // otherwise stochastic method
            if (genjetpt > 0.0) {
                Logger::get("JetEnergyResolution")
                    ->debug("Found gen jet for hybrid smearing method");
                double shift = (resoSF - 1.0) *
                               (pt_values_corrected.at(i) - genjetpt) /
                               pt_values_corrected.at(i);
                pt_values_corrected.at(i) *= std::max(0.0, 1.0 + shift);
            } 
            //else if (jet.Pt()<50 && std::abs(jet.Eta)>2.5 && std::abs(jet.Eta)<3.0 )
            //{
            //}
            else if ( pt_values_corrected.at(i)> 50 || std::abs(jet.Eta())<2.5 || std::abs(jet.Eta())>3.0  )
            {
            //else {
                Logger::get("JetEnergyResolution")
                    ->debug("No gen jet found. Applying stochastic smearing.");
                double shift = randm.Gaus(0, reso) *
                               std::sqrt(std::max(resoSF * resoSF - 1., 0.0));
                pt_values_corrected.at(i) *= std::max(0.0, 1.0 + shift);
            }
            Logger::get("JetEnergyResolution")
                ->debug("Shifting jet pt from {} to {} ", corr_pt,
                        pt_values_corrected.at(i));

            // apply uncertainty shifts related to the jet energy scale
            // mostly following
            // https://github.com/cms-nanoAOD/nanoAOD-tools/blob/master/python/postprocessing/modules/jme/jetmetUncertainties.py
            float pt_scale_sf = 1.0;
            if (jes_shift != 0.0) {
                if (jes_shift_sources.at(0) != "HEMIssue") {
                    // Differentiate between single source and combined source
                    // for reduced scheme
                    float JetEnergyScaleShifts_sf;
                    if (JetEnergyScaleShifts.size() == 1) {     
                        if (std::abs(eta_values.at(i)) < 4.7) {
                            JetEnergyScaleShifts_sf=JetEnergyScaleShifts.at(0)->evaluate(
                                {eta_values.at(i),
                                pt_values_corrected.at(i)});}
                        else JetEnergyScaleShifts_sf =1.0;


                        pt_scale_sf =
                            1. + jes_shift * JetEnergyScaleShifts_sf;
                        Logger::get("JetEnergyScaleShift")
                            ->debug("Shifting jet pt by {} for single source "
                                    "with SF {}",
                                    jes_shift, pt_scale_sf);
                    } else {
                        float quad_sum = 0.;
                        for (const auto &evaluator : JetEnergyScaleShifts) {
                            if (std::abs(eta_values.at(i)) < 4.7) {
                                JetEnergyScaleShifts_sf = evaluator->evaluate(
                                    {eta_values.at(i),
                                    pt_values_corrected.at(i)});
                            }
                            else JetEnergyScaleShifts_sf = 1.0;
                            quad_sum +=
                                std::pow(JetEnergyScaleShifts_sf,
                                         2.0);
                        }
                        pt_scale_sf = 1. + jes_shift * std::sqrt(quad_sum);
                        Logger::get("JetEnergyScaleShift")
                            ->debug("Shifting jet pt by {} for multiple "
                                    "sources with SF {}",
                                    jes_shift, pt_scale_sf);
                    }
                }
                // for reference:
                // https://hypernews.cern.ch/HyperNews/CMS/get/JetMET/2000.html
                else if (jes_shift_sources.at(0) == "HEMIssue") {
                    if (jes_shift == (-1.) && pt_values_corrected.at(i) > 15. &&
                        phi_values.at(i) > (-1.57) &&
                        phi_values.at(i) < (-0.87) && ID_values.at(i) == 2) {
                        if (eta_values.at(i) > (-2.5) &&
                            eta_values.at(i) < (-1.3))
                            pt_scale_sf = 0.8;
                        else if (eta_values.at(i) > (-3.) &&
                                 eta_values.at(i) <= (-2.5))
                            pt_scale_sf = 0.65;
                    }
                }
            }
            pt_values_corrected.at(i) *= pt_scale_sf;
            Logger::get("JetEnergyScaleShift")
                ->debug("Shifting jet pt from {} to {} ",
                        pt_values_corrected.at(i) / pt_scale_sf,
                        pt_values_corrected.at(i));

            // if (pt_values_corrected.at(i)>15.0), this
            // correction should be propagated to MET
            // (requirement for type I corrections)


        }
        return pt_values_corrected;
    };
    auto df1 = df.Define(corrected_jet_pt, JetEnergyCorrectionLambda,
                         {jet_pt, jet_eta, jet_phi, jet_area, jet_rawFactor,
                          jet_ID, gen_jet_pt, gen_jet_eta, gen_jet_phi, rho});
    return df1;
}
////jet veto map
ROOT::RDF::RNode
JetVetoMap_run3(ROOT::RDF::RNode df, const std::string &jetVetoMap,
                const std::string &jet_pt, const std::string &jet_eta,
                const std::string &jet_phi, const std::string &jet_area,
                const std::string &jet_rawFactor, const std::string &jet_ID,
                const std::string &jet_veto_map, const std::string &jet_veto_tag) {
    // identifying jet radius from algorithm
    //float jet_dR = 0.4;
    //if (jec_algo.find("AK8") != std::string::npos) {
    //    jet_dR = 0.8;
    //}
    // loading jet veto maps
    auto jet_veto_map_evaluator = correction::CorrectionSet::from_file(jet_veto_map)->at(
        jet_veto_tag);
    auto jet_veto_SF =
        [jet_veto_map_evaluator](const float eta, const float phi) {
            auto tmp_phi  = phi;
            if (phi > 3.141592653589793) tmp_phi = phi - (3.141592653589793 * 2);
            if (phi < -3.141592653589793) tmp_phi = phi + (3.141592653589793 * 2);
            if (std::abs(eta) < 5.19) return jet_veto_map_evaluator->evaluate({ "jetvetomap", eta,  tmp_phi});  // the bin edge is 5.1  , 3.0 should be enough
            else return 1.0;
    };

    // lambda run with dataframe
    auto JetEnergyCorrectionLambda = [jet_veto_SF ](
                                         const ROOT::RVec<float> &pt_values,
                                         const ROOT::RVec<float> &eta_values,
                                         const ROOT::RVec<float> &phi_values
                                      ){
        // random value generator for jet smearing
        TRandom3 randm = TRandom3(12345);
        float pt_veto = -999.0;
        ROOT::RVec<float> pt_values_corrected;
        // // apply jet veto map. If any jet lies within jet veto map, reject the events. 
        // // at the object level it's not straightforward to veto the events, so we return a RVec of pt -999 for all jets 
        
        // Flag to check if any non-zero jet_veto_sf_value is found
        bool non_zero_veto = false;
        // Loop to check if any non-zero jet_veto_sf_value exists
        for (int i = 0; i < pt_values.size(); i++) {

            Logger::get("JetEnergyResolution")
                ->debug("checking jet veto map for index {} ", i);
            float jet_veto_sf_value = jet_veto_SF(eta_values.at(i), phi_values.at(i));
            if (jet_veto_sf_value != 0) {
                non_zero_veto = true;
            }
        }
        if (non_zero_veto) {
            for (int i = 0; i < pt_values.size(); i++) {
                // do jet veto here:         
                // If any non-zero jet_veto_sf_value was found, return a vector filled with -999
                Logger::get("JetEnergyResolution")
                    ->debug("checking jet veto map for index {} ", i);
                pt_values_corrected.push_back(pt_veto);
            }
            return pt_values_corrected;
        }            
    };
    auto df1 = df.Define(jetVetoMap, JetEnergyCorrectionLambda,
                         {jet_pt, jet_eta, jet_phi});
    return df1;
}
////finished jetvetomap
//jetvetomap data
//ROOT::RDF::RNode
//JetPtCorrection_data_2022_jetvetomap(ROOT::RDF::RNode df, const std::string &corrected_jet_pt,
//                     const std::string &jet_pt, const std::string &jet_eta, const std::string &jet_phi, 
//                     const std::string &jet_area,
//                     const std::string &jet_rawFactor,
//                     const std::string &jet_veto_map, const std::string &jet_veto_tag) {
//    
//    // loading jet veto maps
//    auto jet_veto_map_evaluator = correction::CorrectionSet::from_file(jet_veto_map)->at(
//        jet_veto_tag);
//    auto jet_veto_SF =
//        [jet_veto_map_evaluator](const float eta, const float phi) {
//            auto tmp_phi  = phi;
//            if (phi > 3.141592653589793) tmp_phi = phi - (3.141592653589793 * 2);
//            if (phi < -3.141592653589793) tmp_phi = phi + (3.141592653589793 * 2);
//            if (std::abs(eta) < 5.1) return jet_veto_map_evaluator->evaluate({ "jetvetomap", eta,  tmp_phi});
//            else return 1.0;
//    };
//
//
//        // lambda run with dataframe
//        auto JetEnergyCorrectionLambda =
//            [jet_veto_SF](const ROOT::RVec<float> &pt_values,
//                               const ROOT::RVec<float> &eta_values,
//                               const ROOT::RVec<float> &phi_values,
//                               const ROOT::RVec<float> &area_values,
//                               const ROOT::RVec<float> &rawFactor_values
//                               ) {
//                ROOT::RVec<float> pt_values_corrected;
//                // apply jet veto map. If any jet lies within jet veto map, reject the events. 
//                // at the object level it's not straightforward to veto the events, so we return a RVec of pt -10 for all jets
//                
//                // Flag to check if any non-zero jet_veto_sf_value is found
//                bool non_zero_veto = false;
//                // Loop to check if any non-zero jet_veto_sf_value exists
//                for (int i = 0; i < pt_values.size(); i++) {
//                    float jet_veto_sf_value=0;
//                    if (std::abs(eta_values.at(i)) < 5.19)  jet_veto_sf_value= jet_veto_SF(eta_values.at(i), phi_values.at(i));
//                    else jet_veto_sf_value =0;
//                    if (jet_veto_sf_value != 0) {
//                        non_zero_veto = true;
//                        break;  // No need to continue if we already found one non-zero value
//                    }
//                }
//                // If any non-zero jet_veto_sf_value was found, return a vector filled with -999
//                if (non_zero_veto) {
//                    for (int i = 0; i < pt_values.size(); i++) {
//                        pt_values_corrected.push_back(-999.0);
//                    }
//                    return pt_values_corrected;
//                } 
//
//                for (int i = 0; i < pt_values.size(); i++) {
//                    float corr_pt = pt_values.at(i);
//                    pt_values_corrected.push_back(corr_pt);
//                    // if (pt_values_corrected.at(i)>15.0), this
//                    // correction should be propagated to MET
//                    // (requirement for type I corrections)
//                }
//                return pt_values_corrected;
//            };
//        auto df1 = df.Define(corrected_jet_pt, JetEnergyCorrectionLambda,
//                             {jet_pt, jet_eta, jet_phi, jet_area, jet_rawFactor});
//        return df1;
//    } else {
//            // we still need to do jet veto
//           auto JetEnergyCorrectionLambda =
//            [jet_veto_SF](const ROOT::RVec<float> &pt_values,
//                               const ROOT::RVec<float> &eta_values,
//                               const ROOT::RVec<float> &phi_values,
//                               const ROOT::RVec<float> &area_values,
//                               const ROOT::RVec<float> &rawFactor_values
//                               ) {
//                ROOT::RVec<float> pt_values_corrected;
//                // apply jet veto map. If any jet lies within jet veto map, reject the events. 
//                // at the object level it's not straightforward to veto the events, so we return a RVec of pt -10 for all jets
//                
//                // Flag to check if any non-zero jet_veto_sf_value is found
//                bool non_zero_veto = false;
//                // Loop to check if any non-zero jet_veto_sf_value exists
//                for (int i = 0; i < pt_values.size(); i++) {
//                    float jet_veto_sf_value=0;
//                    if (std::abs(eta_values.at(i)) < 5.19)  jet_veto_sf_value= jet_veto_SF(eta_values.at(i), phi_values.at(i));
//                    else jet_veto_sf_value =0;
//                    if (jet_veto_sf_value != 0) {
//                        non_zero_veto = true;
//                        break;  // No need to continue if we already found one non-zero value
//                    }
//                }
//                // If any non-zero jet_veto_sf_value was found, return a vector filled with -999
//                if (non_zero_veto) {
//                    for (int i = 0; i < pt_values.size(); i++) {
//                        pt_values_corrected.push_back(-999.0);
//                    }
//                    return pt_values_corrected;
//                } 
//
//                for (int i = 0; i < pt_values.size(); i++) {
//                    pt_values_corrected.push_back(pt_values.at(i));
//                }
//                return pt_values_corrected;
//            };
//        auto df1 = df.Define(corrected_jet_pt, JetEnergyCorrectionLambda,
//                             {jet_pt, jet_eta, jet_phi, jet_area, jet_rawFactor});
//        return df1;        
//        // auto df1 = df.Define(
//        //     corrected_jet_pt,
//        //     [](const ROOT::RVec<float> &pt_values) { return pt_values; },
//        //     {jet_pt});
//        // return df1;
//
//
//    }
//}
//finish jetvetomap data
//////finished modification
ROOT::RDF::RNode
JetPtCorrection_data_2022(ROOT::RDF::RNode df, const std::string &corrected_jet_pt,
                     const std::string &jet_pt, const std::string &jet_eta, const std::string &jet_phi, 
                     const std::string &jet_area,
                     const std::string &jet_rawFactor, //const std::string &rho,
                     const std::string &jec_file, const std::string &jes_tag,
                     const std::string &jec_algo, 
                     const std::string &jet_veto_map, const std::string &jet_veto_tag) {
    
    // loading jet veto maps
    auto jet_veto_map_evaluator = correction::CorrectionSet::from_file(jet_veto_map)->at(
        jet_veto_tag);
    auto jet_veto_SF =
        [jet_veto_map_evaluator](const float eta, const float phi) {
            auto tmp_phi  = phi;
            if (phi > 3.141592653589793) tmp_phi = phi - (3.141592653589793 * 2);
            if (phi < -3.141592653589793) tmp_phi = phi + (3.141592653589793 * 2);
            if (std::abs(eta) < 5.1) return jet_veto_map_evaluator->evaluate({ "jetvetomap", eta,  tmp_phi});
            else return 1.0;
    };

    if (jes_tag != "") {
        // loading jet energy correction scale factor evaluation function
        auto JES_evaluator =
            correction::CorrectionSet::from_file(jec_file)->compound().at(
                jes_tag + "_L1L2L3Res_" + jec_algo);
        Logger::get("JetEnergyScaleData")
            ->debug("file: {}, function {}", jec_file,
                    (jes_tag + "_L1L2L3Res_" + jec_algo));
        auto JetEnergyScaleSF = [JES_evaluator](const float area,
                                                const float eta, const float pt//, const float rho
                                                ) {
            //if (std::abs(eta) < 4.7) return JES_evaluator->evaluate({area, eta, pt, rho});
            if (std::abs(eta) < 4.7) return JES_evaluator->evaluate({area, eta, pt});
            else return 1.0;
        };

        // lambda run with dataframe
        auto JetEnergyCorrectionLambda =
            [jes_tag,
             JetEnergyScaleSF, jet_veto_SF](const ROOT::RVec<float> &pt_values,
                               const ROOT::RVec<float> &eta_values,
                               const ROOT::RVec<float> &phi_values,
                               const ROOT::RVec<float> &area_values,
                               const ROOT::RVec<float> &rawFactor_values//,
                               //const float &rho_value
                               ) {
                ROOT::RVec<float> pt_values_corrected;
                // apply jet veto map. If any jet lies within jet veto map, reject the events. 
                // at the object level it's not straightforward to veto the events, so we return a RVec of pt -10 for all jets
                
                // Flag to check if any non-zero jet_veto_sf_value is found
                bool non_zero_veto = false;
                // Loop to check if any non-zero jet_veto_sf_value exists
                for (int i = 0; i < pt_values.size(); i++) {
                    float jet_veto_sf_value=0;
                    if (std::abs(eta_values.at(i)) < 5.19)  jet_veto_sf_value= jet_veto_SF(eta_values.at(i), phi_values.at(i));
                    else jet_veto_sf_value =0;
                    if (jet_veto_sf_value != 0) {
                        non_zero_veto = true;
                        break;  // No need to continue if we already found one non-zero value
                    }
                }
                // If any non-zero jet_veto_sf_value was found, return a vector filled with -999
                if (non_zero_veto) {
                    for (int i = 0; i < pt_values.size(); i++) {
                        pt_values_corrected.push_back(-999.0);
                    }
                    return pt_values_corrected;
                } 

                for (int i = 0; i < pt_values.size(); i++) {
                    float corr_pt = pt_values.at(i);
                    if (jes_tag != "") {
                        // reapplying the JES correction
                        float raw_pt =
                            pt_values.at(i) * (1 - rawFactor_values.at(i));
                        float corr = JetEnergyScaleSF(area_values.at(i),
                                                      eta_values.at(i), raw_pt//, rho_value
                                                      );
                        corr_pt = raw_pt * corr;
                        Logger::get("JetEnergyScaleData")
                            ->debug("reapplying JE scale for data: orig. jet "
                                    "pt {} to raw "
                                    "jet pt {} to recorr. jet pt {}",
                                    pt_values.at(i), raw_pt, corr_pt);
                    }
                    pt_values_corrected.push_back(corr_pt);
                    // if (pt_values_corrected.at(i)>15.0), this
                    // correction should be propagated to MET
                    // (requirement for type I corrections)
                }
                return pt_values_corrected;
            };
        auto df1 = df.Define(corrected_jet_pt, JetEnergyCorrectionLambda,
                             //{jet_pt, jet_eta, jet_phi, jet_area, jet_rawFactor, rho});
                             {jet_pt, jet_eta, jet_phi, jet_area, jet_rawFactor});
        return df1;
    } else {
            // we still need to do jet veto
           auto JetEnergyCorrectionLambda =
            [jes_tag, jet_veto_SF](const ROOT::RVec<float> &pt_values,
                               const ROOT::RVec<float> &eta_values,
                               const ROOT::RVec<float> &phi_values,
                               const ROOT::RVec<float> &area_values,
                               const ROOT::RVec<float> &rawFactor_values//, const float &rho_value
                               ) {
                ROOT::RVec<float> pt_values_corrected;
                // apply jet veto map. If any jet lies within jet veto map, reject the events. 
                // at the object level it's not straightforward to veto the events, so we return a RVec of pt -10 for all jets
                
                // Flag to check if any non-zero jet_veto_sf_value is found
                bool non_zero_veto = false;
                // Loop to check if any non-zero jet_veto_sf_value exists
                for (int i = 0; i < pt_values.size(); i++) {
                    float jet_veto_sf_value=0;
                    if (std::abs(eta_values.at(i)) < 5.19)  jet_veto_sf_value= jet_veto_SF(eta_values.at(i), phi_values.at(i));
                    else jet_veto_sf_value =0;
                    if (jet_veto_sf_value != 0) {
                        non_zero_veto = true;
                        break;  // No need to continue if we already found one non-zero value
                    }
                }
                // If any non-zero jet_veto_sf_value was found, return a vector filled with -999
                if (non_zero_veto) {
                    for (int i = 0; i < pt_values.size(); i++) {
                        pt_values_corrected.push_back(-999.0);
                    }
                    return pt_values_corrected;
                } 

                for (int i = 0; i < pt_values.size(); i++) {
                    pt_values_corrected.push_back(pt_values.at(i));
                }
                return pt_values_corrected;
            };
        auto df1 = df.Define(corrected_jet_pt, JetEnergyCorrectionLambda,
                             //{jet_pt, jet_eta, jet_phi, jet_area, jet_rawFactor, rho});
                             {jet_pt, jet_eta, jet_phi, jet_area, jet_rawFactor});
        return df1;        
        // auto df1 = df.Define(
        //     corrected_jet_pt,
        //     [](const ROOT::RVec<float> &pt_values) { return pt_values; },
        //     {jet_pt});
        // return df1;


    }
}
////ahhhhhh

/// Function to correct jet energy for data
///
/// \param[in] df the input dataframe
/// \param[out] corrected_jet_pt the name of the corrected jet pts
/// \param[in] jet_pt name of the input jet pts
/// \param[in] jet_eta name of the jet etas
/// \param[in] jet_area name of the jet catchment area
/// \param[in] jet_rawFactor name of the raw factor for jet pt
/// \param[in] rho name of the pileup density
/// \param[in] jec_file path to the file with jet energy correction information
/// \param[in] jes_tag era dependent tag for JES correction
/// \param[in] jec_algo algorithm used for jets e.g. AK4PFchs
///
/// \return a dataframe containing the modified jet pts
ROOT::RDF::RNode
JetPtCorrection_data(ROOT::RDF::RNode df, const std::string &corrected_jet_pt,
                     const std::string &jet_pt, const std::string &jet_eta,
                     const std::string &jet_area,
                     const std::string &jet_rawFactor, const std::string &rho,
                     const std::string &jec_file, const std::string &jes_tag,
                     const std::string &jec_algo) {
    if (jes_tag != "") {
        // loading jet energy correction scale factor evaluation function
        auto JES_evaluator =
            correction::CorrectionSet::from_file(jec_file)->compound().at(
                jes_tag + "_L1L2L3Res_" + jec_algo);
        Logger::get("JetEnergyScaleData")
            ->debug("file: {}, function {}", jec_file,
                    (jes_tag + "_L1L2L3Res_" + jec_algo));
        auto JetEnergyScaleSF = [JES_evaluator](const float area,
                                                const float eta, const float pt,
                                                const float rho) {
            return JES_evaluator->evaluate({area, eta, pt, rho});
        };

        // lambda run with dataframe
        auto JetEnergyCorrectionLambda =
            [jes_tag,
             JetEnergyScaleSF](const ROOT::RVec<float> &pt_values,
                               const ROOT::RVec<float> &eta_values,
                               const ROOT::RVec<float> &area_values,
                               const ROOT::RVec<float> &rawFactor_values,
                               const float &rho_value) {
                ROOT::RVec<float> pt_values_corrected;
                for (int i = 0; i < pt_values.size(); i++) {
                    float corr_pt = pt_values.at(i);
                    if (jes_tag != "") {
                        // reapplying the JES correction
                        float raw_pt =
                            pt_values.at(i) * (1 - rawFactor_values.at(i));
                        float corr = JetEnergyScaleSF(area_values.at(i),
                                                      eta_values.at(i), raw_pt,
                                                      rho_value);
                        corr_pt = raw_pt * corr;
                        Logger::get("JetEnergyScaleData")
                            ->debug("reapplying JE scale for data: orig. jet "
                                    "pt {} to raw "
                                    "jet pt {} to recorr. jet pt {}",
                                    pt_values.at(i), raw_pt, corr_pt);
                    }
                    pt_values_corrected.push_back(corr_pt);
                    // if (pt_values_corrected.at(i)>15.0), this
                    // correction should be propagated to MET
                    // (requirement for type I corrections)
                }
                return pt_values_corrected;
            };
        auto df1 = df.Define(corrected_jet_pt, JetEnergyCorrectionLambda,
                             {jet_pt, jet_eta, jet_area, jet_rawFactor, rho});
        return df1;
    } else {
        auto df1 = df.Define(
            corrected_jet_pt,
            [](const ROOT::RVec<float> &pt_values) { return pt_values; },
            {jet_pt});
        return df1;
    }
}

/// Function to select jets passing a ID requirement, using
/// basefunctions::FilterMin
///
/// \param[in] df the input dataframe
/// \param[in] quantity name of the rawID column in the NanoAOD
/// \param[out] maskname the name of the mask to be added as column to the
/// dataframe
/// \param[in] idThreshold minimal ID value
///
/// \return a dataframe containing the new mask
ROOT::RDF::RNode CutRawID(ROOT::RDF::RNode df, const std::string &quantity,
                          const std::string &maskname,
                          const float &idThreshold) {
    auto df1 =
        df.Define(maskname, basefunctions::FilterMin(idThreshold), {quantity});
    return df1;
}
/// Function to select jets failing a ID requirement, using
/// basefunctions::FilterMax
///
/// \param[in] df the input dataframe
/// \param[in] quantity name of the rawID column in the NanoAOD
/// \param[out] maskname the name of the mask to be added as column to the
/// dataframe
/// \param[in] idThreshold maximal ID value
///
/// \return a dataframe containing the new mask
ROOT::RDF::RNode AntiCutRawID(ROOT::RDF::RNode df, const std::string &quantity,
                              const std::string &maskname,
                              const float &idThreshold) {
    auto df1 =
        df.Define(maskname, basefunctions::FilterMax(idThreshold), {quantity});
    return df1;
}
} // end namespace jet
} // end namespace physicsobject

namespace quantities {
namespace jet {
/// Function to determine number of jets in a jet collection
///
/// \param[in] df the input dataframe
/// \param[out] outputname the name of the produced quantity
/// \param[in] jetcollection name of the vector that contains jet indices of the
/// jets belonging to the collection, its length constitutes the output quantity
///
/// \return a dataframe containing the number of jets in the jet collection
ROOT::RDF::RNode NumberOfJets(ROOT::RDF::RNode df,
                              const std::string &outputname,
                              const std::string &jetcollection) {
    return df.Define(outputname,
                     [](const ROOT::RVec<int> &jetcollection) {
                         Logger::get("NumberOfJets")->debug("Counting jets");
                         Logger::get("NumberOfJets")
                             ->debug("NJets {}", jetcollection.size());
                         return (int)jetcollection.size();
                     },
                     {jetcollection});
}
/// Function to writeout the value of the btagger for a jet. The tag value is
/// identified via the discriminant of e.g. the DeepJet tagger from nanoAOD
///
/// \param[in] df the input dataframe
/// \param[out] outputname the name of the produced quantity
/// \param[in] btagcolumn name of the column that contains btag values of
/// the jets
/// \param[in] jetcollection name of the vector that contains jet indices of the
/// jets belonging to the collection, its length constitutes the output quantity
/// \param position The position in the jet collection vector, which is used to
/// store the index of the particle in the particle quantity vectors.
///
/// \returns a dataframe with the new column

ROOT::RDF::RNode btagValue(ROOT::RDF::RNode df, const std::string &outputname,
                           const std::string &btagcolumn,
                           const std::string &jetcollection,
                           const int &position) {
    return df.Define(outputname,
                     [position](const ROOT::RVec<float> &btagvalues,
                                const ROOT::RVec<int> &jetcollection) {
                         float btagValue = default_float;
                         try {
                             const int index = jetcollection.at(position);
                             btagValue = btagvalues.at(index);
                         } catch (const std::out_of_range &e) {
                         }
                         return btagValue;
                     },
                     {btagcolumn, jetcollection});
}
/// Function to writeout the hadron flavor for a jet.
///
/// \param[in] df the input dataframe
/// \param[out] outputname the name of the produced quantity
/// \param[in] flavorcolumn name of the column that contains flavor values of
/// the jets
/// \param[in] jetcollection name of the vector that contains jet indices of the
/// jets belonging to the collection, its length constitutes the output quantity
/// \param position The position in the jet collection vector, which is used to
/// store the index of the particle in the particle quantity vectors.
///
/// \returns a dataframe with the new column

ROOT::RDF::RNode flavor(ROOT::RDF::RNode df, const std::string &outputname,
                        const std::string &flavorcolumn,
                        const std::string &jetcollection, const int &position) {
    return df.Define(outputname,
                     [position](const ROOT::RVec<int> &flavorvalues,
                                const ROOT::RVec<int> &jetcollection) {
                         int flavorValue = default_int;
                         const int index =
                             jetcollection.at(position, default_int);
                         flavorValue = flavorvalues.at(index, default_int);
                         return flavorValue;
                     },
                     {flavorcolumn, jetcollection});
}
} // end namespace jet
} // end namespace quantities
#endif /* GUARDJETS_H */
