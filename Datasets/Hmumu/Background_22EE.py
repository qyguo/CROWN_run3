input_dir = "/publicfs/cms/data/hzz/guoqy/Hmumu/2022EE/After_hadd/"
input_dir = "/publicfs/cms/data/hzz/guoqy/Hmumu/2022EE/After_hadd_Inc_nbJetsnMuons/"
input_dir = "/publicfs/cms/data/hzz/guoqy/Hmumu/2022EE/After_hadd_Inc/"
xs_bkg = {}

background_samples = []
background_files = {}

sam = "DYJetsToLL_M50_madgraphMLM"
#sam = "DYJetsToLL_M50"
sam = "DY_50MLM"
sam_Full = "DYJetsToLL_M-50-madgraphMLM_2022EE_forPOG"
sam_Full = "DYJetsToLL_M-50-madgraphMLM_2022EE"
#xs_bkg[sam] = 6225.4
xs_bkg[sam] = 6345.99
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)

sam = "DYJetsToLL_M50_amcatnloFXFX"
sam = "DYJetsToLL_M50"
sam = "DY_50FxFx"
sam_Full = "DYto2L-2Jets_MLL-50_amcatnloFXFX_2022EE_ext1-v1"
xs_bkg[sam] = 6345.99
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)

sam = "DYto2Mu_50FxFx"
sam_Full = "DYto2Mu-2Jets_MLL-50_amcatnloFXFX_2024"
#xs_bkg[sam] = 2094.2
xs_bkg[sam] = 2091.7
#https://twiki.cern.ch/twiki/bin/viewauth/CMS/MATRIXCrossSectionsat13p6TeV
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)

sam = "DYto2Mu_MLL-50to120_powheg"
sam_Full = "DYto2Mu_MLL-50to120_powheg_2022EE"
xs_bkg[sam] = 2219
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)

sam = "DYto2Mu_MLL-120to200_powheg"
sam_Full = "DYto2Mu_MLL-120to200_powheg_2022EE"
xs_bkg[sam] = 21.65
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)

sam = "DYto2Mu-M105To160_FxFX"
sam = "DY_105To160"
sam_Full = "DYto2Mu-2Jets_MLL-105To160_amcatnloFXFX_2022EE"
xs_bkg[sam] = 48.196713
# 4.907e+01 pb * sf = 48.196713 pb
# 2091.7/2129.6 * 4.907e+01 
#xs_bkg[sam] = 48.03
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)

sam = "DY_105To160_No-VBF-Fil"
sam_Full = "DYto2Mu-2Jets_MLL-105To160_amcatnloFXFX_2022EE"
xs_bkg[sam] = 45.146972
# 48.03 - 2.083
# 48.196713 - 3.0497410 = 45.146972
#xs_bkg[sam] = 45.947000
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)

sam = "DY_105To160_VBF-Fil"
sam_Full = "DYto2Mu-2Jets_Bin-MLL-105to160_Fil-VBF_2022EE"
xs_bkg[sam] = 3.0497410
# 3.105 pb *sf = 3.0497410 pb
# 2091.7/2129.6 * 3.105 pb
#xs_bkg[sam] = 2.083
#48.03/47.12*2.043
#6345.99/6225.4*2.043
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)

#sam = "DYJetsToLL_M-105To160"
#sam_Full = "DYJetsToLL_M-105To160_TuneCP5_PSweights_13TeV-amcatnloFXFX_RunIIAutumn18"
#background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
#xs_bkg[sam] = 47.12
#sumW_bkg[sam] = read_sumW("%ssumW/%s.txt"%(input_dir,sam_Full))


sam = "EWK_LLJJ_M50"
background_files[sam] = "%sEWK_2L2J_TuneCH3_13p6TeV_madgraph-herwig7_2022EE.root"%(input_dir)
#xs_bkg[sam] = 0.0022907/0.0019621*1.029
#xs_bkg[sam] = 1.029
xs_bkg[sam] = 1.2013304
#sumW_bkg[sam] = read_sumW("%ssumW/EWK_2L2J_TuneCH3_13p6TeV_madgraph-herwig7_2022EE.txt"%(input_dir))

sam = "EWK_LLJJ_M105To160"
background_files[sam] = "%sEWK-2Mu2J_MLL-105To160_TuneCH3_13p6TeV_madgraph-herwig7_2024.root"%(input_dir)
#xs_bkg[sam] = 0.078
#xs_bkg[sam] = 0.0795
xs_bkg[sam] = 0.091062946
#sumW_bkg[sam] = read_sumW("%ssumW/EWK-2Mu2J_MLL-105To160_TuneCH3_13p6TeV_madgraph-herwig7_2024.txt"%(input_dir))

#sam = "GGToZZTo2e2mu"
#sam_Full = "GluGluToContinToZZTo2e2mu-mcfm701"
#background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
#xs_bkg[sam] = 0.00329
#sumW_bkg[sam] = read_sumW("%ssumW/%s.txt"%(input_dir,sam_Full))
#
#sam = "GGToZZTo2e2tau"
#sam_Full = "GluGluToContinToZZTo2e2tau-mcfm701"
#background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
#xs_bkg[sam] = 0.00329
#sumW_bkg[sam] = read_sumW("%ssumW/%s.txt"%(input_dir,sam_Full))
#
#sam = "GGToZZTo2mu2nu"
#sam_Full = "GluGluToContinToZZTo2mu2nu-mcfm701"
#background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
#xs_bkg[sam] = 0.001772
#sumW_bkg[sam] = read_sumW("%ssumW/%s.txt"%(input_dir,sam_Full))
#
#sam = "GGToZZTo2mu2tau"
#sam_Full = "GluGluToContinToZZTo2mu2tau-mcfm701"
#background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
#xs_bkg[sam] = 0.00329
#sumW_bkg[sam] = read_sumW("%ssumW/%s.txt"%(input_dir,sam_Full))
#
#sam = "GGToZZTo4mu"
#sam_Full = "GluGluToContinToZZTo4mu-mcfm701"
#background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
#xs_bkg[sam] = 0.001402
#sumW_bkg[sam] = read_sumW("%ssumW/%s.txt"%(input_dir,sam_Full))
#
#sam = "GGToZZTo4tau"
#sam_Full = "GluGluToContinToZZTo4tau-mcfm701"
#background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
#xs_bkg[sam] = 0.001402
#sumW_bkg[sam] = read_sumW("%ssumW/%s.txt"%(input_dir,sam_Full))
#
sam = "ZZTo4L"
sam_Full = "ZZto4L_powheg_2022EE_ext1-v2"
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
xs_bkg[sam] = 1.65

sam = "ZZTo2L2Nu"
sam_Full = "ZZto2L2Nu_powheg_2022EE_ext1-v2"
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
xs_bkg[sam] = 1.19

sam = "WWTo2L2Nu"
sam_Full = "WWto2L2Nu_powheg_2022EE_ext1-v2"
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
xs_bkg[sam] = 12.98

sam = "WZTo3LNu"
sam_Full = "WZto3LNu_powheg_2022EE"
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
xs_bkg[sam] =  5.31

sam = "ZZTo2L2Q"
sam_Full = "ZZto2L2Q_powheg_2022EE_ext1-v2"
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
xs_bkg[sam] = 8.08

sam = "WZTo2L2Q"
sam_Full = "WZto2L2Q_powheg_2022EE_ext1-v2"
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
xs_bkg[sam] = 8.17

sam = "WWW"
sam_Full = "WWW_4F_amcatnlo-madspin_2022EE"
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
xs_bkg[sam] = 0.2328

sam = "WWZ"
sam_Full = "WWZ_4F_amcatnlo_2022EE"
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
xs_bkg[sam] = 0.1851

sam = "WZZ"
sam_Full = "WZZ_amcatnlo_2022EE"
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
xs_bkg[sam] = 0.06206

sam = "ZZZ"
sam_Full = "ZZZ_amcatnlo_2022EE"
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
xs_bkg[sam] = 0.01591

sam = "TTTo2L2Nu"
sam_Full = "TTto2L2Nu_powheg_2022EE_ext1-v2"
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
xs_bkg[sam] = 97.4488

#sam = "TTToSemiLep"
#sam_Full = "TTToSemiLeptonic-powheg"
#background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
#xs_bkg[sam] = 358.57
#sumW_bkg[sam] = read_sumW("%ssumW/%s.txt"%(input_dir,sam_Full))

sam = "ST_tW_top"
#sam_Full = "ST_tW_top_5f_inclusiveDecays-powheg"
sam_Full = "TWminusto2L2Nu_powheg_2022EE_ext1-v2"
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
#xs_bkg[sam] = 35.99
xs_bkg[sam] = 4.6511

sam = "ST_tW_antitop"
#sam_Full = "ST_tW_antitop_5f_inclusiveDecays-powheg"
sam_Full = "TbarWplusto2L2Nu_powheg_2022EE_ext1-v2"
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
#xs_bkg[sam] = 36.05
xs_bkg[sam] = 4.6511

#sam = "ST_t-channel_top"
#sam_Full = "ST_t-channel_top_5f_InclusiveDecays-powheg"
#background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
#xs_bkg[sam] = 136.02
#sumW_bkg[sam] = read_sumW("%ssumW/%s.txt"%(input_dir,sam_Full))
#
#sam = "ST_t-channel_antitop"
#sam_Full = "ST_t-channel_antitop_5f_InclusiveDecays-powheg"
#background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
#xs_bkg[sam] = 80.95
#sumW_bkg[sam] = read_sumW("%ssumW/%s.txt"%(input_dir,sam_Full))
#
#sam = "ST_s-channel"
#sam_Full = "ST_s-channel_4f_leptonDecays-amcatnlo"
#background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
#xs_bkg[sam] = 3.40
#sumW_bkg[sam] = read_sumW("%ssumW/%s.txt"%(input_dir,sam_Full))

sam = "tZq"
#sam_Full = "tZq_ll_4f_ckm_NLO-madgraph_RunIIAutumn18_ext1-v1"
sam_Full = "TZQB-4FS_OnshellZ_amcatnlo_2022EE"
background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
xs_bkg[sam] = 0.0801

#good 
#sam = ""
#sam_Full = ""
#background_files[sam] = "%s%s.root"%(input_dir,sam_Full)
#xs_bkg[sam] = 
#sumW_bkg[sam] = read_sumW("%ssumW/%s.txt"%(input_dir,sam_Full))

#good 
#background_samples = ["GGToZZTo2e2mu","GGToZZTo2mu2nu","GGToZZTo2mu2tau","GGToZZTo4mu","ZZTo4L","ZZTo2L2Nu","WZTo3LNu","ZZTo2L2Q","WZTo2L2Q","WWTo2L2Nu","WWW","TTTo2L2Nu","TTToSemiLep","ST_tW_top","ST_tW_antitop","ST_t-channel_top","ST_t-channel_antitop","ST_s-channel","tZq","EWK_LLJJ_M50","EWK_LLJJ_M105-160","DYJetsToLL_M-105To160","DYJetsToLL_M50"]
background_samples = ["ZZTo4L","ZZTo2L2Nu","WZTo3LNu","ZZTo2L2Q","WZTo2L2Q","WWTo2L2Nu","WWW","WWZ","WZZ","ZZZ","TTTo2L2Nu","ST_tW_top","ST_tW_antitop","tZq","DYJetsToLL_M50"]
background_samples = ["ZZTo4L","ZZTo2L2Nu","WZTo3LNu","ZZTo2L2Q","WZTo2L2Q","WWTo2L2Nu","WWW","WWZ","WZZ","ZZZ","TTTo2L2Nu","ST_tW_top","ST_tW_antitop","DYJetsToLL_M50"]
#background_samples = ["ZZTo4L","ZZTo2L2Nu","WZTo3LNu","ZZTo2L2Q","WZTo2L2Q","WWTo2L2Nu","WWW","WWZ","WZZ","ZZZ","TTTo2L2Nu","ST_tW_top","ST_tW_antitop","DYto2Mu_MLL-120to200_powheg","DYto2Mu_MLL-50to120_powheg"]


background_vars = [
"Flag_DiMuonFromHiggs",
"Flag_LeptonChargeSumVeto",
#"Flag_dimuon_Zmass_veto",
"H_eta",
"H_mass",
"H_phi",
"H_pt",
"dijet_eta",
"dijet_mass",
"event",
"genWeight",
"genmet_phi",
"genmet_pt",
#"is_data",
#"is_diboson",
#"is_dyjets",
#"is_embedding",
#"is_gghmm",
#"is_top",
#"is_triboson",
#"is_vbfhmm",
#"is_vhmm",
#"is_wjets",
#"is_zjjew",
"jet1_eta",
"jet1_mass",
"jet1_phi",
"jet1_pt",
"jet2_eta",
"jet2_mass",
"jet2_phi",
"jet2_pt",
"lumi",
"met_phi",
"met_pt",
"mu1_fromH_eta",
"mu1_fromH_phi",
"mu1_fromH_pt",
"mu1_mu2_dphi",
"mu2_fromH_eta",
"mu2_fromH_phi",
"mu2_fromH_pt",
"mumuH_dR",
"nbjets_loose",
"nbjets_medium",
"nelectrons",
"njets",
"nmuons",
"puweight",
"run",
"trg_single_mu24",
#"trg_single_mu27",
"id_wgt_mu_1",
"id_wgt_mu_2",
"iso_wgt_mu_1",
"iso_wgt_mu_2",
"mu1_fromH_ptErr",
"mu2_fromH_ptErr",
"pt_rc_1",
"pt_rc_2",
#"prefiring_wgt",
"fsrPhoton_pt_1",
"fsrPhoton_eta_1",
"fsrPhoton_phi_1",
"fsrPhoton_dROverEt2_1",
"fsrPhoton_relIso03_1",
"fsrPhoton_pt_2",
"fsrPhoton_eta_2",
"fsrPhoton_phi_2",
"fsrPhoton_dROverEt2_2",
"fsrPhoton_relIso03_2",
"SoftActivityJetNjets5",
#"jet1_qgl",
#"jet2_qgl",
#"jet1_rawMass",
#"jet2_rawMass",
#"jet1_rawpT",
#"jet2_rawpT",
#"BSC_pt_1",
#"BSC_pt_2",
#"BSC_pt_rc_1",
#"BSC_pt_rc_2",
#"BSC_pt_roc_1",
#"BSC_pt_roc_2",
#"pt_roc_1",
#"pt_roc_2",
#"BSC_ptErr_1",
#"BSC_ptErr_2",
#"BSC_Chi2_1",
#"BSC_Chi2_2",
#"PDF_uncertainty_down",
#"PDF_uncertainty_up",
#"qcd_unc_down",
#"qcd_unc_up",
#"id_wgt_mu_1__MuonEffdown",
#"id_wgt_mu_1__MuonEffup",
#"iso_wgt_mu_1__MuonEffdown",
#"iso_wgt_mu_1__MuonEffup",
#"id_wgt_mu_2__MuonEffdown",
#"id_wgt_mu_2__MuonEffup",
#"iso_wgt_mu_2__MuonEffdown",
#"iso_wgt_mu_2__MuonEffup",
#"pt_kit_1",
#"pt_kit_2",
#"BSC_pt_kit_1",
#"BSC_pt_kit_2",
"mu1_fromH_bsConstrainedChi2",
"mu2_fromH_bsConstrainedChi2",
"mu1_fromH_bsConstrainedPt",
"mu2_fromH_bsConstrainedPt",
"pt_kit_bsc_1",
"pt_kit_bsc_2",
"pt_kit_1",
"pt_kit_2",
#"pt_bsc_1",
#"pt_bsc_2",
"pt_rc_bsc_1",
"pt_rc_bsc_2",
]

