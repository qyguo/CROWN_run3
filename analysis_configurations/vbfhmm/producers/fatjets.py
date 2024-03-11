from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

####################
# Set of producers used for selection possible good fatjets
####################

### energy corrections
# vh these pT corrections are copied from Htautau
# TODO check if L1FastJet L2L3 and residual corrections are consistent with hmm
FatJetPtCorrection = Producer(
    name="FatJetPtCorrection",
    call="physicsobject::jet::JetPtCorrection({df}, {output}, {input}, {fatjet_reapplyJES}, {fatjet_jes_sources}, {fatjet_jes_shift}, {fatjet_jer_shift}, {fatjet_jec_file}, {fatjet_jer_tag}, {fatjet_jes_tag}, {fatjet_jec_algo})",
    input=[
        nanoAOD.FatJet_pt,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        nanoAOD.FatJet_area,
        nanoAOD.FatJet_rawFactor,
        nanoAOD.FatJet_ID,
        nanoAOD.GenJetAK8_pt,
        nanoAOD.GenJetAK8_eta,
        nanoAOD.GenJetAK8_phi,
        nanoAOD.rho,
    ],
    output=[q.FatJet_pt_corrected],
    scopes=["global"],
)
FatJetMassCorrection = Producer(
    name="FatJetMassCorrection",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.FatJet_mass,
        nanoAOD.FatJet_pt,
        q.FatJet_pt_corrected,
    ],
    output=[q.FatJet_mass_corrected],
    scopes=["global"],
)
FatJetEnergyCorrection = ProducerGroup(
    name="FatJetEnergyCorrection",
    call=None,
    input=None,
    output=None,
    scopes=["global"],
    subproducers=[FatJetPtCorrection, FatJetMassCorrection],
)
# in data and embdedded sample, we simply rename the nanoAOD jets to the jet_pt_corrected column
RenameFatJetPt = Producer(
    name="RenameFatJetPt",
    call="basefunctions::rename<ROOT::RVec<float>>({df}, {input}, {output})",
    input=[nanoAOD.FatJet_pt],
    output=[q.FatJet_pt_corrected],
    scopes=["global"],
)
RenameFatJetMass = Producer(
    name="RenameFatJetMass",
    call="basefunctions::rename<ROOT::RVec<float>>({df}, {input}, {output})",
    input=[nanoAOD.FatJet_mass],
    output=[q.FatJet_mass_corrected],
    scopes=["global"],
)
RenameFatJetsData = ProducerGroup(
    name="RenameFatJetsData",
    call=None,
    input=None,
    output=None,
    scopes=["global"],
    subproducers=[RenameFatJetPt, RenameFatJetMass],
)
FatJetPtCut = Producer(
    name="FatJetPtCut",
    call="physicsobject::CutPt({df}, {input}, {output}, {min_fatjet_pt})",
    input=[q.FatJet_pt_corrected],
    output=[],
    scopes=["global"],
)
FatJetEtaCut = Producer(
    name="FatJetEtaCut",
    call="physicsobject::CutEta({df}, {input}, {output}, {max_fatjet_eta})",
    input=[nanoAOD.FatJet_eta],
    output=[],
    scopes=["global"],
)
FatJetSDMassCut = Producer(
    name="FatJetSDMassCut",
    call="physicsobject::CutVarMin({df}, {input}, {output}, {min_fatjet_MSD})",
    input=[nanoAOD.FatJet_msoftdrop],
    output=[],
    scopes=["global"],
)
FatJetIDCut = Producer(
    name="FatJetIDCut",
    call="physicsobject::jet::CutID({df}, {output}, {input}, {fatjet_id})",
    input=[nanoAOD.FatJet_ID],
    output=[q.fatjet_id_mask],
    scopes=["global"],
)
VetoOverlappingFatJetsWithMuons = Producer(
    name="VetoOverlappingFatJetsWithMuons",
    call="jet::VetoOverlappingJets({df}, {output}, {input}, {deltaR_fatjet_veto})",
    input=[nanoAOD.FatJet_eta, nanoAOD.FatJet_phi, nanoAOD.Muon_eta, nanoAOD.Muon_phi, q.base_muons_mask], # vh base or good muon?
    output=[q.fatjet_overlap_veto_mask],
    scopes=["global"],
)
GoodFatJets = ProducerGroup(
    name="GoodFatJets",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[],
    output=[q.good_fatjets_mask],
    scopes=["global"],
    subproducers=[FatJetPtCut, FatJetEtaCut, FatJetSDMassCut, FatJetIDCut, VetoOverlappingFatJetsWithMuons],
)
NumberOfGoodFatJets = Producer(
    name="NumberOfGoodFatJets",
    call="quantities::NumberOfGoodObjects({df}, {output}, {input})",
    input=[q.good_fatjets_mask],
    output=[q.nfatjets],
    scopes=["global"],
)
# fatjet collection
FatJetCollection = Producer(
    name="FatJetCollection",
    call="jet::OrderJetsByPt({df}, {output}, {input})",
    input=[q.FatJet_pt_corrected, q.good_fatjets_mask],
    output=[q.good_fatjet_collection],
    scopes=["global"],
)
LVFatJet1 = Producer(
    name="LVFatJet1",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_fatjet_collection,
        q.FatJet_pt_corrected,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        q.FatJet_mass_corrected,
    ],
    output=[q.fatjet_p4_1],
    scopes=["global"],
)