from __future__ import annotations  # needed for type annotations in > python 3.7

from typing import List

from .producers import event as event
from .producers import triggers as triggers
from .producers import genparticles as genparticles
from .producers import muons as muons
from .producers import fsrPhoton as fsrPhoton
from .producers import jets as jets
from .producers import scalefactors as scalefactors
# add by botao
from .producers import lepton as lepton
from .producers import electrons as electrons
from .producers import met as met
from .producers import p4 as p4
from .producers import cr as cr
from .producers import fatjets as fatjets
# end 
from .quantities import nanoAOD as nanoAOD
from .quantities import output as q
from code_generation.configuration import Configuration
from code_generation.modifiers import EraModifier
from code_generation.rules import RemoveProducer, AppendProducer
from code_generation.systematics import SystematicShift


def build_config(
    era: str,
    sample: str,
    scopes: List[str],
    shifts: List[str],
    available_sample_types: List[str],
    available_eras: List[str],
    available_scopes: List[str],
):

    configuration = Configuration(
        era,
        sample,
        scopes,
        shifts,
        available_sample_types,
        available_eras,
        available_scopes,
    )

    configuration.add_config_parameters(
        "global",
        {
            "PU_reweighting_file_hist": EraModifier(
                {
                    "2016preVFP": "data/pileup/Data_Pileup_2016_271036-284044_13TeVMoriond17_23Sep2016ReReco_69p2mbMinBiasXS.root",
                    "2016postVFP": "data/pileup/Data_Pileup_2016_271036-284044_13TeVMoriond17_23Sep2016ReReco_69p2mbMinBiasXS.root",
                    "2017": "data/pileup/Data_Pileup_2017_294927-306462_13TeVSummer17_PromptReco_69p2mbMinBiasXS.root",
                    "2018": "data/pileup/Data_Pileup_2018_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18.root",
                    # "2022": "not/available/yet",
                    #"2022": "data/pileup/Data_Pileup_2018_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18.root",
                    #'2022': In all those directories you will find (as indicated in the file name) histograms corresponding to the following values of the pp inelastic cross section: 69200 ub (recommended central value), 66000 ub (central value - 4.6%), 72400 ub (central value + 4.6%), 80000 ub (conventional value used for the public plots, agreed with ATLAS years ago).
                    #pileup: https://twiki.cern.ch/twiki/bin/view/CMS/PileupJSONFileforData
                    "2022": "data/pileup/pileupHistogram-Cert_Collisions2022_355100_362760_GoldenJson-13p6TeV-69200ub-99bins.root",
                    "2022EE": "data/pileup/pileupHistogram-Cert_Collisions2022_355100_362760_GoldenJson-13p6TeV-69200ub-99bins.root",
                    "2023": "data/pileup/pileupHistogram-Cert_Collisions2023_366442_370790_GoldenJson-13p6TeV-69200ub-99bins.root",
                    "2023BPix": "data/pileup/pileupHistogram-Cert_Collisions2023_366442_370790_GoldenJson-13p6TeV-69200ub-99bins.root",
                }
            ),
            "PU_reweighting_hist": "pileup",
            "PU_reweighting_file": EraModifier(
                {
                    "2016preVFP": "data/jsonpog-integration/POG/LUM/2016preVFP_UL/puWeights.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/LUM/2016postVFP_UL/puWeights.json.gz",
                    "2017": "data/jsonpog-integration/POG/LUM/2017_UL/puWeights.json.gz",
                    "2018": "data/jsonpog-integration/POG/LUM/2018_UL/puWeights.json.gz",
                    "2022": "data/jsonpog-integration/POG/LUM/2022_Summer22/puWeights.json.gz",
                    "2022EE": "data/jsonpog-integration/POG/LUM/2022_Summer22EE/puWeights.json.gz",
                    "2023": "data/jsonpog-integration/POG/LUM/2023_Summer23/puWeights.json.gz",
                    "2023BPix": "data/jsonpog-integration/POG/LUM/2023_Summer23BPix/puWeights.json.gz",
                }
            ),
            "PU_reweighting_era": EraModifier(
                {
                    "2016preVFP": "Collisions16_UltraLegacy_goldenJSON",
                    "2016postVFP": "Collisions16_UltraLegacy_goldenJSON",
                    "2017": "Collisions17_UltraLegacy_goldenJSON",
                    "2018": "Collisions18_UltraLegacy_goldenJSON",
                    "2022": "Collisions2022_355100_357900_eraBCD_GoldenJson",
                    "2022EE": "Collisions2022_359022_362760_eraEFG_GoldenJson",
                    "2023": "Collisions2023_366403_369802_eraBC_GoldenJson",
                    "2023BPix": "Collisions2023_369803_370790_eraD_GoldenJson",
                }
            ),
            "PU_reweighting_variation": "nominal",
            "golden_json_file": EraModifier(
                {
                    "2016preVFP": "data/golden_json/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
                    "2016postVFP": "data/golden_json/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
                    "2017": "data/golden_json/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt",
                    "2018": "data/golden_json/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt",
                    #"2022": "data/golden_json/Cert_Collisions2022_355100_362760_GoldenJSON.txt",
                    "2022": "data/golden_json/Cert_Collisions2022_355100_362760_Golden.json",
                    "2022EE": "data/golden_json/Cert_Collisions2022_355100_362760_Golden.json",
                    # https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGoodLumiSectionsJSONFile
                    # https://cms-service-dqmdc.web.cern.ch/CAF/certification/
                    "2023": "data/golden_json/Cert_Collisions2023_366442_370790_Golden.json",
                    "2023BPix": "data/golden_json/Cert_Collisions2023_366442_370790_Golden.json",
                }
            ),
            "met_filters": EraModifier(
                {
                    "2016preVFP": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        # "Flag_BadPFMuonDzFilter", # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                    ],
                    "2016postVFP": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        # "Flag_BadPFMuonDzFilter", # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                    ],
                    "2017": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        # "Flag_BadPFMuonDzFilter", # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                    ],
                    "2018": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter", # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                    ],
                    "2022": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        #"Flag_HBHENoiseFilter",
                        #"Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter", # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                        "Flag_hfNoisyHitsFilter",
                    ],
                    "2022EE": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        #"Flag_HBHENoiseFilter",
                        #"Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter", # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                        "Flag_hfNoisyHitsFilter",
                    ],
                    "2023": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        #"Flag_HBHENoiseFilter",
                        #"Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter", # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                        "Flag_hfNoisyHitsFilter",
                    ],
                    "2023BPix": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        #"Flag_HBHENoiseFilter",
                        #"Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter", # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                        "Flag_hfNoisyHitsFilter",
                    ],
                    #https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFiltersRun2
                }
            ),
        },
    )

    # vh add triggers (copying htautau mtau TODO)
    configuration.add_config_parameters(
        ["gghmm","vbfhmm","e2m","m2m","eemm","mmmm","nnmm","fjmm","nnmm_dycontrol","nnmm_topcontrol"],
        {
            "singlemuon_trigger": EraModifier(
                {
                # vh TODO update pT threshold in trigger matching
                    "2022": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 26,
                            "etacut": 2.5,
                            "filterbit": 3,
                            #"filterbit": -1,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        #{
                        #    "flagname": "trg_single_mu27",
                        #    "hlt_path": "HLT_IsoMu27",
                        #    "ptcut": 28,
                        #    "etacut": 2.5,
                        #    "filterbit": 3,
                        #    "trigger_particle_id": 13,
                        #    "max_deltaR_triggermatch": 0.4,
                        #},
                    ],
                    "2022EE": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 26,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2023": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 26,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2023BPix": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 26,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    ####
                    "2018": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 26,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        #{
                        #    "flagname": "trg_single_mu27",
                        #    "hlt_path": "HLT_IsoMu27",
                        #    "ptcut": 28,
                        #    "etacut": 2.5,
                        #    "filterbit": 3,
                        #    "trigger_particle_id": 13,
                        #    "max_deltaR_triggermatch": 0.4,
                        #},
                    ],
                    "2017": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu27",
                            "hlt_path": "HLT_IsoMu27",
                            "ptcut": 28,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                }
            ),
        },
    )

    # muon base selection:
    configuration.add_config_parameters(
        ["global","gghmm","vbfhmm","e2m","m2m","eemm","mmmm","nnmm","fjmm","nnmm_dycontrol","nnmm_topcontrol"],
        {
            "muon_RoccoR_files": EraModifier(
                {
                    "2016preVFP": "data/RoccoR_files/RoccoR2016aUL.txt",
                    "2016postVFP": "data/RoccoR_files/RoccoR2016bUL.txt",
                    "2017": "data/RoccoR_files/RoccoR2017UL.txt",
                    "2018": "data/RoccoR_files/RoccoR2018UL.txt",
                    "2022": "data/RoccoR_files/RoccoR2018UL.txt",
                    "2022EE": "data/RoccoR_files/RoccoR2018UL.txt",
                    "2023": "data/RoccoR_files/RoccoR2018UL.txt",
                    "2023BPix": "data/RoccoR_files/RoccoR2018UL.txt",
                }
            ),
        }
    )

    configuration.add_config_parameters(
        ["global","gghmm","vbfhmm","e2m","m2m","eemm","mmmm","nnmm","fjmm","nnmm_dycontrol","nnmm_topcontrol"],
        {
            "min_muon_pt": 20, # ggh, vbf
            "max_muon_eta": 2.4, # ggh, vbf
            "muon_id": "Muon_mediumId", # ggh, vbf cut-based atm https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2#Medium_Muon
            "muon_iso_cut": 0.25, # ggh, vbf PFIsoLoose dR=0.4 https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2#Particle_Flow_isolation
        },
    )
    configuration.add_config_parameters(
        ["e2m","m2m","eemm","mmmm","nnmm","fjmm","nnmm_dycontrol","nnmm_topcontrol"],
        {
            "max_muon_dxy": 0.05, # vh
            "max_muon_dz": 0.10, # vh
            "max_sip3d" : 8.0, # vh
            #"min_lepmva" : 0.4, 
            "min_muon_mvaTTH" : 0.4,
        },
    )
    # electron base selection:
    configuration.add_config_parameters(
        "global",
        {
            "ele_id": EraModifier(
                {
                    "2016preVFP": "Electron_mvaFall17V2noIso_WP90",
                    "2016postVFP": "Electron_mvaFall17V2noIso_WP90",
                    "2017": "Electron_mvaFall17V2noIso_WP90",
                    "2018": "Electron_mvaFall17V2noIso_WP90",
                    "2022": "Electron_mvaNoIso_WP90",
                    "2022EE": "Electron_mvaNoIso_WP90",
                    "2023": "Electron_mvaNoIso_WP90",
                    "2023BPix": "Electron_mvaNoIso_WP90",
                }
            ),
        }
    )
    configuration.add_config_parameters(
        "global",
        {
            "min_ele_pt": 20,
            "max_ele_eta": 2.5,
            "upper_threshold_barrel": 1.444,
            "lower_threshold_endcap": 1.566,
        }
    )
    # Muon scale factors configuration
    configuration.add_config_parameters(
        ["gghmm","vbfhmm","e2m","m2m","eemm","mmmm","nnmm","nnmm_dycontrol","nnmm_topcontrol"],
        {
            "muon_sf_file": EraModifier(
                {
                    "2016preVFP": "data/jsonpog-integration/POG/MUO/2016preVFP_UL/muon_Z.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/MUO/2016postVFP_UL/muon_Z.json.gz",
                    "2017": "data/jsonpog-integration/POG/MUO/2017_UL/muon_Z.json.gz",
                    "2018": "data/jsonpog-integration/POG/MUO/2018_UL/muon_Z.json.gz",
                    #"2022": "data/jsonpog-integration/POG/MUO/2018_UL/muon_Z.json.gz",
                    # https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/-/tree/master/POG/MUO?ref_type=heads
                    "2022": "data/jsonpog-integration/POG/MUO/2022_27Jun2023/muon_Z.json.gz", #BCD, 2022
                    "2022EE": "data/jsonpog-integration/POG/MUO/2022EE_27Jun2023/muon_Z.json.gz", #EFG, 2022EE
                    "2023": "data/jsonpog-integration/POG/MUO/2023_Summer23/muon_Z.json.gz",
                    "2023BPix": "data/jsonpog-integration/POG/MUO/2023_Summer23BPix/muon_Z.json.gz",
                }
            ),
            "muon_id_sf_name": "NUM_MediumID_DEN_TrackerMuons",
            #"muon_iso_sf_name": "NUM_TightRelIso_DEN_MediumID",
            "muon_iso_sf_name": EraModifier(
                {
                    "2016preVFP": "NUM_TightRelIso_DEN_MediumID",
                    "2016postVFP": "NUM_TightRelIso_DEN_MediumID",
                    "2017": "NUM_TightRelIso_DEN_MediumID",
                    "2018": "NUM_TightRelIso_DEN_MediumID",
                    "2022": "NUM_TightPFIso_DEN_MediumID",
                    "2022EE": "NUM_TightPFIso_DEN_MediumID",
                    "2023": "NUM_TightPFIso_DEN_MediumID",
                    "2023BPix": "NUM_TightPFIso_DEN_MediumID",
                }
            ),
            "muon_sf_year_id": EraModifier(
                {
                    "2016preVFP": "2016preVFP_UL",
                    "2016postVFP": "2016postVFP_UL",
                    "2017": "2017_UL",
                    "2018": "2018_UL",
                    "2022": "2022", # 2022 without year information
                    "2022EE": "2022EE", #
                    "2023": "2023", # 2022 without year information
                    "2023BPix": "2023BPix", # 2022 without year information
                }
            ),
            #"muon_sf_varation": "sf",  # "sf" is nominal, "systup"/"systdown" are up/down variations
            "muon_sf_varation": EraModifier(
                {
                    "2016preVFP": "sf", # "sf" is nominal, "systup"/"systdown" are up/down variations
                    "2016postVFP": "sf",
                    "2017": "sf",
                    "2018": "sf",
                    "2022": "nominal", # Nominal central scale factor value
                    "2022EE": "nominal",
                    "2023": "nominal", # Nominal central scale factor value
                    "2023BPix": "nominal", # Nominal central scale factor value
                }
            ),
        },
    )
    # electron scale factors configuration
    configuration.add_config_parameters(
        ["e2m","eemm"],
        {
            "ele_sf_file": EraModifier(
                {
                    "2016preVFP": "data/jsonpog-integration/POG/EGM/2016preVFP_UL/electron.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/EGM/2016postVFP_UL/electron.json.gz",
                    "2017": "data/jsonpog-integration/POG/EGM/2017_UL/electron.json.gz",
                    "2018": "data/jsonpog-integration/POG/EGM/2018_UL/electron.json.gz",
                    #"2022": "data/jsonpog-integration/POG/EGM/2018_UL/electron.json.gz",
                    # https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/-/tree/master/POG/MUO?ref_type=heads
                    "2022": "data/jsonpog-integration/POG/EGM/2022_Summer22/electron.json.gz",
                    "2022EE": "data/jsonpog-integration/POG/EGM/2022_Summer22EE/electron.json.gz",
                    "2023": "data/jsonpog-integration/POG/EGM/2023_Summer23/electron.json.gz",
                    "2023BPix": "data/jsonpog-integration/POG/EGM/2023_Summer23BPix/electron.json.gz",
                }
            ),
            #"ele_id_sf_name": "UL-Electron-ID-SF",
            "ele_id_sf_name": EraModifier(
                {
                    "2016preVFP": "UL-Electron-ID-SF",
                    "2016postVFP": "UL-Electron-ID-SF",
                    "2017": "UL-Electron-ID-SF",
                    "2018": "UL-Electron-ID-SF",
                    "2022": "Electron-ID-SF",
                    "2022EE": "Electron-ID-SF",
                    "2023": "Electron-ID-SF",
                    "2023BPix": "Electron-ID-SF",
                }
            ),
            "ele_sf_year_id": EraModifier(
                {
                    "2016preVFP": "2016preVFP",
                    "2016postVFP": "2016postVFP",
                    "2017": "2017",
                    "2018": "2018",
                    "2022": "2022Re-recoBCD",
                    "2022EE": "2022Re-recoE+PromptFG",
                    "2023": "2023PromptC",
                    "2023BPix": "2023PromptD",
                }
            ),
            "ele_sf_varation": "sf",  # "sf" is nominal, "sfup"/"sfdown" are up/down variations
        },
    )

    # jet base selection:
    configuration.add_config_parameters(
        "global",
        {
            "min_jet_pt": 25, # vh
            "max_jet_eta": 4.7, # vh
            # "jet_id": 2,  # default: 2==pass tight ID and fail tightLepVeto
            "jet_id": EraModifier(
                {
                    # Jet ID flags bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto
                    "2016preVFP": 1,  # 1==pass(loose)
                    "2016postVFP": 1,  # 1==pass(loose)
                    "2017": 2,  # 2==pass(tight)
                    "2018": 2,  # 2==pass(tight)
                    "2022": 2,  # 2==pass(tight)
                    "2022EE": 2,  # 2==pass(tight)
                    "2023": 2,  # 2==pass(tight)
                    "2023BPix": 2,  # 2==pass(tight)
                }
            ),
            # v12 not used
            "jet_puid": EraModifier(
                {
                    "2016preVFP": 1,  # 0==fail, 1==pass(loose), 3==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2016postVFP": 1,  # 0==fail, 1==pass(loose), 3==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2017": 4,  # 0==fail, 4==pass(loose), 6==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2018": 4,  # 0==fail, 4==pass(loose), 6==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2022": 4,  # 0==fail, 4==pass(loose), 6==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2022EE": 4,  # 0==fail, 4==pass(loose), 6==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2023": 4,  # 0==fail, 4==pass(loose), 6==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2023BPix": 4,  # 0==fail, 4==pass(loose), 6==pass(loose,medium), 7==pass(loose,medium,tight)
                }
            ),
            "jet_puid_max_pt": 50,  # recommended to apply puID only for jets below 50 GeV
            "deltaR_jet_veto": 0.4, # vh jet-muon dR<0.4 overlap removal
            "jet_reapplyJES": False,
            "jet_jes_sources": '{""}',
            "jet_jes_shift": 0,
            "jet_jer_shift": '"nom"',  # or '"up"', '"down"'
            "jet_jec_file": EraModifier(
                {
                    "2016preVFP": '"data/jsonpog-integration/POG/JME/2016preVFP_UL/jet_jerc.json.gz"',
                    "2016postVFP": '"data/jsonpog-integration/POG/JME/2016postVFP_UL/jet_jerc.json.gz"',
                    "2017": '"data/jsonpog-integration/POG/JME/2017_UL/jet_jerc.json.gz"',
                    "2018": '"data/jsonpog-integration/POG/JME/2018_UL/jet_jerc.json.gz"',
                    #"2022": '"data/jsonpog-integration/POG/JME/2018_UL/jet_jerc.json.gz"',
                    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetMET#Group_charge
                    "2022": '"data/jsonpog-integration/POG/JME/2022_Summer22/jet_jerc.json.gz"',
                    "2022EE": '"data/jsonpog-integration/POG/JME/2022_Summer22EE/jet_jerc.json.gz"',
                    "2023": '"data/jsonpog-integration/POG/JME/2023_Summer23/jet_jerc.json.gz"',
                    "2023BPix": '"data/jsonpog-integration/POG/JME/2023_Summer23BPix/jet_jerc.json.gz"',
                }
            ),
            "jet_jer_tag": EraModifier(
                {
                    "2016preVFP": '"Summer20UL16APV_JRV3_MC"',
                    "2016postVFP": '"Summer20UL16_JRV3_MC"',
                    "2017": '"Summer19UL17_JRV2_MC"',
                    "2018": '"Summer19UL18_JRV2_MC"',
                    #"2022": '"Summer19UL18_JRV2_MC"',
                    "2022": '"Summer22_22Sep2023_JRV1_MC"',
                    "2022EE": '"Summer22EE_22Sep2023_JRV1_MC"',
                    "2023": '"Summer23Prompt23_RunCv4_JRV1_MC"',
                    "2023BPix": '"Summer23BPixPrompt23_RunD_JRV1_MC"',
                }
            ),
            "jet_jes_tag_data": '""',
            "jet_jes_tag": EraModifier(
                {
                    "2016preVFP": '"Summer19UL16APV_V7_MC"',
                    "2016postVFP": '"Summer19UL16_V7_MC"',
                    "2017": '"Summer19UL17_V5_MC"',
                    "2018": '"Summer19UL18_V5_MC"',
                    #"2022": '"Summer19UL18_V5_MC"',
                    "2022": '"Summer22_22Sep2023_V2_MC"',
                    "2022EE": '"Summer22EE_22Sep2023_V2_MC"',
                    "2023": '"Summer23Prompt23_V1_MC"',
                    "2023BPix": '"Summer23BPixPrompt23_V1_MC"',
                }
            ),
            #"jet_jec_algo": '"AK4PFchs"',
            "jet_jec_algo": EraModifier(
                    {
                        "2016preVFP": '"AK4PFchs"',
                        "2016postVFP": '"AK4PFchs"',
                        "2017": '"AK4PFchs"',
                        "2018": '"AK4PFchs"',
                        "2022": '"AK4PFPuppi"',
                        "2022EE": '"AK4PFPuppi"',
                        "2023": '"AK4PFPuppi"',
                        "2023BPix": '"AK4PFPuppi"',
                    }
            ),
            "jet_veto_map": EraModifier(
                    {
                        "2022":'"data/jsonpog-integration/POG/JME/2022_Summer22/jetvetomaps.json.gz"',
                        "2022EE": '"data/jsonpog-integration/POG/JME/2022_Summer22EE/jetvetomaps.json.gz"',
                        "2023": '"data/jsonpog-integration/POG/JME/2023_Summer23/jetvetomaps.json.gz"',
                        "2023BPix": '"data/jsonpog-integration/POG/JME/2023_Summer23BPix/jetvetomaps.json.gz"',
                    }
            ),
            "jet_veto_tag": EraModifier(
                    {
                        "2022":'"Summer22_23Sep2023_RunCD_V1"',
                        "2022EE": '"Summer22EE_23Sep2023_RunEFG_V1"',
                        "2023": '"Summer23Prompt23_RunC_V1"',
                        "2023BPix": '"Summer23BPixPrompt23_RunD_V1"',
                    }
            ),
        },
    )
    # fat jet base selection:
    # vhbb run2 approval link: fatjet in slide 4
    # https://indico.cern.ch/event/1198083/contributions/5039217/attachments/2507086/4309256/Calandri_HIGPAG_13092022.pdf
    configuration.add_config_parameters(
        "global",
        {
            "min_fatjet_pt": 150, # vhbb selection 250
            "max_fatjet_eta": 2.5, # vhbb selection
            "min_fatjet_MSD": 50, # soft drop mass > 50 GeV
            # "fatjet_id": 2,  # default: 2==pass tight ID and fail tightLepVeto
            "fatjet_id": EraModifier(
                {
                    # Jet ID flags bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto
                    "2016preVFP": 1,  # 1==pass(loose)
                    "2016postVFP": 1,  # 1==pass(loose)
                    "2017": 2,  # 2==pass(tight)
                    "2018": 2,  # 2==pass(tight)
                    "2022": 2,  # 2==pass(tight)
                    "2022EE": 2,  # 2==pass(tight)
                    "2023": 2,  # 2==pass(tight)
                    "2023BPix": 2,  # 2==pass(tight)
                }
            ),
            # may no need fatjet_puid
            "deltaR_fatjet_veto": 0.8, # vh fatjet-muon dR<0.8 overlap removal
            "fatjet_reapplyJES": False,
            "fatjet_jes_sources": '{""}',
            "fatjet_jes_shift": 0,
            "fatjet_jer_shift": '"nom"',  # or '"up"', '"down"'
            "fatjet_jec_file": EraModifier(
                {
                    "2016preVFP": '"data/jsonpog-integration/POG/JME/2016preVFP_UL/fatJet_jerc.json.gz"',
                    "2016postVFP": '"data/jsonpog-integration/POG/JME/2016postVFP_UL/fatJet_jerc.json.gz"',
                    "2017": '"data/jsonpog-integration/POG/JME/2017_UL/fatJet_jerc.json.gz"',
                    "2018": '"data/jsonpog-integration/POG/JME/2018_UL/fatJet_jerc.json.gz"',
                    #"2022": '"data/jsonpog-integration/POG/JME/2018_UL/fatJet_jerc.json.gz"',
                    "2022": '"data/jsonpog-integration/POG/JME/2022_Summer22/fatJet_jerc.json.gz"',
                    "2022EE": '"data/jsonpog-integration/POG/JME/2022_Summer22EE/fatJet_jerc.json.gz"',
                    "2023": '"data/jsonpog-integration/POG/JME/2023_Summer23/fatJet_jerc.json.gz"',
                    "2023BPix": '"data/jsonpog-integration/POG/JME/2023_Summer23BPix/fatJet_jerc.json.gz"',
                }
            ),
            "fatjet_jer_tag": EraModifier(
                {
                    "2016preVFP": '"Summer20UL16APV_JRV3_MC"', # TODO JER tag
                    "2016postVFP": '"Summer20UL16_JRV3_MC"',
                    "2017": '"Summer19UL17_JRV2_MC"',
                    "2018": '"Summer19UL18_JRV2_MC"',
                    #"2022": '"Summer19UL18_JRV2_MC"',
                    "2022": '"Summer22_22Sep2023_JRV1_MC"',
                    "2022EE": '"Summer22EE_22Sep2023_JRV1_MC"',
                    "2023": '"Summer23Prompt23_RunCv4_JRV1_MC"',
                    "2023BPix": '"Summer23BPixPrompt23_RunD_JRV1_MC"',
                }
            ),
            "fatjet_jes_tag_data": '""',
            "fatjet_jes_tag": EraModifier(
                {
                    "2016preVFP": '"Summer19UL16APV_V7_MC"', # TODO JES tag
                    "2016postVFP": '"Summer19UL16_V7_MC"',
                    "2017": '"Summer19UL17_V5_MC"',
                    "2018": '"Summer19UL18_V5_MC"',
                    "2022": '"Summer22_22Sep2023_V2_MC"',
                    "2022EE": '"Summer22EE_22Sep2023_V2_MC"',
                    "2023": '"Summer23Prompt23_V1_MC"',
                    "2023BPix": '"Summer23BPixPrompt23_V1_MC"',
                }
            ),
            "fatjet_jec_algo": '"AK8PFPuppi"',
        },
    )
    # bjet base selection:
    configuration.add_config_parameters(
        "global",
        {
            "min_bjet_pt": 25, # vh
            "max_bjet_eta": EraModifier( # vh
                {
                    "2016preVFP": 2.4,
                    "2016postVFP": 2.4,
                    "2017": 2.5,
                    "2018": 2.5,
                    "2022": 2.5,
                    "2022EE": 2.5,
                    "2023": 2.5,
                    "2023BPix": 2.5,
                }
            ),
            "btag_cut_loose": EraModifier(  # loose # (vhmm Run2 use DeepCSV)
                {
                    "2016preVFP": 0.2027, # 2016preVFP: 0.2027, 2016postVFP: 0.1918
                    "2016postVFP": 0.1918, # 2016preVFP: 0.2027, 2016postVFP: 0.1918
                    "2017": 0.1355, # 2017: 0.1355
                    "2018": 0.1208, # 2018: 0.1208
                    # https://btv-wiki.docs.cern.ch/ScaleFactors/#sf-campaigns
                    # particleNet
                    "2022": 0.047,
                    "2022EE": 0.0499,
                    "2023": 0.0358,
                    "2023BPix": 0.0359,
                }
            ),
            "btag_cut_medium": EraModifier(  # medium
                {
                    "2016preVFP": 0.6001, # 2016preVFP: 0.6001, 2016postVFP: 0.5847
                    "2016postVFP": 0.5847, # 2016preVFP: 0.6001, 2016postVFP: 0.5847
                    "2017": 0.4506, # 2017: 0.4506
                    "2018": 0.4168, # 2018: 0.4168
                    "2022": 0.245,
                    "2022EE": 0.2605,
                    "2023": 0.1917,
                    "2023BPix": 0.1919,
                }
            ),
        },
    )
    # bjet scale factors
    configuration.add_config_parameters(
        scopes,
        {
            "btag_sf_file": EraModifier(
                {
                    "2016preVFP": "data/jsonpog-integration/POG/BTV/2016preVFP_UL/btagging.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/BTV/2016postVFP_UL/btagging.json.gz",
                    "2017": "data/jsonpog-integration/POG/BTV/2017_UL/btagging.json.gz",
                    "2018": "data/jsonpog-integration/POG/BTV/2018_UL/btagging.json.gz",
                    "2022": "data/jsonpog-integration/POG/BTV/2022_Summer22/btagging.json.gz",
                    "2022EE": "data/jsonpog-integration/POG/BTV/2022_Summer22EE/btagging.json.gz",
                    "2023": "data/jsonpog-integration/POG/BTV/2023_Summer23/btagging.json.gz",
                    "2023BPix": "data/jsonpog-integration/POG/BTV/2023_Summer23BPix/btagging.json.gz",
                }
            ),
            "btag_sf_variation": "central",
            #"btag_corr_algo": "deepJet_shape",
            "btag_corr_algo": EraModifier(
                {
                    "2016preVFP": "deepCSV_comb",
                    "2016postVFP": "deepCSV_comb",
                    "2017": "deepCSV_comb",
                    "2018": "deepCSV_comb",
                    "2022": "particleNet_comb",
                    "2022EE": "particleNet_comb",
                    # no particleNet_comb yet 2025 Mar 10
                    # no using the BtagSF
                    "2023": "particleNet_light",
                    "2023BPix": "particleNet_light",
                }
            )
        }
    )

    # veto ttH
    configuration.add_config_parameters(
        "global",
        {
            "vetottH_max_nbjets_loose" : 1,
            "vetottH_max_nbjets_medium" : 0,
            # "vh_njets" : 3,
        }
    )

    #veto VH
    configuration.add_config_parameters(
        ["gghmm","vbfhmm"],
        {
            "vetoVH_max_nmuons" : 2,
            "vetoVH_max_nelectrons" : 0,
        }
    )

    # vbfhmm cuts
    configuration.add_config_parameters(
        ["vbfhmm"],
        {
            "vbf_nmuons" : 2,
            "flag_DiMuonFromHiggs" : 1,
            "flag_LeptonChargeSumVeto" : 2, # sum lepton charge = 0
            #"lead_muon_pt" : 26,
            # "dimuon_pair" : 1, # dimuon_pair in [110,150] >=1
            "vbf_njets" : 2,
            "lead_jet_pt" : 35, #lead jet pt > 35
            "sublead_jet_pt" : 25, #sublead jet pt > 25
            "dijet_mass" : 400, #dijet mass > 400
            "dijet_eta" : 2.5, #jet-jet delta eta > 2.5
            "min_genjet_pt": 25,
            "max_genjet_eta": 4.7, # vh
        }
    )

    ###
    configuration.add_config_parameters(
        ["vbfhmm"],
        {
            "RoccoR_seed": 0,
            "RoccoR_error_set": 0,
            "RoccoR_error_member": 0,
        }
    )
    ###

    """
    ## all scopes misc settings
    configuration.add_config_parameters(
        scopes,
        {
            "pairselection_min_dR": 0.5,
        },
    )
    """
    configuration.add_producers(
        "global",
        [
            event.SampleFlags,
            event.PUweights,
            #event.PrefireWeight,
            event.Lumi,
            event.MetFilter,
            muons.BaseMuons, # vh
            # vbfhmm muon Rochester corr, FSR recovery added 
            # GeoFit? TODO
            electrons.BaseElectrons,
            jets.JetEnergyCorrection_2022, # include pt corr and mass corr and 2022 modify the JR sf adding pt
            #jets.JetEnergyCorrection_2022_GenMatch, # include pt corr and mass corr and 2022 modify the JR sf adding pt
            #jets.GoodJets, # vh overlap removal with ?base? muons done [need validation]
            jets.GoodJets_2022, # vh overlap removal with ?base? muons done [need validation]
            jets.GoodBJetsLoose, 
            jets.GoodBJetsMedium, 
            ####
            jets.NumberOfGoodJets,
            jets.NumberOfLooseB, # vh count loose bjets for ttH veto
            jets.NumberOfMediumB, # vh count medium bjets for ttH veto
            #event.VetottHLooseB, # vh veto ttH no more than 1 loose bjet
            #event.VetottHMediumB, # vh veto ttH no more than 1 medium bjet
            met.MetBasics, # build met vector for calculation
            met.BuildGenMetVector,
            jets.JetCollection,
            jets.Calc_MHT,
            #jets.FilterNJets,
            #jets.LVJet1,
            #jets.LVJet2,
            #jets.LVJet3,
            #jets.LVJet4,
            #fatjets.FatJetEnergyCorrection,
            #fatjets.GoodFatJets,
            #fatjets.NumberOfGoodFatJets,
            #fatjets.FatJetCollection,
            #fatjets.LVFatJet1,
        ],
    )
    configuration.add_producers(
        "vbfhmm",
        [
            muons.GoodMuons, # vh tighter selections on muons
            muons.NumberOfGoodMuons,
            # muons.MuonIDCut, # included in basedMuon and GoodMuons
            #event.FilterNMuons, # vbfhmm == 2 muons
            event.FilterNMuons_OverE2, # vbfhmm >= 2 muons
            muons.MuonCollection, # collect ordered by pt
            ###
            event.Mask_DiMuonPair, # dimuonHiggs index
            event.Flag_DiMuonFromHiggs,
            event.HiggsToDiMuonPair_p4, # select the dimuon pairs in [70,150] and order by pt
            ###
            event.DiMuonMassFromZVeto,# has dimuon from Z return mask equal to 0, otherwise return 1
            ##event.VetoVHElectron,
            ##event.VetoVHMuon,
            ##jets.FilterNJets,
            ####event.LeadMuonPtCut,
            ##event.LeadJetPtCut,
            ##event.SubleadJetPtCut,
            ##event.DiJetMassCut,
            ##event.DiJetEtaCut,
            lepton.LeptonChargeSumVeto,
            ###
            electrons.NumberOfBaseElectrons,
            electrons.ElectronCollection,
            ###
            jets.LVJet1,
            jets.LVJet2,
            # flag cut
            event.FilterFlagDiMuFromH,
            event.FilterFlagLepChargeSum,
            ###
            muons.Mu1_H,
            muons.Mu2_H,
            ###
            event.mumuH_dR,
            ###
            event.mu1_mu2_dphi,
            #
            muons.LVMu1,
            muons.LVMu2,
            triggers.GenerateSingleMuonTriggerFlagsForDiMuChannel_2022, 
            # vvfhmm the trigger-matched muon should have pT > 29 (26) for 2017 (2016,18)
            
            #
            p4.mu1_fromH_pt,
            p4.mu1_fromH_eta,
            p4.mu1_fromH_phi,
            p4.mu2_fromH_pt,
            p4.mu2_fromH_eta,
            p4.mu2_fromH_phi,
            p4.met_pt,
            p4.met_phi,
            p4.H_pt,
            p4.H_eta,
            p4.H_phi,
            p4.H_mass,
            p4.jet1_pt,
            p4.jet1_eta,
            p4.jet1_phi,
            p4.jet1_mass,
            p4.jet2_pt,
            p4.jet2_eta,
            p4.jet2_phi,
            p4.jet2_mass,
            jets.DiJetMass,
            jets.DiJetEta,
            jets.Jet1_rawpT,
            jets.Jet1_rawMass,
            jets.Jet2_rawpT,
            jets.Jet2_rawMass,
            #jets.Jet1_QGdiscriminator,
            #jets.Jet2_QGdiscriminator,
            #jets.nSoftJet5,
            #jets.Jet1_qgl,
            #jets.Jet2_qgl,
            
            p4.genmet_pt,
            p4.genmet_phi,

            scalefactors.btagging_SF,
            scalefactors.MuonIDIso_SF_vbfhmm_noYear, #2 mu from H
            fsrPhoton.muon_fsrPhotonIdx_1,
            fsrPhoton.muon_fsrPhotonIdx_2,

            fsrPhoton.muon_fsrPhoton_pt_1,
            fsrPhoton.muon_fsrPhoton_eta_1,
            fsrPhoton.muon_fsrPhoton_phi_1,
            fsrPhoton.muon_fsrPhoton_dROverEt2_1,
            fsrPhoton.muon_fsrPhoton_relIso03_1,
            fsrPhoton.muon_fsrPhoton_pt_2,
            fsrPhoton.muon_fsrPhoton_eta_2,
            fsrPhoton.muon_fsrPhoton_phi_2,
            fsrPhoton.muon_fsrPhoton_dROverEt2_2,
            fsrPhoton.muon_fsrPhoton_relIso03_2,
#
            muons.Muon_pTErr_1,
            muons.Muon_pTErr_2,

            genparticles.dimuon_gen_collection,
            genparticles.genMu1_H,
            genparticles.genMu2_H,
            p4.genmu1_fromH_pt,
            p4.genmu1_fromH_eta,
            p4.genmu1_fromH_phi,
            p4.genmu1_fromH_mass,
            p4.genmu2_fromH_pt,
            p4.genmu2_fromH_eta,
            p4.genmu2_fromH_phi,
            p4.genmu2_fromH_mass,
            jets.GEN_GoodJets,
            jets.NumberOfGoodGENJets,

        ],
    )

    configuration.add_outputs(
        scopes,
        [
            q.is_data,
            q.is_embedding,
            q.is_top,
            q.is_dyjets,
            q.is_wjets,
            q.is_diboson,
            q.is_vhmm,
            q.is_gghmm,
            q.is_vbfhmm,
            q.is_zjjew,
            q.is_triboson,
            nanoAOD.run,
            q.lumi,
            nanoAOD.event,
            q.puweight,
            #q.prefireweight,
            #
            q.nmuons,
            #q.MHT_p4,
            q.njets,
            q.nbjets_loose,
            q.nbjets_medium,

            q.met_pt,
            q.met_phi,
            q.genmet_pt,
            q.genmet_phi,
        ],
    )

    configuration.add_outputs(
        ["vbfhmm","e2m","m2m","eemm","mmmm","nnmm","fjmm"],
        [
            q.mu1_fromH_pt,
            q.mu1_fromH_eta,
            q.mu1_fromH_phi,

            q.mu2_fromH_pt,
            q.mu2_fromH_eta,
            q.mu2_fromH_phi,
            
            q.H_pt,
            q.H_eta,
            q.H_phi,
            q.H_mass,

        ],
    )
    configuration.add_outputs(
        "vbfhmm",
        [
            q.jet1_pt,
            q.jet1_eta,
            q.jet1_phi,
            q.jet1_mass,
            q.jet1_rawpT,
            q.jet1_rawMass,
            q.jet2_rawpT,
            q.jet2_rawMass,

            q.jet2_pt,
            q.jet2_eta,
            q.jet2_phi,
            q.jet2_mass,

            q.dijet_mass,
            q.dijet_eta,
            #q.btag_weight,
            
            q.mumuH_dR,

            #
            q.nelectrons,

            ###
            q.mu1_mu2_dphi,
            
            q.Flag_dimuon_Zmass_veto,
            q.Flag_LeptonChargeSumVeto,
            q.Flag_DiMuonFromHiggs,
            triggers.GenerateSingleMuonTriggerFlagsForDiMuChannel_2022.output_group,

            # gen
            
            #
            q.id_wgt_mu_1,
            q.iso_wgt_mu_1,
            q.id_wgt_mu_2,
            q.iso_wgt_mu_2,
            q.mu1_fromH_ptErr,
            q.mu2_fromH_ptErr,
            q.pt_rc_1,
            q.pt_rc_2,
            # fsr
            q.fsrPhoton_pt_1,
            q.fsrPhoton_eta_1,
            q.fsrPhoton_phi_1,
            q.fsrPhoton_dROverEt2_1,
            q.fsrPhoton_relIso03_1,
            q.fsrPhoton_pt_2,
            q.fsrPhoton_eta_2,
            q.fsrPhoton_phi_2,
            q.fsrPhoton_dROverEt2_2,
            q.fsrPhoton_relIso03_2,
            #q.id_wgt_mu_3,
            #q.iso_wgt_mu_3,
            #q.jet1_qgl,
            #q.jet2_qgl,
            #q.nSoftJet5,
            nanoAOD.nSoftJet5,
            #nanoAOD.nGenJet,
            #q.ngenjets,
        ],
    )
    ##
    if sample != "data":
        configuration.add_modification_rule(
            "vbfhmm",
            AppendProducer(
                producers=[event.ApplyRoccoRMC_2022,],
                samples=sample,
                update_output=False,
            ),
        )
    if sample == "data":
        configuration.add_modification_rule(
            "vbfhmm",
            AppendProducer(
                producers=[event.ApplyRoccoRData,],
                samples=sample,
                update_output=False,
            ),
        )
    ###3252#
    
    # add genWeight for everything but data
    if sample != "data":
        configuration.add_outputs(
            scopes,
            [
                nanoAOD.genWeight,
                nanoAOD.nGenJet,
                q.ngenjets,
            ],
        )

    # all data
    configuration.add_modification_rule(
        "global",
        RemoveProducer(
            #producers=[event.PUweights, event.PrefireWeight, jets.JetEnergyCorrection, fatjets.FatJetEnergyCorrection, met.BuildGenMetVector,],
            #producers=[event.PUweights, event.PrefireWeight, jets.JetEnergyCorrection, met.BuildGenMetVector,],
            producers=[event.PUweights, jets.JetEnergyCorrection_2022, met.BuildGenMetVector,],
            #producers=[event.PUweights, jets.JetEnergyCorrection_2022_GenMatch, met.BuildGenMetVector,],
            samples=["data"],
        ),
    )
    # changes needed for data
    # global scope
    configuration.add_modification_rule(
        "global",
        AppendProducer(
            #producers=[jets.RenameJetsData, fatjets.RenameFatJetsData, event.JSONFilter,],
            #producers=[jets.RenameJetsData,event.JSONFilter,],
            #jetvetomap
            producers=[jets.JetEnergyCorrection_data_2022, event.JSONFilter,],
            samples=["data"],
            update_output=False,
        ),
    )
    ##ahhh
    configuration.add_modification_rule(
        scopes,
        RemoveProducer(
            producers=[
                p4.genmet_pt,
                p4.genmet_phi,
            ],
            samples=["data"],
        ),
    )
    ##

    # As now 2022 data has no Jet_puID, so no possible to do JetPUIDCut
    #if era == "2022" or era == "2022EE":
        ## 2022 MC
        #if sample != "data":
        #    configuration.add_modification_rule(
        #        "global",
        #        RemoveProducer(
        #            producers=[jets.GoodJets, event.PrefireWeight,],
        #            samples=sample,
        #        ),
        #    )
        #    configuration.add_modification_rule(
        #        "global",
        #        AppendProducer(
        #            producers=[jets.JetEnergyCorrection_2022,],
        #            samples=sample,
        #            update_output=False,
        #        ),
        #    )
        # 2022 data and mc
        #configuration.add_modification_rule(
        #    "global",
        #    AppendProducer(
        #        producers=[jets.GoodJets_2022,],
        #        samples=sample,
        #        update_output=False,
        #    ),
        #)
        ###ahhhh

    # all data vbfhmm
    configuration.add_modification_rule(
        ["vbfhmm"],
        RemoveProducer(
            producers=[
                genparticles.dimuon_gen_collection,
                genparticles.genMu1_H,
                genparticles.genMu2_H,
                p4.genmu1_fromH_pt,
                p4.genmu1_fromH_eta,
                p4.genmu1_fromH_phi,
                p4.genmu1_fromH_mass,
                p4.genmu2_fromH_pt,
                p4.genmu2_fromH_eta,
                p4.genmu2_fromH_phi,
                p4.genmu2_fromH_mass,
                jets.GEN_GoodJets,
                jets.NumberOfGoodGENJets,
                scalefactors.MuonIDIso_SF_vbfhmm_noYear,
                scalefactors.btagging_SF,
            ],
            samples=["data"],
        ),
    )
    #if sample != "data":
    #    if era == "2022" or era == "2022EE":
    #        configuration.add_modification_rule(
    #            "vbfhmm",
    #            RemoveProducer(
    #                producers=[scalefactors.MuonIDIso_SF_vbfhmm,],
    #                samples=sample,
    #                update_output=False,
    #            ),
    #        )
    #        configuration.add_modification_rule(
    #            "vbfhmm",
    #            AppendProducer(
    #                producers=[scalefactors.MuonIDIso_SF_vbfhmm_noYear,],
    #                samples=sample,
    #                update_output=False,
    #            ),
    #        )


    configuration.add_shift(
        SystematicShift(
            name="MuonIDUp",
            shift_config={"m2m": {"muon_sf_varation": "systup"}},
            producers={
                "m2m": [
                    # scalefactors.Muon_1_ID_SF,
                    # scalefactors.Muon_2_ID_SF,
                ]
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="MuonIDDown",
            shift_config={"m2m": {"muon_sf_varation": "systdown"}},
            producers={
                "m2m": [
                    # scalefactors.Muon_1_ID_SF,
                    # scalefactors.Muon_2_ID_SF,
                ]
            },
        )
    )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
