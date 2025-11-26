from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup
# write by botao

####################
# Set of producers used for select the smallest mass of di-lepton
####################

# dilepton mass > 12 GeV need SFOS
CalcSmallestDiMuonMass = Producer(
    name="CalcSmallestDiMuonMass",
    call='physicsobject::M_dileptonMass({df}, {output}, {input})',
    input=[nanoAOD.Muon_pt,
           nanoAOD.Muon_eta, 
           nanoAOD.Muon_phi, 
           nanoAOD.Muon_mass,
           nanoAOD.Muon_charge,
           q.good_muon_collection],
    output=[q.smallest_dimuon_mass],
    scopes=["global","m2m","e2m","eemm","mmmm","nnmm","fjmm","nnmm_dycontrol"],
)
CalcSmallestDiElectronMass = Producer(
    name="CalcSmallestDiElectronMass",
    call='physicsobject::M_dileptonMass({df}, {output}, {input})',
    input=[nanoAOD.Electron_pt,
           nanoAOD.Electron_eta, 
           nanoAOD.Electron_phi, 
           nanoAOD.Electron_mass,
           nanoAOD.Electron_charge,
           q.base_electron_collection],
    output=[q.smallest_dielectron_mass],
    scopes=["global","eemm"],
)
LeptonChargeSumVeto = Producer(
    name="LeptonChargeSumVeto",
    call='physicsobject::LeptonChargeSum({df}, {output}, {input})',
    input=[nanoAOD.Muon_charge,  # only in m2m and 4m can input only muon charge
           q.good_muon_collection],
    output=[q.Flag_LeptonChargeSumVeto],   # 1 stands pm1, 2 stands 0, 0 stands others
    scopes=["global","gghmm","vbfhmm","m2m","mmmm","nnmm","fjmm","nnmm_dycontrol"],
)
LeptonChargeSumVeto_elemu = Producer(
    name="LeptonChargeSumVeto_elemu",
    call='physicsobject::LeptonChargeSumEleMu({df}, {output}, {input})',
    input=[nanoAOD.Muon_charge,  # only in e2m and 2e2m can input only muon charge
           nanoAOD.Electron_charge,
           q.good_muon_collection,
           q.base_electron_collection],
    output=[q.Flag_LeptonChargeSumVeto],   # 1 stands pm1, 2 stands 0, 0 stands others
    scopes=["global","e2m","eemm","nnmm_topcontrol"],
)
### extra lepton (muon) in m2m channel
Mu1_W_m2m_index = Producer(
    name="Mu1_W_m2m_index",
    call="physicsobject::ExtraMuonIndexFromW({df}, {output}, {input})",
    input=[
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
        q.good_muon_collection,
        q.dimuon_HiggsCand_collection,
    ],
    output=[q.extra_muon_index],
    scopes=["m2m"],
)
Mu1_W_m2m = Producer(
    name="Mu1_W_m2m",
    call="physicsobject::ExtraMuonFromW({df}, {output}, {input})",
    input=[
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
        q.extra_muon_index,
    ],
    output=[q.extra_lep_p4],
    scopes=["m2m"],
)
### extra lepton (electron) in e2m channel
Ele1_W_e2m = Producer(
    name="Ele1_W_e2m",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.base_electron_collection,
        nanoAOD.Electron_pt,
        nanoAOD.Electron_eta,
        nanoAOD.Electron_phi,
        nanoAOD.Electron_mass,
    ],
    output=[q.extra_lep_p4],
    scopes=["e2m"],
)
### calc MT_W using lepton_p4 and met
Calc_MT_W = Producer(
    name="Calc_MT_W",
    call="quantities::mT_MHT({df}, {output}, {input})",
    input=[
        q.extra_lep_p4,
        q.met_p4,
    ],
    output=[q.mt_W],
    scopes=["e2m","m2m"],
)
### Z lep ID
RenameZlepID_eemm = Producer(
    name="RenameZlepID_eemm",
    call="physicsobject::RedirectZlepID({df}, 0, {output})", # ifMu == 0, return 11
    input=[],
    output=[q.Zlep_ID],
    scopes=["eemm"],
)
RenameZlepID_mmmm = Producer(
    name="RenameZlepID_mmmm",
    call="physicsobject::RedirectZlepID({df}, 1, {output})", # ifMu == 1, return 13
    input=[],
    output=[q.Zlep_ID],
    scopes=["mmmm"],
)