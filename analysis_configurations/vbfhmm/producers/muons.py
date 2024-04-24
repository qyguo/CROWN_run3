from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

####################
# Set of producers used for loosest selection of muons
####################

Muon_pTErr_1 = Producer(
    name="Muon_pTErr_1",
    call="quantities::ptErr({df}, {output}, 0, {input})",
    input=[q.dimuon_HiggsCand_collection, nanoAOD.Muon_ptErr],
    output=[q.mu1_fromH_ptErr],
    scopes=["vbfhmm"],
)

Muon_pTErr_2 = Producer(
    name="Muon_pTErr_2",
    call="quantities::ptErr({df}, {output}, 1, {input})",
    input=[q.dimuon_HiggsCand_collection, nanoAOD.Muon_ptErr],
    output=[q.mu2_fromH_ptErr],
    scopes=["vbfhmm"],
)

MuonPtCut = Producer(
    name="MuonPtCut",
    call="physicsobject::CutPt({df}, {input}, {output}, {min_muon_pt})",
    input=[nanoAOD.Muon_pt],
    output=[],
    scopes=["global","gghmm","vbfhmm"],
)
MuonEtaCut = Producer(
    name="MuonEtaCut",
    call="physicsobject::CutEta({df}, {input}, {output}, {max_muon_eta})",
    input=[nanoAOD.Muon_eta],
    output=[],
    scopes=["global","gghmm","vbfhmm"],
)
MuonDxyCut = Producer(
    name="MuonDxyCut",
    call="physicsobject::CutDxy({df}, {input}, {output}, {max_muon_dxy})",
    input=[nanoAOD.Muon_dxy],
    output=[],
    scopes=["global"],
)
MuonDzCut = Producer(
    name="MuonDzCut",
    call="physicsobject::CutDz({df}, {input}, {output}, {max_muon_dz})",
    input=[nanoAOD.Muon_dz],
    output=[],
    scopes=["global"],
)
MuonSIP3DCut = Producer(
    name="MuonSIP3DCut",
    call="physicsobject::CutVarMax({df}, {input}, {output}, {max_sip3d})", # vh developed CutVarMax/Min, TODO apply to others
    input=[nanoAOD.Muon_sip3d],
    output=[],
    scopes=["global"],
)
# TODO vh LepMVA
Muon_mvaTTH_Cut = Producer(
    name="Muon_mvaTTH_Cut",
    call="physicsobject::CutVarMin({df}, {input}, {output}, {min_muon_mvaTTH})",
    input=[nanoAOD.Muon_mvaTTH],
    output=[],
    scopes=["global"],
)
MuonIDCut = Producer(
    name="MuonIDCut",
    call='physicsobject::muon::CutID({df}, {output}, "{muon_id}")',
    #input=[nanoAOD.Muon_mediumId],
    input=[],
    output=[],
    scopes=["global","gghmm","vbfhmm"],
)
MuonIsoCut = Producer(
    name="MuonIsoCut",
    call="physicsobject::muon::CutIsolation({df}, {output}, {input}, {muon_iso_cut})",
    input=[nanoAOD.Muon_pfRelIso04_all], # vh
    #input=[nanoAOD.Muon_miniPFRelIso_all],
    output=[],
    scopes=["global","gghmm","vbfhmm"],
)
BaseMuons = ProducerGroup(
    name="BaseMuons",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[],
    output=[q.base_muons_mask],
    scopes=["global","vbfhmm","gghmm"],
    subproducers=[
        MuonPtCut,
        MuonEtaCut,
        #MuonDxyCut,
        #MuonDzCut,
        #MuonSIP3DCut,
        # TODO vh add LepMVA
        #Muon_mvaTTH_Cut,
        MuonIDCut,
        MuonIsoCut,
    ],
)

####################
# Set of producers used for more specific selection of muons in channels
####################

# vh just in case different muon selections are needed (e.g. loose vs tight id for fakes)
# do cuts again for ALL the channels

GoodMuonPtCut = Producer(
    name="GoodMuonPtCut",
    call="physicsobject::CutPt({df}, {input}, {output}, {min_muon_pt})",
    input=[nanoAOD.Muon_pt],
    output=[],
    scopes=["gghmm","vbfhmm","e2m","m2m", "eemm","mmmm","nnmm","fjmm","nnmm_dycontrol","nnmm_topcontrol"],
)
GoodMuonEtaCut = Producer(
    name="GoodMuonEtaCut",
    call="physicsobject::CutEta({df}, {input}, {output}, {max_muon_eta})",
    input=[nanoAOD.Muon_eta],
    output=[],
    scopes=["gghmm","vbfhmm","e2m","m2m", "eemm","mmmm","nnmm","fjmm","nnmm_dycontrol","nnmm_topcontrol"],
)
GoodMuonIDCut = Producer(
    name="GoodMuonIDCut",
    call='physicsobject::muon::CutID({df}, {output}, "{muon_id}")',
    #input=[nanoAOD.Muon_mediumId],
    input=[],
    output=[],
    scopes=["global","gghmm","vbfhmm"],
)
###
GoodMuonIsoCut = Producer(
    name="GoodMuonIsoCut",
    #call="physicsobject::electron::CutIsolation({df}, {output}, {input}, {muon_iso_cut})",
    call="physicsobject::muon::CutIsolation({df}, {output}, {input}, {muon_iso_cut})",
    input=[nanoAOD.Muon_pfRelIso04_all],
    #input=[nanoAOD.Muon_miniPFRelIso_all],
    output=[],
    scopes=["gghmm","vbfhmm","e2m","m2m", "eemm","mmmm","nnmm","fjmm","nnmm_dycontrol","nnmm_topcontrol"],
)
GoodMuons = ProducerGroup(
    name="GoodMuons",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[q.base_muons_mask],
    output=[q.good_muons_mask], # vh these are the final selection muons' mask
    scopes=["gghmm","vbfhmm","e2m","m2m", "eemm","mmmm","nnmm","fjmm","nnmm_dycontrol","nnmm_topcontrol"],
    subproducers=[
        GoodMuonPtCut,
        GoodMuonEtaCut,
        GoodMuonIDCut,
        GoodMuonIsoCut,
    ],
)
#
NumberOfGoodMuons = Producer(
    name="NumberOfGoodMuons",
    call="quantities::NumberOfGoodObjects({df}, {output}, {input})",
    input=[q.good_muons_mask],
    output=[q.nmuons],
    scopes=["gghmm","vbfhmm","e2m","m2m", "eemm","mmmm","nnmm","fjmm","nnmm_dycontrol","nnmm_topcontrol"],
)
VetoMuons = Producer(
    name="VetoMuons",
    call="physicsobject::VetoCandInMask({df}, {output}, {input}, {muon_index_in_pair})",
    input=[q.base_muons_mask, q.dileptonpair],
    output=[q.veto_muons_mask],
    scopes=["mm"],
)
VetoSecondMuon = Producer(
    name="VetoSecondMuon",
    call="physicsobject::VetoCandInMask({df}, {output}, {input}, {second_muon_index_in_pair})",
    input=[q.veto_muons_mask, q.dileptonpair],
    output=[q.veto_muons_mask_2],
    scopes=["mm"],
)

ExtraMuonsVeto = Producer(
    name="ExtraMuonsVeto",
    call="physicsobject::LeptonVetoFlag({df}, {output}, {input})",
    input={
        "mm": [q.veto_muons_mask_2],
    },
    output=[q.muon_veto_flag],
    scopes=["mm"],
)

####################
# Set of producers used for di-muon veto
####################

DiMuonVetoPtCut = Producer(
    name="DiMuonVetoPtCut",
    call="physicsobject::CutPt({df}, {input}, {output}, {min_dimuonveto_pt})",
    input=[nanoAOD.Muon_pt],
    output=[],
    scopes=["global"],
)
DiMuonVetoIDCut = Producer(
    name="DiMuonVetoIDCut",
    call='physicsobject::muon::CutID({df}, {output}, "{dimuonveto_id}")',
    input=[],
    output=[],
    scopes=["global"],
)
DiMuonVetoMuons = ProducerGroup(
    name="DiMuonVetoMuons",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=MuonEtaCut.output + MuonDxyCut.output + MuonDzCut.output + MuonIsoCut.output,
    output=[],
    scopes=["global"],
    subproducers=[
        DiMuonVetoPtCut,
        DiMuonVetoIDCut,
    ],
)
DiMuonVeto = ProducerGroup(
    name="DiMuonVeto",
    call="physicsobject::CheckForDiLeptonPairs({df}, {output}, {input}, {dileptonveto_dR})",
    input=[
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
        nanoAOD.Muon_charge,
    ],
    output=[q.dimuon_veto],
    scopes=["global"],
    subproducers=[DiMuonVetoMuons],
)


### Muon collection and their properties
MuonCollection = Producer(
    name="MuonCollection",
    call="jet::OrderJetsByPt({df}, {output}, {input})",
    input=[nanoAOD.Muon_pt, q.good_muons_mask],
    output=[q.good_muon_collection],
    scopes=["gghmm","vbfhmm","e2m","m2m", "eemm","mmmm","nnmm","fjmm","nnmm_dycontrol","nnmm_topcontrol"],
)
LVMu1 = Producer(
    name="LVMu1",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_muon_collection,
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
    ],
    output=[q.muon_p4_1],
    scopes=["gghmm","vbfhmm","e2m","m2m", "eemm","mmmm","nnmm","fjmm"],
)
LVMu2 = Producer(
    name="LVMu2",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_muon_collection,
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
    ],
    output=[q.muon_p4_2],
    scopes=["gghmm","vbfhmm","e2m","m2m", "eemm","mmmm","nnmm","fjmm"],
)
LVMu3 = Producer(
    name="LVMu3",
    call="lorentzvectors::build({df}, {input_vec}, 2, {output})",
    input=[
        q.good_muon_collection,
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
    ],
    output=[q.muon_p4_3],
    scopes=["m2m", "mmmm"],
)
LVMu4 = Producer(
    name="LVMu4",
    call="lorentzvectors::build({df}, {input_vec}, 3, {output})",
    input=[
        q.good_muon_collection,
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
    ],
    output=[q.muon_p4_4],
    scopes=["mmmm"],
)
##### 
##### The leading muon from Higgs
Mu1_H = Producer(
    name="Mu1_H",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.dimuon_HiggsCand_collection,
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
    ],
    output=[q.muon_leadingp4_H],
    scopes=["gghmm","vbfhmm","e2m","m2m", "eemm","nnmm","fjmm"],
)
##### The sub leading muon form Higgs
Mu2_H = Producer(
    name="Mu2_H",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.dimuon_HiggsCand_collection,
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
    ],
    output=[q.muon_subleadingp4_H],
    scopes=["gghmm","vbfhmm","e2m","m2m", "eemm","nnmm","fjmm"],
)
##### The leading muon from Higgs in 4m channel
Mu1_H_4m = Producer(
    name="Mu1_H_4m",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.quadmuon_HiggsZCand_collection,
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
    ],
    output=[q.muon_leadingp4_H],
    scopes=["mmmm"],
)
##### The sub leading muon from Higgs in 4m channel
Mu2_H_4m = Producer(
    name="Mu2_H_4m",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.quadmuon_HiggsZCand_collection,
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
    ],
    output=[q.muon_subleadingp4_H],
    scopes=["mmmm"],
)
##### The leading muon from Z Cand in 4m channel
Mu1_Z_4m = Producer(
    name="Mu1_Z_4m",
    call="lorentzvectors::build({df}, {input_vec}, 2, {output})",
    input=[
        q.quadmuon_HiggsZCand_collection,
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
    ],
    output=[q.lepton_leadingp4_Z],
    scopes=["mmmm"],
)
Mu2_Z_4m = Producer(
    name="Mu2_Z_4m",
    call="lorentzvectors::build({df}, {input_vec}, 3, {output})",
    input=[
        q.quadmuon_HiggsZCand_collection,
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
    ],
    output=[q.lepton_subleadingp4_Z],
    scopes=["mmmm"],
)
