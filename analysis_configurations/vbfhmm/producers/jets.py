from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

####################
# Set of producers used for selection possible good jets
####################

### energy corrections
# vh these pT corrections are copied from Htautau
# TODO check if L1FastJet L2L3 and residual corrections are consistent with hmm
JetPtCorrection = Producer(
    name="JetPtCorrection",
    call="physicsobject::jet::JetPtCorrection({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected],
    scopes=["global"],
)
JetPtCorrection_2022 = Producer(
    name="JetPtCorrection_2022",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected],
    scopes=["global"],
)
####v15
JetPtCorrection_2022_v15 = Producer(
    name="JetPtCorrection_2022_v15",
    call="physicsobject::jet::JetPtCorrection_2022_v15({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        #nanoAOD.Jet_ID,
        q.jet_id_v15,
        nanoAOD.Jet_neEmEF,
        nanoAOD.Jet_chEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected],
    scopes=["global"],
)
####v15
# jet correction additional modification of pt<30 GeV of |eta| in (2,2.5)region.
JetPtCorrection_2022_v15_v2 = Producer(
    name="JetPtCorrection_2022_v15_v2",
    call="physicsobject::jet::JetPtCorrection_2022_v15_v2({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        #nanoAOD.Jet_ID,
        q.jet_id_v15,
        nanoAOD.Jet_neEmEF,
        nanoAOD.Jet_chEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected],
    scopes=["global"],
)

# 2025 new SFUncertainty
# jet correction additional modification of pt<30 GeV of |eta| in (2,2.5)region.
JetPtCorrection_2022_v15_v3 = Producer(
    name="JetPtCorrection_2022_v15_v3",
    call="physicsobject::jet::JetPtCorrection_2022_v15_v3({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo}, {jet_veto_map}, {jet_veto_tag}, {jet_horn_veto}, {jet_horn_eta_min}, {jet_horn_eta_max}, {jet_horn_veto_max_pt}, {jet_horn_jer_genmatch_only})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        #nanoAOD.Jet_ID,
        q.jet_id_v15,
        nanoAOD.Jet_neEmEF,
        nanoAOD.Jet_chEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected],
    scopes=["global"],
)
####
JetPtCorrection_2022_GenMatch = Producer(
    name="JetPtCorrection_2022_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected],
    scopes=["global"],
)
#
JetMassCorrection = Producer(
    name="JetMassCorrection",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected,
    ],
    output=[q.Jet_mass_corrected],
    scopes=["global"],
)
JetEnergyCorrection = ProducerGroup(
    name="JetEnergyCorrection",
    call=None,
    input=None,
    output=None,
    scopes=["global"],
    subproducers=[JetPtCorrection, JetMassCorrection],
)
JetEnergyCorrection_2022 = ProducerGroup(
    name="JetEnergyCorrection_2022",
    call=None,
    input=None,
    output=None,
    scopes=["global"],
    subproducers=[JetPtCorrection_2022, JetMassCorrection],
)
JetEnergyCorrection_2022_v15 = ProducerGroup(
    name="JetEnergyCorrection_2022_v15",
    call=None,
    input=None,
    output=None,
    scopes=["global"],
    subproducers=[JetPtCorrection_2022_v15, JetMassCorrection],
)
JetEnergyCorrection_2022_v15_v2 = ProducerGroup(
    name="JetEnergyCorrection_2022_v15_v2",
    call=None,
    input=None,
    output=None,
    scopes=["global"],
    subproducers=[JetPtCorrection_2022_v15_v2, JetMassCorrection],
)
JetEnergyCorrection_2022_v15_v3 = ProducerGroup(
    name="JetEnergyCorrection_2022_v15_v3",
    call=None,
    input=None,
    output=None,
    scopes=["global"],
    subproducers=[JetPtCorrection_2022_v15_v3, JetMassCorrection],
)
#
JetEnergyCorrection_2022_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global"],
    subproducers=[JetPtCorrection_2022_GenMatch, JetMassCorrection],
)
#
JetPtCorrection_data_2022 = Producer(
    name="JetPtCorrection_data_2022",
    #call="physicsobject::jet::JetPtCorrection_data_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_data_2022({df}, {output}, {input}, {jet_jec_file}, {jet_jes_tag_data}, {jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        #nanoAOD.rho,
        q.jet_id_v15,
        nanoAOD.Jet_neEmEF,
        nanoAOD.Jet_chEmEF,
    ],
    output=[q.Jet_pt_corrected],
    scopes=["global"],
)
JetPtCorrection_data_2024 = Producer(
    name="JetPtCorrection_data_2024",
    #call="physicsobject::jet::JetPtCorrection_data_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_data_2024({df}, {output}, {input}, {jet_jec_file}, {jet_jes_tag_data}, {jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        q.jet_id_v15,
        nanoAOD.rho,
        nanoAOD.Jet_neEmEF,
        nanoAOD.Jet_chEmEF,
        nanoAOD.run,
    ],
    output=[q.Jet_pt_corrected],
    scopes=["global"],
)
JetPtCorrection_data_2025 = Producer(
    name="JetPtCorrection_data_2025",
    #call="physicsobject::jet::JetPtCorrection_data_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_data_2025({df}, {output}, {input}, {jet_jec_file}, {jet_jes_tag_data}, {jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        q.jet_id_v15,
        nanoAOD.rho,
        nanoAOD.Jet_neEmEF,
        nanoAOD.Jet_chEmEF,
        nanoAOD.run,
    ],
    output=[q.Jet_pt_corrected],
    scopes=["global"],
)
##
JetEnergyCorrection_data_2022 = ProducerGroup(
    name="JetEnergyCorrection_data_2022",
    call=None,
    input=None,
    output=None,
    scopes=["global"],
    subproducers=[JetPtCorrection_data_2022, JetMassCorrection],
)
JetEnergyCorrection_data_2024 = ProducerGroup(
    name="JetEnergyCorrection_data_2024",
    call=None,
    input=None,
    output=None,
    scopes=["global"],
    subproducers=[JetPtCorrection_data_2024, JetMassCorrection],
)
JetEnergyCorrection_data_2025 = ProducerGroup(
    name="JetEnergyCorrection_data_2025",
    call=None,
    input=None,
    output=None,
    scopes=["global"],
    subproducers=[JetPtCorrection_data_2025, JetMassCorrection],
)
# in data and embdedded sample, we simply rename the nanoAOD jets to the jet_pt_corrected column
RenameJetPt = Producer(
    name="RenameJetPt",
    call="basefunctions::rename<ROOT::RVec<float>>({df}, {input}, {output})",
    input=[nanoAOD.Jet_pt],
    output=[q.Jet_pt_corrected],
    scopes=["global"],
)
RenameJetMass = Producer(
    name="RenameJetMass",
    call="basefunctions::rename<ROOT::RVec<float>>({df}, {input}, {output})",
    input=[nanoAOD.Jet_mass],
    output=[q.Jet_mass_corrected],
    scopes=["global"],
)
RenameJetsData = ProducerGroup(
    name="RenameJetsData",
    call=None,
    input=None,
    output=None,
    scopes=["global"],
    subproducers=[RenameJetPt, RenameJetMass],
)
### selecting jets

JetPtCut = Producer(
    name="JetPtCut",
    call="physicsobject::CutPt({df}, {input}, {output}, {min_jet_pt})",
    input=[q.Jet_pt_corrected],
    output=[],
    scopes=["global"],
)
BJetPtCut = Producer(
    name="BJetPtCut",
    call="physicsobject::CutPt({df}, {input}, {output}, {min_bjet_pt})",
    input=[q.Jet_pt_corrected],
    output=[],
    scopes=["global"],
)
JetEtaCut = Producer(
    name="JetEtaCut",
    call="physicsobject::CutEta({df}, {input}, {output}, {max_jet_eta})",
    input=[nanoAOD.Jet_eta],
    output=[],
    scopes=["global"],
)
BJetEtaCut = Producer(
    name="BJetEtaCut",
    call="physicsobject::CutEta({df}, {input}, {output}, {max_bjet_eta})",
    input=[nanoAOD.Jet_eta],
    output=[],
    scopes=["global"],
)
JetIDCut = Producer(
    name="JetIDCut",
    call="physicsobject::jet::CutID({df}, {output}, {input}, {jet_id})",
    input=[nanoAOD.Jet_ID],
    output=[q.jet_id_mask],
    scopes=["global"],
)
RenameJetID_v12 = Producer(
    name="RenameJetID_v12",
    call="basefunctions::rename<ROOT::RVec<UChar_t>>({df}, {input}, {output})",
    input=[nanoAOD.Jet_ID],
    output=[q.jet_id_v15],
    scopes=["global"],
)
JetPUIDCut = Producer(
    name="JetPUIDCut",
    call="physicsobject::jet::CutPUID({df}, {output}, {input}, {jet_puid}, {jet_puid_max_pt})",
    input=[nanoAOD.Jet_PUID, q.Jet_pt_corrected],
    output=[q.jet_puid_mask],
    scopes=["global"],
)
BTagCutLoose = Producer(
    name="BTagCutLoose",
    call="physicsobject::jet::CutRawID({df}, {input}, {output}, {btag_cut_loose})",
    input=[nanoAOD.BJet_discriminator],
    output=[],
    scopes=["global"],
)
BTagCutMedium = Producer(
    name="BTagCutMedium",
    call="physicsobject::jet::CutRawID({df}, {input}, {output}, {btag_cut_medium})",
    input=[nanoAOD.BJet_discriminator],
    output=[],
    scopes=["global"],
)
# v15 UParTAK4
BTagCutLoose = Producer(
    name="BTagCutLoose",
    call="physicsobject::jet::CutRawID({df}, {input}, {output}, {btag_cut_loose})",
    input=[nanoAOD.BJet_discriminator_v15],
    output=[],
    scopes=["global"],
)
BTagCutMedium = Producer(
    name="BTagCutMedium",
    call="physicsobject::jet::CutRawID({df}, {input}, {output}, {btag_cut_medium})",
    input=[nanoAOD.BJet_discriminator_v15],
    output=[],
    scopes=["global"],
)

# vh veto overlapping jets against muons
# TODO this runs over all jets, not efficient!!!
# need to run over only good jets
VetoOverlappingJetsWithMuons = Producer(
    name="VetoOverlappingJetsWithMuons",
    call="jet::VetoOverlappingJets({df}, {output}, {input}, {deltaR_jet_veto})",
    input=[nanoAOD.Jet_eta, nanoAOD.Jet_phi, nanoAOD.Muon_eta, nanoAOD.Muon_phi, q.base_muons_mask], # vh base or good muon?
    output=[q.jet_overlap_veto_mask],
    scopes=["global"],
)

GoodJets = ProducerGroup(
    name="GoodJets",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[],
    output=[q.good_jets_mask],
    scopes=["global"],
    subproducers=[JetPtCut, JetEtaCut, JetIDCut, JetPUIDCut, VetoOverlappingJetsWithMuons],
)
### As now 2022 data has no Jet_puID, so no possible to do JetPUIDCut
GoodJets_2022 = ProducerGroup(
    name="GoodJets_2022",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[],
    output=[q.good_jets_mask],
    scopes=["global"],
    subproducers=[JetPtCut, JetEtaCut, JetIDCut, VetoOverlappingJetsWithMuons],
)

JetIdTightLepVeto_Cut = Producer(
    name="JetIdTightLepVeto_Cut",
    call="physicsobject::jet::JetIdTightLepVeto_Cut({df}, {output}, {input})",
    input=[nanoAOD.Jet_eta, nanoAOD.Jet_ID, nanoAOD.Jet_neHEF, nanoAOD.Jet_neEmEF, nanoAOD.Jet_muEF, nanoAOD.Jet_chEmEF],
    output=[q.jet_id_mask],
    scopes=["global"],
)
### nanoAOD v13 14 15
### https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetID13p6TeV#nanoAOD_Flags
JetIdTightLepVeto_Cut_v15 = Producer(
    name="JetIdTightLepVeto_Cut_v15",
    call="physicsobject::jet::JetIdTightLepVeto_Cut_v15({df}, {output}, {input})",
    input=[nanoAOD.Jet_eta, nanoAOD.Jet_neHEF, nanoAOD.Jet_neEmEF, nanoAOD.Jet_chMultiplicity, nanoAOD.Jet_neMultiplicity, nanoAOD.Jet_chHEF, nanoAOD.Jet_muEF, nanoAOD.Jet_chEmEF],
    #output=[q.jet_id_mask],
    output=[q.jet_id_v15],
    scopes=["global"],
)
JetIDCut_v15 = Producer(
    name="JetIDCut_v15",
    call="physicsobject::jet::CutID({df}, {output}, {input}, static_cast<UChar_t>({jet_id}))",
    input=[q.jet_id_v15],
    output=[q.jet_id_mask],
    scopes=["global"],
)
GoodJets_2022_JetIdTightLepVeto_v15 = ProducerGroup(
    name="GoodJets_2022_JetIdTightLepVeto_v15",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[],
    output=[q.good_jets_mask],
    scopes=["global"],
    subproducers=[JetPtCut, JetEtaCut, JetIDCut_v15, VetoOverlappingJetsWithMuons],
)
##
GoodJets_2022_JetIdTightLepVeto = ProducerGroup(
    name="GoodJets_2022_JetIdTightLepVeto",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[],
    output=[q.good_jets_mask],
    scopes=["global"],
    subproducers=[JetPtCut, JetEtaCut, JetIdTightLepVeto_Cut, VetoOverlappingJetsWithMuons],
)

### GEN jet
GEN_JetPtCut = Producer(
    name="GEN_JetPtCut",
    call="physicsobject::CutPt({df}, {input}, {output}, {min_genjet_pt})",
    input=[nanoAOD.GenJet_pt],
    output=[],
    scopes=["vbfhmm"],
)
GEN_JetEtaCut = Producer(
    name="GEN_JetEtaCut",
    call="physicsobject::CutEta({df}, {input}, {output}, {max_genjet_eta})",
    input=[nanoAOD.GenJet_eta],
    output=[],
    scopes=["vbfhmm"],
)
GEN_GoodJets = ProducerGroup(
    name="GEN_GoodJets",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[],
    output=[q.good_genjets_mask],
    scopes=["vbfhmm"],
    subproducers=[GEN_JetPtCut, GEN_JetEtaCut],
)

## jet collection
#GEN_JetCollection = Producer(
#    name="GEN_JetCollection",
#    call="jet::OrderJetsByPt({df}, {output}, {input})",
#    input=[nanoAOD.GenJet_pt, q.good_genjets_mask],
#    output=[q.good_genjet_collection],
#    scopes=["vbfhmm"],
#)
NumberOfGoodGENJets = Producer(
    name="NumberOfGoodGENJets",
    call="quantities::NumberOfGoodObjects({df}, {output}, {input})",
    input=[q.good_genjets_mask],
    output=[q.ngenjets],
    scopes=["vbfhmm"],
)

###
### dy gen level checking the vbf filter or not with a flag
GEN_vbffilter = ProducerGroup(
    name="GEN_vbffilter",
    call=None,
    input=None,
    output=None,
    scopes=["global","vbfhmm"],
    subproducers=[
        Producer(
            name="genvbffilter_flag",
            call=(
                "physicsobject::jet::VBFGenJetFilterFlag("
                "{df}, {output}, {input}, true)"
                # "{df}, correctionManager, {output}, {input}, true)"
                # the true here is the setting in DY_vbf-filter sample
                # leadJetsNoLepMass = cms.untracked.bool ( True), # Require the cut on the mass of the leading jets consist with DY_vbf-filter sample
                # https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_fragment/HIG-RunIII2024Summer24wmLHEGS-01941/0
            ),
            input=[
                nanoAOD.GenJet_pt,
                nanoAOD.GenJet_eta,
                nanoAOD.GenJet_phi,
                nanoAOD.GenJet_mass,
                nanoAOD.GenParticle_pdgId,
                nanoAOD.GenParticle_eta,
                nanoAOD.GenParticle_phi,
                nanoAOD.GenParticle_statusFlags,
            ],
            output=[q.genvbffilter_flag],
            scopes=["global","vbfhmm"],
        ),
    ],
)
###
##checking the jet1 and jet2 macthed genjets
MatchedGenJetPt1 = Producer(
    name="MatchedGenJetPt1",
    #call="physicsobject::jet::MatchedGenJetFloat({df}, correctionManager, {output}, {input}, 0)",
    call="physicsobject::jet::MatchedGenJetFloat({df}, {output}, {input}, 0)",
    input=[
        q.good_jet_collection,
        nanoAOD.Jet_associatedGenJet,
        nanoAOD.GenJet_pt,
    ],
    output=[q.genjet_pt_1],
    scopes=["global", "vbfhmm"],
)

MatchedGenJetEta1 = Producer(
    name="MatchedGenJetEta1",
    call="physicsobject::jet::MatchedGenJetFloat({df}, {output}, {input}, 0)",
    input=[
        q.good_jet_collection,
        nanoAOD.Jet_associatedGenJet,
        nanoAOD.GenJet_eta,
    ],
    output=[q.genjet_eta_1],
    scopes=["global", "vbfhmm"],
)

MatchedGenJetPhi1 = Producer(
    name="MatchedGenJetPhi1",
    call="physicsobject::jet::MatchedGenJetFloat({df}, {output}, {input}, 0)",
    input=[
        q.good_jet_collection,
        nanoAOD.Jet_associatedGenJet,
        nanoAOD.GenJet_phi,
    ],
    output=[q.genjet_phi_1],
    scopes=["global", "vbfhmm"],
)

MatchedGenJetMass1 = Producer(
    name="MatchedGenJetMass1",
    call="physicsobject::jet::MatchedGenJetFloat({df}, {output}, {input}, 0)",
    input=[
        q.good_jet_collection,
        nanoAOD.Jet_associatedGenJet,
        nanoAOD.GenJet_mass,
    ],
    output=[q.genjet_mass_1],
    scopes=["global", "vbfhmm"],
)


MatchedGenJetPt2 = Producer(
    name="MatchedGenJetPt2",
    call="physicsobject::jet::MatchedGenJetFloat({df}, {output}, {input}, 1)",
    input=[
        q.good_jet_collection,
        nanoAOD.Jet_associatedGenJet,
        nanoAOD.GenJet_pt,
    ],
    output=[q.genjet_pt_2],
    scopes=["global", "vbfhmm"],
)

MatchedGenJetEta2 = Producer(
    name="MatchedGenJetEta2",
    call="physicsobject::jet::MatchedGenJetFloat({df}, {output}, {input}, 1)",
    input=[
        q.good_jet_collection,
        nanoAOD.Jet_associatedGenJet,
        nanoAOD.GenJet_eta,
    ],
    output=[q.genjet_eta_2],
    scopes=["global", "vbfhmm"],
)

MatchedGenJetPhi2 = Producer(
    name="MatchedGenJetPhi2",
    call="physicsobject::jet::MatchedGenJetFloat({df}, {output}, {input}, 1)",
    input=[
        q.good_jet_collection,
        nanoAOD.Jet_associatedGenJet,
        nanoAOD.GenJet_phi,
    ],
    output=[q.genjet_phi_2],
    scopes=["global", "vbfhmm"],
)

MatchedGenJetMass2 = Producer(
    name="MatchedGenJetMass2",
    call="physicsobject::jet::MatchedGenJetFloat({df}, {output}, {input}, 1)",
    input=[
        q.good_jet_collection,
        nanoAOD.Jet_associatedGenJet,
        nanoAOD.GenJet_mass,
    ],
    output=[q.genjet_mass_2],
    scopes=["global", "vbfhmm"],
)


NMatchedGenJetsJet1Jet2 = Producer(
    name="NMatchedGenJetsJet1Jet2",
    call="physicsobject::jet::NMatchedGenJetsJet1Jet2({df}, {output}, {input})",
    input=[
        q.good_jet_collection,
        nanoAOD.Jet_associatedGenJet,
        nanoAOD.GenJet_pt,
    ],
    output=[q.n_jets_matched_genjet],
    scopes=["global", "vbfhmm"],
)


MatchedGenJetVariables = ProducerGroup(
    name="MatchedGenJetVariables",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[
        MatchedGenJetPt1,
        MatchedGenJetEta1,
        MatchedGenJetPhi1,
        MatchedGenJetMass1,
        MatchedGenJetPt2,
        MatchedGenJetEta2,
        MatchedGenJetPhi2,
        MatchedGenJetMass2,
        NMatchedGenJetsJet1Jet2,
    ],
)

GoodBJetsLoose = ProducerGroup(
    name="GoodBJetsLoose",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[q.good_jets_mask],
    output=[q.good_bjets_mask_loose],
    scopes=["global"],
    subproducers=[BJetPtCut, BJetEtaCut, BTagCutLoose],
)
GoodBJetsMedium = ProducerGroup(
    name="GoodBJetsMedium",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[q.good_bjets_mask_loose],
    output=[q.good_bjets_mask_medium],
    scopes=["global"],
    subproducers=[BTagCutMedium],
)

NumberOfLooseB = Producer(
    name="NumberOfLooseB",
    call="quantities::NumberOfGoodObjects({df}, {output}, {input})",
    input=[q.good_bjets_mask_loose],
    output=[q.nbjets_loose],
    scopes=["global"],
)
NumberOfMediumB = Producer(
    name="NumberOfMediumB",
    call="quantities::NumberOfGoodObjects({df}, {output}, {input})",
    input=[q.good_bjets_mask_medium],
    output=[q.nbjets_medium],
    scopes=["global"],
)
# define MHT from good_jet_collection
Calc_MHT = Producer(
    name="Calc_MHT",
    call="physicsobject::MHT_Calculation({df}, {output}, {input})",
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected,
        q.good_jet_collection,
    ],
    output=[q.MHT_p4],
    scopes=["global","e2m","m2m"],
)
# n jets ouput
NumberOfGoodJets = Producer(
    name="NumberOfGoodJets",
    call="quantities::NumberOfGoodObjects({df}, {output}, {input})",
    input=[q.good_jets_mask],
    output=[q.njets],
    scopes=["global"],
)
##
Jet1_QGdiscriminator = Producer(
    name="Jet1_QGdiscriminator",
    call="quantities::ptErr({df}, {output}, 0, {input})",
    input=[q.good_jet_collection, nanoAOD.Jet_QGdiscriminator],
    output=[q.jet1_btagDeepFlavQG],
    scopes=["global","vbfhmm"],
)
Jet2_QGdiscriminator = Producer(
    name="Jet2_QGdiscriminator",
    call="quantities::ptErr({df}, {output}, 1, {input})",
    input=[q.good_jet_collection, nanoAOD.Jet_QGdiscriminator],
    output=[q.jet2_btagDeepFlavQG],
    scopes=["global","vbfhmm"],
)
#Jet1_qgl = Producer(
#    name="Jet1_qgl",
#    call="quantities::ptErr({df}, {output}, 0, {input})",
#    input=[q.good_jet_collection, nanoAOD.Jet_qgl],
#    output=[q.jet1_qgl],
#    scopes=["vbfhmm"],
#)
#Jet2_qgl = Producer(
#    name="Jet2_qgl",
#    call="quantities::ptErr({df}, {output}, 1, {input})",
#    input=[q.good_jet_collection, nanoAOD.Jet_qgl],
#    output=[q.jet2_qgl],
#    scopes=["vbfhmm"],
#)
###ah
# jet collection
JetCollection = Producer(
    name="JetCollection",
    call="jet::OrderJetsByPt({df}, {output}, {input})",
    input=[q.Jet_pt_corrected, q.good_jets_mask],
    output=[q.good_jet_collection],
    scopes=["global"],
)
##raw jet
Jet1_rawpT = Producer(
    name="Jet1_rawpT",
    call="basefunctions::getvar<float>({df}, {output}, 0, {input})",
    input=[q.good_jet_collection, nanoAOD.Jet_pt],
    output=[q.jet1_rawpT],
    scopes=["global","vbfhmm"],
)
Jet2_rawpT = Producer(
    name="Jet2_rawpT",
    call="basefunctions::getvar<float>({df}, {output}, 1, {input})",
    input=[q.good_jet_collection, nanoAOD.Jet_pt],
    output=[q.jet2_rawpT],
    scopes=["global","vbfhmm"],
)
Jet1_rawMass = Producer(
    name="Jet1_rawMass",
    call="basefunctions::getvar<float>({df}, {output}, 0, {input})",
    input=[q.good_jet_collection, nanoAOD.Jet_mass],
    output=[q.jet1_rawMass],
    scopes=["global","vbfhmm"],
)
Jet2_rawMass = Producer(
    name="Jet2_rawMass",
    call="basefunctions::getvar<float>({df}, {output}, 1, {input})",
    input=[q.good_jet_collection, nanoAOD.Jet_mass],
    output=[q.jet2_rawMass],
    scopes=["global","vbfhmm"],
)
#Jet PU 

Jet1_puIdDisc = Producer(
    name="Jet1_puIdDisc",
    call="basefunctions::getvar<float>({df}, {output}, 0, {input})",
    input=[q.good_jet_collection, nanoAOD.Jet_puIdDisc],
    output=[q.jet1_puIdDisc],
    scopes=["global","vbfhmm"],
)
Jet2_puIdDisc = Producer(
    name="Jet2_puIdDisc",
    call="basefunctions::getvar<float>({df}, {output}, 1, {input})",
    input=[q.good_jet_collection, nanoAOD.Jet_puIdDisc],
    output=[q.jet2_puIdDisc],
    scopes=["global","vbfhmm"],
)

LVJet1 = Producer(
    name="LVJet1",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected,
    ],
    output=[q.jet_p4_1],
    scopes=["global","vbfhmm"],
)
LVJet2 = Producer(
    name="LVJet2",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected,
    ],
    output=[q.jet_p4_2],
    scopes=["global","vbfhmm"],
)
LVJet3 = Producer(
    name="LVJet3",
    call="lorentzvectors::build({df}, {input_vec}, 2, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected,
    ],
    output=[q.jet_p4_3],
    scopes=["global","vbfhmm"],
)
LVJet4 = Producer(
    name="LVJet4",
    call="lorentzvectors::build({df}, {input_vec}, 3, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected,
    ],
    output=[q.jet_p4_4],
    scopes=["global","vbfhmm"],
)
FilterNJets = Producer(
    name="FilterNJets",
    call='basefunctions::FilterThreshold({df}, {input}, {vbf_njets}, ">=", "Number of jets >= 2")',
    input=[q.njets],
    output=None,
    scopes=["global","vbfhmm"],
)
Calc_MHT_all = Producer(
    name="Calc_MHT_all",
    call="physicsobject::MHT_CalculationALL({df}, {output}, {input})",
    input=[
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
        q.good_muon_collection,
        nanoAOD.Electron_pt,
        nanoAOD.Electron_eta,
        nanoAOD.Electron_phi,
        nanoAOD.Electron_mass,
        q.base_electron_collection,
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected,
        q.good_jet_collection,
    ],
    output=[q.MHTALL_p4],
    scopes=["global","e2m","m2m"],
)

DiJetMass = Producer(
    name="DiJetMass",
    call='jet::Calculate_JetMass({df}, {output}, {input})',
    input=[q.Jet_pt_corrected,
           nanoAOD.Jet_eta, 
           nanoAOD.Jet_phi, 
           q.Jet_mass_corrected,
           q.good_jet_collection,
    ],
    output=[q.dijet_mass],
    scopes=["global","vbfhmm"],
)
DiJetEta = Producer(
    name="DiJetEta",
    call='jet::Calculate_JetDeltaEta({df}, {output}, {input})',
    input=[q.Jet_pt_corrected,
           nanoAOD.Jet_eta, 
           nanoAOD.Jet_phi, 
           q.Jet_mass_corrected,
           q.good_jet_collection,
    ],
    output=[q.dijet_eta],
    scopes=["global","vbfhmm"],
)

#nSoftJet5 = Producer(
#    name="nSoftJet5",
#    call="basefunctions::rename<Int_t>({df}, {input}, {output})",
#    input=[nanoAOD.SoftActivityJetNjets5],
#    output=[q.nSoftJet5],
#    scopes=["global","vbfhmm"],
#)
