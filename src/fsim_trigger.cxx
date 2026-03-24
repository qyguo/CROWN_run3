#ifndef GUARD_FSIM_TRIGGER_H
#define GUARD_FSIM_TRIGGER_H

#include "../include/utility/Logger.hxx"
#include "ROOT/RDataFrame.hxx"
#include "correction.h"
#include <Math/Vector4D.h>
#include <algorithm>
#include <cmath>
#include <random>
#include <stdexcept>
#include <string>

namespace trigger {
namespace {

double clampEfficiency(double eff) {
    if (!std::isfinite(eff))
        return 0.0;
    return std::clamp(eff, 0.0, 1.0);
}

uint64_t buildEventSeed(const UInt_t run, const UInt_t luminosityBlock,
                        const ULong64_t event, const uint64_t salt) {
    uint64_t seed = static_cast<uint64_t>(event);
    seed ^= static_cast<uint64_t>(run) << 32;
    seed ^= static_cast<uint64_t>(luminosityBlock) << 16;
    seed ^= salt;
    return seed;
}

double muonEfficiency(
    const std::shared_ptr<const correction::Correction> &evaluator,
    const ROOT::Math::PtEtaPhiMVector &particle, const float pt_cut,
    const float eta_cut) {
    if (particle.pt() < pt_cut)
        return 0.0;
    if (std::abs(particle.eta()) > eta_cut)
        return 0.0;

    const double eff = evaluator->evaluate({std::abs(particle.eta()),
                                            static_cast<double>(particle.pt())});
    return clampEfficiency(eff);
}

std::shared_ptr<const correction::Correction>
loadEfficiencyEvaluator(const std::string &eff_json,
                        const std::string &eff_correction) {
    Logger::get("fsim_trigger")
        ->info("Loading fsim trigger efficiency: file='{}', correction='{}'",
               eff_json, eff_correction);
    return correction::CorrectionSet::from_file(eff_json)->at(eff_correction);
}

bool decideTrigger(const double trigger_probability, const UInt_t run,
                   const UInt_t luminosityBlock, const ULong64_t event,
                   const uint64_t salt) {
    std::mt19937_64 rng(buildEventSeed(run, luminosityBlock, event, salt));
    std::uniform_real_distribution<double> uniform01(0.0, 1.0);
    const double random_number = uniform01(rng);
    return random_number < trigger_probability;
}

} // namespace

ROOT::RDF::RNode GenerateDoubleTriggerFlagFromEfficiency(
    ROOT::RDF::RNode df, const std::string &triggerflag_name,
    const std::string &run_column, const std::string &luminosityBlock_column,
    const std::string &event_column, const std::string &particle1_p4,
    const std::string &particle2_p4, const std::string &eff_json,
    const std::string &eff_correction, const float &p1_pt_cut,
    const float &p2_pt_cut, const float &p1_eta_cut, const float &p2_eta_cut) {

    auto evaluator = loadEfficiencyEvaluator(eff_json, eff_correction);

    auto fsim_trigger = [evaluator, p1_pt_cut, p2_pt_cut, p1_eta_cut, p2_eta_cut](
                            const UInt_t &run, const UInt_t &luminosityBlock,
                            const ULong64_t &event,
                            const ROOT::Math::PtEtaPhiMVector &particle1,
                            const ROOT::Math::PtEtaPhiMVector &particle2) {
        const double eff_1 =
            muonEfficiency(evaluator, particle1, p1_pt_cut, p1_eta_cut);
        const double eff_2 =
            muonEfficiency(evaluator, particle2, p2_pt_cut, p2_eta_cut);
        const double trigger_probability = 1.0 - (1.0 - eff_1) * (1.0 - eff_2);

        Logger::get("fsim_trigger")
            ->debug("double-lepton eff1={}, eff2={}, probability={}", eff_1,
                    eff_2, trigger_probability);

        return decideTrigger(trigger_probability, run, luminosityBlock, event,
                             0x11ULL);
    };

    return df.Define(triggerflag_name, fsim_trigger,
                     {run_column, luminosityBlock_column, event_column,
                      particle1_p4, particle2_p4});
}

ROOT::RDF::RNode GenerateTripleTriggerFlagFromEfficiency(
    ROOT::RDF::RNode df, const std::string &triggerflag_name,
    const std::string &run_column, const std::string &luminosityBlock_column,
    const std::string &event_column, const std::string &particle1_p4,
    const std::string &particle2_p4, const std::string &particle3_p4,
    const std::string &eff_json, const std::string &eff_correction,
    const float &p1_pt_cut, const float &p2_pt_cut, const float &p3_pt_cut,
    const float &p1_eta_cut, const float &p2_eta_cut, const float &p3_eta_cut) {

    auto evaluator = loadEfficiencyEvaluator(eff_json, eff_correction);

    auto fsim_trigger =
        [evaluator, p1_pt_cut, p2_pt_cut, p3_pt_cut, p1_eta_cut, p2_eta_cut,
         p3_eta_cut](const UInt_t &run, const UInt_t &luminosityBlock,
                     const ULong64_t &event,
                     const ROOT::Math::PtEtaPhiMVector &particle1,
                     const ROOT::Math::PtEtaPhiMVector &particle2,
                     const ROOT::Math::PtEtaPhiMVector &particle3) {
            const double eff_1 =
                muonEfficiency(evaluator, particle1, p1_pt_cut, p1_eta_cut);
            const double eff_2 =
                muonEfficiency(evaluator, particle2, p2_pt_cut, p2_eta_cut);
            const double eff_3 =
                muonEfficiency(evaluator, particle3, p3_pt_cut, p3_eta_cut);
            const double trigger_probability =
                1.0 - (1.0 - eff_1) * (1.0 - eff_2) * (1.0 - eff_3);

            Logger::get("fsim_trigger")
                ->debug("triple-lepton eff=({}, {}, {}), probability={}",
                        eff_1, eff_2, eff_3, trigger_probability);

            return decideTrigger(trigger_probability, run, luminosityBlock,
                                 event, 0x21ULL);
        };

    return df.Define(triggerflag_name, fsim_trigger,
                     {run_column, luminosityBlock_column, event_column,
                      particle1_p4, particle2_p4, particle3_p4});
}

ROOT::RDF::RNode GenerateQuadTriggerFlagFromEfficiency(
    ROOT::RDF::RNode df, const std::string &triggerflag_name,
    const std::string &run_column, const std::string &luminosityBlock_column,
    const std::string &event_column, const std::string &particle1_p4,
    const std::string &particle2_p4, const std::string &particle3_p4,
    const std::string &particle4_p4, const std::string &eff_json,
    const std::string &eff_correction, const float &p1_pt_cut,
    const float &p2_pt_cut, const float &p3_pt_cut, const float &p4_pt_cut,
    const float &p1_eta_cut, const float &p2_eta_cut, const float &p3_eta_cut,
    const float &p4_eta_cut) {

    auto evaluator = loadEfficiencyEvaluator(eff_json, eff_correction);

    auto fsim_trigger = [evaluator, p1_pt_cut, p2_pt_cut, p3_pt_cut, p4_pt_cut,
                         p1_eta_cut, p2_eta_cut, p3_eta_cut, p4_eta_cut](
                            const UInt_t &run, const UInt_t &luminosityBlock,
                            const ULong64_t &event,
                            const ROOT::Math::PtEtaPhiMVector &particle1,
                            const ROOT::Math::PtEtaPhiMVector &particle2,
                            const ROOT::Math::PtEtaPhiMVector &particle3,
                            const ROOT::Math::PtEtaPhiMVector &particle4) {
        const double eff_1 =
            muonEfficiency(evaluator, particle1, p1_pt_cut, p1_eta_cut);
        const double eff_2 =
            muonEfficiency(evaluator, particle2, p2_pt_cut, p2_eta_cut);
        const double eff_3 =
            muonEfficiency(evaluator, particle3, p3_pt_cut, p3_eta_cut);
        const double eff_4 =
            muonEfficiency(evaluator, particle4, p4_pt_cut, p4_eta_cut);
        const double trigger_probability =
            1.0 - (1.0 - eff_1) * (1.0 - eff_2) * (1.0 - eff_3) *
                      (1.0 - eff_4);

        Logger::get("fsim_trigger")
            ->debug("quad-lepton eff=({}, {}, {}, {}), probability={}", eff_1,
                    eff_2, eff_3, eff_4, trigger_probability);

        return decideTrigger(trigger_probability, run, luminosityBlock, event,
                             0x41ULL);
    };

    return df.Define(triggerflag_name, fsim_trigger,
                     {run_column, luminosityBlock_column, event_column,
                      particle1_p4, particle2_p4, particle3_p4, particle4_p4});
}

} // namespace trigger

#endif /* GUARD_FSIM_TRIGGER_H */
