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
# jet collection
JetCollection = Producer(
    name="JetCollection",
    call="jet::OrderJetsByPt({df}, {output}, {input})",
    input=[q.Jet_pt_corrected, q.good_jets_mask],
    output=[q.good_jet_collection],
    scopes=["global"],
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
