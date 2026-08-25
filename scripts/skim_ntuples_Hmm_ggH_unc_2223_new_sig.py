#!/usr/bin/env python
#
# Created QianyingGUO 05.22.2024
#
import gc  # garbage collector
import os
import re
import math
from argparse import ArgumentParser
from ROOT import Math, TVector2, TVector3, TLorentzVector
import numpy as np
#import time
import pandas as pd
import uproot
# from root_pandas import *
from tqdm import tqdm
from scripts.ZSelector_Horn_2425_v5 import *
import awkward as ak
#from out_dict_ggH import *
#from out_dict_ggH_24_simple import *
from out_dict_ggH_2425_v5 import *
from Datasets.Hmumu.Data_22EE import *
from Datasets.Hmumu.HToMumu_22EE import *
from Datasets.Hmumu.Background_22EE import *

def getArgs():
    parser = ArgumentParser(description="Skim the input ntuples for Hmumu XGBoost analysis.")
    parser.add_argument('-i', '--input', action='store', default='inputs', help='Path to the input ntuple')
    parser.add_argument('-o', '--output', action='store', default='outputs', help='Path to the output ntuple')
    parser.add_argument('-y', '--year', action='store', default='2022EE', help='which year of DataSet')
    parser.add_argument('--chunksize', type=int, default=500000, help='size to process at a time') 
    return  parser.parse_args()

def preselect(data):

    mask = data["ngenjets"] <= 1
    filtered_data = {key: value[mask] for key, value in data.items()}
    return filtered_data
    #return data

def decorate_hmm(data):

    if data.shape[0] == 0: return data
    data['muon_mass']=0.1056584

    data['H_zeppenfeld'] = data.apply(lambda x: compute_H_zeppenfeld(x), axis=1)
    data['z_star_H_zeppenfeld'] = data.apply(lambda x: compute_z_star_H_zeppenfeld(x), axis=1)
    data['R_pt'] = data.apply(lambda x: compute_pt_balance(x), axis=1)
    data = data.astype(float)
    data = data.astype({'njets': int, 'nelectrons': int, 'nmuons': int, 'event': int})

    return data
###

def decorate_vbfhmm(data):

    if data.shape[0] == 0: return data
    return data

def getLumi(year):
    if year == "2018":  lumi = 59.8*1000
    elif year == "2017":  lumi = 41.4*1000
    elif year == "2016":  lumi = 35*1000
    elif year == "2022":  lumi = (5.02+2.97)*1000
    elif year == "2022EE":  lumi = (5.81+17.78+3.09)*1000
    elif year == "2023":  lumi = 17.96*1000
    elif year == "2023BPix":  lumi = 9.68*1000
    elif year == "2024":  lumi = 109.82*1000
    elif year == "2025":  lumi = 110.84*1000
    return lumi


from pathlib import PurePosixPath
SHORT_NAMES = {
    "DYto2Mu-2Jets_MLL-105To160_": "DY_105To160",
    "EWK_2L2J_":                    "EWK_LLJJ_M50",
    'DYJetsToLL_M-50-madgraphMLM': 'DY_50MLM',
    'DYto2L-2Jets_MLL-50_amcatnloFXFX': 'DY_50FxFx',

    "GluGluHto2Mu_M-125_":         "GluGluHto2Mu_M-125",
    "VBFHto2Mu_M-125_":            "VBFHto2Mu_M-125",
    "TTH_Hto2Mu_M-125_":           "TTHto2Mu_M-125",
    "WminusH_Hto2Mu_":             "WminusHto2Mu_M-125",
    "WplusH_Hto2Mu_":              "WplusHto2Mu_M-125",
    "ZH_Hto2Mu_":                  "qqZHto2Mu_M-125",
    "ggZHto2Mu_M-125_":             "ggZHto2Mu_M-125",
    "bbHto2Mu_M-125_":              "bbHto2Mu_M-125",

    "TTto2L2Nu_":                  "TTTo2L2Nu",
    "TWminusto2L2Nu_":             "ST_tW_top",
    "TbarWplusto2L2Nu_":           "ST_tW_antitop",
    "TZQB-4FS_OnshellZ_":          "tZq",
    "TZQB-Zto2L-4FS_MLL-30_":      "tZq",

    "WWto2L2Nu_":                  "WWTo2L2Nu",
    "WZto2L2Q_":                   "WZTo2L2Q",
    "WZto3LNu_":                   "WZTo3LNu",
    "ZZto2L2Nu_":                  "ZZTo2L2Nu",
    "ZZto2L2Q_":                   "ZZTo2L2Q",
    "ZZto4L_":                     "ZZTo4L",

    "WWW_4F_":                     "WWW",
    "WWZ_4F_":                     "WWZ",
    "WZZ_":                        "WZZ",
    "ZZZ_":                        "ZZZ",
    "Muon":                        "data",
}


def getShortName(full_name):
    filename = PurePosixPath(full_name).name
    ShortName=None

    # Special samples: check these before the general DY matching.
    if "Fil-VBF" in filename or "VBF-Fil" in filename or "VBFFilter" in filename:
        ShortName = "DY_105To160_VBF-Fil"
    elif (
        "DY_105To160_" in filename
        or "DYto2Mu-2Jets_MLL-105To160_amcatnloFXFX" in filename
    ):
        ShortName = "DY_105To160"
    elif any(pattern in filename for pattern in (
        "EWK_2Mu2J_105to160",
        "EWK_LLJJ_105to160",
        "EWK-2Mu2J_Bin-M2Mu-105to160",
        "EWK-2Mu2J_MLL-105To160",
        "EWK_2Mu2J_Bin-MLL-105to160",
        "EWK-2Mu2J_M2Mu-105to160",
    )):
        ShortName = "EWK_LLJJ_M105To160"
    if ShortName is not None:
        print("ShortName: ", ShortName)
        return ShortName

    for prefix, ShortName in SHORT_NAMES.items():
        if filename.startswith(prefix):
            print("ShortName: ", ShortName)
            return ShortName

    raise ValueError(f"No short name configured for: {filename}")

def combXS(xs_sig,xs_bkg):
        xs = {}
        for s in xs_sig:
            xs[s] = xs_sig[s]
        for s in xs_bkg:
            xs[s] = xs_bkg[s]

        xs["data"] = 1
        xs["fake"] = 1

        return xs

def process_chunk(data, year, isMC, weight):
    """Apply your existing logic (without writing), return two DataFrames."""
    # this is basically your original chunk body, minus the file writes

    data["weight"] = np.full(len(data["event"]), weight)
    print("%i events... " % (len(data["event"])), end="", flush=True)
    data["isMC"] = np.full(len(data["event"]), isMC)
    data["year"] = np.full(len(data["event"]), year)

    data = select(data)
    #data["genWeight"] = data["Generator_weight"]

    if isMC:
        data["eventWeight"] = (
            data["genWeight"]
            * data["puweight"]
            * data["weight"]
            * data["id_wgt_mu_1"] * data["id_wgt_mu_2"]
            * data["iso_wgt_mu_1"] * data["iso_wgt_mu_2"]
        )

        data['id_MuonEffup']   = (data["id_wgt_mu_1__MuonEffup"]  * data["id_wgt_mu_2__MuonEffup"])  / (data["id_wgt_mu_1"] * data["id_wgt_mu_2"])
        data['id_MuonEffdown'] = (data["id_wgt_mu_1__MuonEffdown"]* data["id_wgt_mu_2__MuonEffdown"])/ (data["id_wgt_mu_1"] * data["id_wgt_mu_2"])
        data['iso_MuonEffup']  = (data["iso_wgt_mu_1__MuonEffup"] * data["iso_wgt_mu_2__MuonEffup"]) / (data["iso_wgt_mu_1"]* data["iso_wgt_mu_2"])
        data['iso_MuonEffdown']= (data["iso_wgt_mu_1__MuonEffdown"]* data["iso_wgt_mu_2__MuonEffdown"])/(data["iso_wgt_mu_1"]* data["iso_wgt_mu_2"])
    else:
        data["eventWeight"]      = data["weight"]
        data['id_MuonEffup']     = np.full(len(data["event"]), 1.0)
        data['id_MuonEffdown']   = np.full(len(data["event"]), 1.0)
        data['iso_MuonEffup']    = np.full(len(data["event"]), 1.0)
        data['iso_MuonEffdown']  = np.full(len(data["event"]), 1.0)
        data['PDF_uncertainty_down'] = np.full(len(data["event"]), 1.0)
        data['PDF_uncertainty_up']   = np.full(len(data["event"]), 1.0)
        data['qcd_unc_down']         = np.full(len(data["event"]), 1.0)
        data['qcd_unc_up']           = np.full(len(data["event"]), 1.0)

    data['nleptons'] = data['nelectrons'] + data['nmuons']

    label_map = {
        "2018": 2018,
        "2017": 2017,
        "2016": 2016,
        "2022": 2022,
        "2022EE": -2022,
        "2023": 2023,
        "2023BPix": -2023,
        "2024": 2024,
        "2025": 2025
    }
    data["source_year"] = np.full(len(data["event"]), label_map[year])

    # you already have 'branches' list in your code
    output = {branch: data[branch] for branch in branches}
    df = pd.DataFrame(output)

    # your region selections
    data_two_jet_m110To150_ggH = df[
        (df['GGH']) &
        (df['trg_single_mu24']) &
        (df['diMufsr_kit_BSC_mass'] > 110) & (df['diMufsr_kit_BSC_mass'] < 150)
    ]

    data_two_jet_m110To150_VBF = df[
        (df['VBF']) &
        (df['trg_single_mu24']) &
        (df['diMufsr_kit_BSC_mass'] > 110) & (df['diMufsr_kit_BSC_mass'] < 150)
    ]

    #rm_notUsed=["GGH","VBF","iso_wgt_mu_1__MuonIDIsoDown","iso_wgt_mu_1__MuonIDIsoUp","iso_wgt_mu_2__MuonIDIsoDown","iso_wgt_mu_2__MuonIDIsoUp", "id_wgt_mu_1__MuonIDIsoDown","id_wgt_mu_1__MuonIDIsoUp","id_wgt_mu_2__MuonIDIsoDown","id_wgt_mu_2__MuonIDIsoUp","trg_single_mu24"]

    #rm_notUsed=["id_MuonEffup", "id_MuonEffdown", "iso_MuonEffup", "iso_MuonEffdown", "PDF_uncertainty_down", "PDF_uncertainty_up", "qcd_unc_down", "qcd_unc_up","GGH","VBF","VH","TTH"]
    rm_notUsed=["GGH","VBF","VH","TTH"]
    data_two_jet_m110To150_ggH = data_two_jet_m110To150_ggH.drop(columns=rm_notUsed, errors="ignore")
    data_two_jet_m110To150_VBF = data_two_jet_m110To150_VBF.drop(columns=rm_notUsed, errors="ignore")
    return data_two_jet_m110To150_ggH, data_two_jet_m110To150_VBF
    #return data_two_jet_m110To150_VBF




def process_chunk_sys(data, year, isMC, weight):
    """Apply your existing logic (without writing), return two DataFrames."""
    # this is basically your original chunk body, minus the file writes

    data["weight"] = np.full(len(data["event"]), weight)
    print("%i events... " % (len(data["event"])), end="", flush=True)
    data["isMC"] = np.full(len(data["event"]), isMC)
    data["year"] = np.full(len(data["event"]), year)

    data = select(data)

    if isMC:
        data["eventWeight"] = (
            data["genWeight"]
            * data["puweight"]
            * data["weight"]
            * data["id_wgt_mu_1"] * data["id_wgt_mu_2"]
            * data["iso_wgt_mu_1"] * data["iso_wgt_mu_2"]
        )

        data['id_MuonEffup']   = (data["id_wgt_mu_1__MuonEffup"]  * data["id_wgt_mu_2__MuonEffup"])  / (data["id_wgt_mu_1"] * data["id_wgt_mu_2"])
        data['id_MuonEffdown'] = (data["id_wgt_mu_1__MuonEffdown"]* data["id_wgt_mu_2__MuonEffdown"])/ (data["id_wgt_mu_1"] * data["id_wgt_mu_2"])
        data['iso_MuonEffup']  = (data["iso_wgt_mu_1__MuonEffup"] * data["iso_wgt_mu_2__MuonEffup"]) / (data["iso_wgt_mu_1"]* data["iso_wgt_mu_2"])
        data['iso_MuonEffdown']= (data["iso_wgt_mu_1__MuonEffdown"]* data["iso_wgt_mu_2__MuonEffdown"])/(data["iso_wgt_mu_1"]* data["iso_wgt_mu_2"])
    else:
        data["eventWeight"]      = data["weight"]
        data['id_MuonEffup']     = np.full(len(data["event"]), 1.0)
        data['id_MuonEffdown']   = np.full(len(data["event"]), 1.0)
        data['iso_MuonEffup']    = np.full(len(data["event"]), 1.0)
        data['iso_MuonEffdown']  = np.full(len(data["event"]), 1.0)
        data['PDF_uncertainty_down'] = np.full(len(data["event"]), 1.0)
        data['PDF_uncertainty_up']   = np.full(len(data["event"]), 1.0)
        data['qcd_unc_down']         = np.full(len(data["event"]), 1.0)
        data['qcd_unc_up']           = np.full(len(data["event"]), 1.0)

    data['nleptons'] = data['nelectrons'] + data['nmuons']

    label_map = {
        "2018": 2018,
        "2017": 2017,
        "2016": 2016,
        "2022": 2022,
        "2022EE": -2022,
        "2023": 2023,
        "2023BPix": -2023,
        "2024": 2024,
        "2025": 2025
    }
    data["source_year"] = np.full(len(data["event"]), label_map[year])

    #rm_notUsed=["diMu-mass_resolution_old","diMu-mass_resolution_abs_old", "diMu-mass_resolution_BSC_old", "diMu-mass_resolution_BSC_abs_old", "1oDiMuResolution_old", "1oDiMuResolution_BSC_old", "id_MuonEffup", "id_MuonEffdown", "iso_MuonEffup", "iso_MuonEffdown", "PDF_uncertainty_down", "PDF_uncertainty_up", "qcd_unc_down", "qcd_unc_up","GGH","VBF","VH","TTH"]
    rm_notUsed=["id_MuonEffup", "id_MuonEffdown", "iso_MuonEffup", "iso_MuonEffdown", "PDF_uncertainty_down", "PDF_uncertainty_up", "qcd_unc_down", "qcd_unc_up","GGH","VBF","VH","TTH","nmuons","nelectrons","nleptons","nbjets_loose","nbjets_mediumi","BSC_pt_1","BSC_pt_2","BSC_ptErr_1","BSC_ptErr_2","pt_kit_1","pt_kit_2","diMu_pt_kit","diMu_eta_kit","diMu_phi_kit","diMu_mass_kit","diMufsr_pt","diMufsr_eta","diMufsr_phi","diMufsr_mass","diMufsr_BSC_pt","diMufsr_BSC_eta","diMufsr_BSC_phi","diMufsr_BSC_mass","trg_single_mu24","Mu1_fsr_pt","Mu2_fsr_pt","Mu1_fsr_BSC_pt","Mu2_fsr_BSC_pt","mu1_fromH_bsConstrainedChi2","mu2_fromH_bsConstrainedChi2","nbjets_medium","nbjets_loose","H_pt","H_eta","H_phi","H_mass","mu1_fromH_pt","mu2_fromH_pt","mu1_fromH_ptErr","mu2_fromH_ptErr"]
    #rm_notUsed=["GGH","VBF","PDF_uncertainty","alphaS_uncertainty","iso_wgt_mu_1__MuonIDIsoDown","iso_wgt_mu_1__MuonIDIsoUp","iso_wgt_mu_2__MuonIDIsoDown","iso_wgt_mu_2__MuonIDIsoUp", "id_wgt_mu_1__MuonIDIsoDown","id_wgt_mu_1__MuonIDIsoUp","id_wgt_mu_2__MuonIDIsoDown","id_wgt_mu_2__MuonIDIsoUp","LHEScaleWeight_0","LHEScaleWeight_1","LHEScaleWeight_2","LHEScaleWeight_3","LHEScaleWeight_4","LHEScaleWeight_5","Generator_weight","trg_single_mu24", "id_MuonIDIsoUp", "id_MuonIDIsoDown", "iso_MuonIDIsoUp", "iso_MuonIDIsoDown"]
    # you already have 'branches' list in your code

    output = {branch: data[branch] for branch in branches}

    df = pd.DataFrame(output)

    # your region selections
    data_two_jet_m110To150_ggH = df[
        (df['GGH']) &
        (df['trg_single_mu24']) &
        (df['diMufsr_kit_BSC_mass'] > 110) & (df['diMufsr_kit_BSC_mass'] < 150)
    ]

    data_two_jet_m110To150_VBF = df[
        (df['VBF']) &
        (df['trg_single_mu24']) &
        (df['diMufsr_kit_BSC_mass'] > 110) & (df['diMufsr_kit_BSC_mass'] < 150)
    ]

    data_two_jet_m110To150_ggH = data_two_jet_m110To150_ggH.drop(columns=rm_notUsed, errors="ignore")
    data_two_jet_m110To150_VBF = data_two_jet_m110To150_VBF.drop(columns=rm_notUsed, errors="ignore")

    #return data_two_jet_m110To150_VBF
    return data_two_jet_m110To150_ggH, data_two_jet_m110To150_VBF
    #return data_two_jet_m110To150_ggH

def discover_systematics(input_file, tree_name="ntuple"):
    """
    Look in input_file:tree_name for branches starting with 'njets__'.
    Return a sorted list of syst names, where branch is 'njets__<syst>'.
    Only keep syst if jet1_pt__<syst> and jet2_pt__<syst> also exist.
    """
    with uproot.open(f"{input_file}:{tree_name}") as tree:
        all_branches = [k.decode() if isinstance(k, bytes) else k
                        for k in tree.keys()]

    syst_names = []
    for name in all_branches:
        if name.startswith("njets__"):
            syst = name.split("__", 1)[1]
            # check corresponding jet branches exist
            j1 = f"jet1_pt__{syst}"
            j2 = f"jet2_pt__{syst}"
            j1_e = f"jet1_eta__{syst}"
            j2_e = f"jet2_eta__{syst}"
            j1_p = f"jet1_phi__{syst}"
            j2_p = f"jet2_phi__{syst}"
            j1_m = f"jet1_mass__{syst}"
            j2_m = f"jet2_mass__{syst}"
            if j1 in all_branches and j2 in all_branches and j1_e in all_branches and j2_e in all_branches and j1_p in all_branches and j2_p in all_branches and j1_m in all_branches and j2_m in all_branches:
                syst_names.append(syst)
            else:
                print(f"WARNING: found {name} but missing {j1} or {j2}, skipping syst '{syst}'")

    syst_names = sorted(set(syst_names))
    print("Discovered systematics:", syst_names)
    return syst_names

def process_all(f, data, syst_list, year, isMC, weight, chunk_index):

    # ---- 1. Nominal processing ----
    data_nom = dict(data)
    df_nom_ggH, df_nom_VBF = process_chunk(data_nom, year, isMC, weight)
    #df_nom_VBF = process_chunk(data_nom, year, isMC, weight)

    if not df_nom_ggH.empty:
        if chunk_index == 0:
            f["data_two_jet_m110To150_ggH"] = df_nom_ggH
        else:
            f["data_two_jet_m110To150_ggH"].extend(df_nom_ggH)

    if not df_nom_VBF.empty:
        if chunk_index == 0:
            f["data_two_jet_m110To150_VBF"] = df_nom_VBF
        else:
            f["data_two_jet_m110To150_VBF"].extend(df_nom_VBF)

    # ---- 2. Systematic variations ----
    for syst in syst_list:
        data_var = dict(data)

        # overwrite nominal jet vars with shifted ones
        for base in ["njets", "jet1_pt", "jet2_pt", "jet1_eta", "jet2_eta", "jet1_phi", "jet2_phi", "jet1_mass", "jet2_mass"]:
            shifted = f"{base}__{syst}"
            if shifted not in data:
                print(f"Missing {shifted}, skipping {syst}")
                break
            data_var[base] = data[shifted]

        else:
            df_s_ggH, df_s_VBF = process_chunk_sys(data_var, year, isMC, weight)
            #df_s_VBF = process_chunk_sys(data_var, year, isMC, weight)

            name_ggH = f"data_two_jet_m110To150_ggH__{syst}"
            name_VBF = f"data_two_jet_m110To150_VBF__{syst}"

            if not df_s_ggH.empty:
                if chunk_index == 0:
                    f[name_ggH] = df_s_ggH
                else:
                    f[name_ggH].extend(df_s_ggH)

            if not df_s_VBF.empty:
                if chunk_index == 0:
                    f[name_VBF] = df_s_VBF
                else:
                    f[name_VBF].extend(df_s_VBF)

def main():
    
    args = getArgs()


    print("Now!!! Porcessing {:s} ......".format(args.input))
    lumi=getLumi(args.year)
    year=args.year
    #ShortName=(args.output).split('/')[-1].split('.root')[0]
    FullName=(args.input).split('/')[-1].split('.root')[0]
    ShortName=getShortName(FullName)

    if os.path.isfile(args.output): os.remove(args.output)

    initial_events = 0
    final_events = 0
    isSignal = 0
    isMC = 1
    if "HToMuMu" in args.input or "Hto2Mu" in args.input:
        isSignal = 1
    if "Muon" in args.input:
        isMC = 0
    if not isMC:  variables = data_vars
    elif isSignal:  variables = signal_vars
    else: variables = background_vars
    #else: variables = background_vars + ["ngenjets"]
    if isMC:
        variables += ["jet1_puIdDisc","jet2_puIdDisc","jet1_btagDeepFlavQG","jet2_btagDeepFlavQG","mu1_fromH_bsConstrainedChi2","mu2_fromH_bsConstrainedChi2","mu1_fromH_bsConstrainedPt","mu2_fromH_bsConstrainedPt","mu1_fromH_bsConstrainedPtErr","mu2_fromH_bsConstrainedPtErr","PDF_uncertainty_down","PDF_uncertainty_up","qcd_unc_down","qcd_unc_up","id_wgt_mu_1__MuonEffdown","id_wgt_mu_1__MuonEffup","iso_wgt_mu_1__MuonEffdown","iso_wgt_mu_1__MuonEffup", "id_wgt_mu_2__MuonEffdown","id_wgt_mu_2__MuonEffup","iso_wgt_mu_2__MuonEffdown","iso_wgt_mu_2__MuonEffup","n_jets_matched_genjet","genvbffilter_flag"]
        #if "DY" in ShortName:
        #    variables += ["genvbffilter_flag"]
        to_remove = ["pt_rc_bsc_1", "pt_rc_bsc_2","pt_rc_1","pt_rc_2","pt_kit_1","pt_kit_2"]
        #variables = [variable for variable in background_vars if "_rc" not in variable]
        variables = [v for v in variables if v not in to_remove]
        branches.update({"jet1_puIdDisc": float, "jet2_puIdDisc": float, "mu1_fromH_bsConstrainedChi2": float, "mu2_fromH_bsConstrainedChi2": float, "mu1_fromH_bsConstrainedPt": float, "mu2_fromH_bsConstrainedPt": float, "mu1_fromH_bsConstrainedPtErr": float, "mu2_fromH_bsConstrainedPtErr": float, "jet1_btagDeepFlavQG": float, "jet2_btagDeepFlavQG": float, "n_jets_matched_genjet": float, "genvbffilter_flag": float})
    else:
        variables += ["jet1_puIdDisc","jet2_puIdDisc","jet1_btagDeepFlavQG","jet2_btagDeepFlavQG","mu1_fromH_bsConstrainedChi2","mu2_fromH_bsConstrainedChi2","mu1_fromH_bsConstrainedPt","mu2_fromH_bsConstrainedPt","mu1_fromH_bsConstrainedPtErr","mu2_fromH_bsConstrainedPtErr"]
        to_remove = ["pt_rc_bsc_1", "pt_rc_bsc_2","pt_rc_1","pt_rc_2","pt_kit_1","pt_kit_2"]
        #variables = [variable for variable in background_vars if "_rc" not in variable]
        variables = [v for v in variables if v not in to_remove]
        branches.update({"jet1_puIdDisc": float, "jet2_puIdDisc": float, "mu1_fromH_bsConstrainedChi2": float, "mu2_fromH_bsConstrainedChi2": float, "mu1_fromH_bsConstrainedPt": float, "mu2_fromH_bsConstrainedPt": float, "mu1_fromH_bsConstrainedPtErr": float, "mu2_fromH_bsConstrainedPtErr": float, "jet1_btagDeepFlavQG": float, "jet2_btagDeepFlavQG": float})
    if year in ["2022", "2022EE", "2023", "2023BPix"]:
        to_remove_2223 = ["jet1_puIdDisc","jet2_puIdDisc"]
        variables = [v for v in variables if v not in to_remove_2223]
        for branch in to_remove_2223:
            branches.pop(branch, None)

#    for data in tqdm(read_root(args.input, key='DiMuonNtuple', columns=variables, chunksize=args.chunksize), desc='Processing %s' % args.input, bar_format='{desc}: {percentage:3.0f}%|{bar:20}{r_bar}'):

    #data = pd.read_parquet(args.input)
    print("Reading in ",end='',flush=True)
    file = uproot.open(args.input)
    print("Is signal: ", isSignal)
    print("Is MC: ", isMC)

    #sumW_fromTxT=True
    sumW_fromTxT=False

    if sumW_fromTxT:
        if isMC==1:
            root_path=args.input
            # extract year (4 digits)

            import re
            base = os.path.basename(root_path).replace(".root", "")
            #base = re.sub(r'flashsimNtuple_\d+\.root', 'flashsimNtuple', root_path)
            #base = "fullsimNtuple"
            # build txt path
            txt_path = os.path.join(
                os.path.dirname(root_path),
                #txt_path_1,
                "sumW",
                base + ".txt"
            )
            # read first line
            with open(txt_path, "r") as f:
                sumW = float(f.readline().strip())
            print(f"{base}: sumW = {sumW}")
            print("root_path: ",root_path)
            print("txt_path: ",txt_path)
        else:
            sumW = 1
    

    #GENW = file["conditions"]
    events = file["ntuple"]
    if not sumW_fromTxT:
        if isMC==1:
            GENW = file["conditions"]
            sumW = 0
            SumWeights = GENW["genEventSumw"].array(library="np")
            sumW = np.sum(SumWeights)
            #if isSignal==1:
            #    sumW = events.num_entries
            del GENW
        else:
            sumW = 1

    if isMC:
        if isSignal:
            weight = float(xs_sig[ShortName])/sumW*lumi
        else:
            weight = float(xs_bkg[ShortName])/sumW*lumi
    else:
        weight = 1.0

    print("weight: ", weight)
    #del GENW
    file.close()

    with uproot.recreate(args.output) as f:

        syst_list = discover_systematics(args.input, tree_name="ntuple")
        jet_vars = [
            "njets",
            "jet1_pt", "jet1_eta", "jet1_phi", "jet1_mass",
            "jet2_pt", "jet2_eta", "jet2_phi", "jet2_mass",
        ]
        for syst in syst_list:
            for v in jet_vars:
                varname = f"{v}__{syst}"
                variables.append(varname)

                ## detect integer vs float automatically
                #if "njets" in v:
                #    branches[varname] = np.int32
                #else:
                #    branches[varname] = np.float32
        #reso_correct=["diMu-mass_resolution","diMu-mass_resolution_abs", "diMu-mass_resolution_BSC", "diMu-mass_resolution_BSC_abs", "1oDiMuResolution", "1oDiMuResolution_BSC"]
        #for v in reso_correct:
        #    branches[v+"_old"] = np.float32

        for i, data in enumerate(
            uproot.iterate([args.input + ":ntuple"], expressions=variables, library="np", step_size="50 MB")
        ):

            # Now process this chunk safely
            print(f"Processing chunk with {len(data['event'])} events")
            #process_chunk(data, year, isMC, weight)
            #run_all_systematics(args.input, args.output, variables, year, isMC, weight):

            process_all(
                f=f,                    # <-- pass open file handle
                data=data,
                syst_list=syst_list,
                year=year,
                isMC=isMC,
                weight=weight,
                chunk_index=i,
            )


    print("Finished!!! Have gotten the skimmed data in {:s}".format(args.output))
    gc.collect()

if __name__ == '__main__':
    main()
