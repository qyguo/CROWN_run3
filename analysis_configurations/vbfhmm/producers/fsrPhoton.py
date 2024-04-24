from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

####################
# Set of producers used for selection fsr associated with muons
####################

#Muon_pTErr_1 = Producer(
#    name="Muon_pTErr_1",
#    call="quantities::ptErr({df}, {output}, 0, {input})",
#    input=[q.dimuon_HiggsCand_collection, nanoAOD.Muon_ptErr],
#    output=[q.mu1_fromH_ptErr],
#    scopes=["vbfhmm"],
#)

muon_fsrPhotonIdx_1 = Producer(
    name="muon_fsrPhotonIdx_1",
    call="quantities::fsrIdx({df}, {output}, 0, {input})",
    #input=[q.selectedLepton, nanoAOD.Muon_fsrPhotonIdx],
    input=[q.dimuon_HiggsCand_collection, nanoAOD.Muon_fsrPhotonIdx],
    output=[q.fsrPhotonIdx_1],
    scopes=["vbfhmm"],
)
muon_fsrPhotonIdx_2 = Producer(
    name="muon_fsrPhotonIdx_2",
    call="quantities::fsrIdx({df}, {output}, 1, {input})",
    input=[q.dimuon_HiggsCand_collection, nanoAOD.Muon_fsrPhotonIdx],
    output=[q.fsrPhotonIdx_2],
    scopes=["vbfhmm"],
)

muon_fsrPhoton_pt_1 = Producer(
    name="muon_fsrPhoton_pt_1",
    #call="basefunctions::getvar<float>({df}, {output}, 0, {input})",
    call="basefunctions::getvar<float>({df}, {output}, {input})",
    input=[q.fsrPhotonIdx_1, nanoAOD.FsrPhoton_pt],
    output=[q.fsrPhoton_pt_1],
    scopes=["vbfhmm"],
)
muon_fsrPhoton_eta_1 = Producer(
    name="muon_fsrPhoton_eta_1",
    #call="basefunctions::getvar<float>({df}, {output}, 0, {input})",
    call="basefunctions::getvar<float>({df}, {output}, {input})",
    input=[q.fsrPhotonIdx_1, nanoAOD.FsrPhoton_eta],
    output=[q.fsrPhoton_eta_1],
    scopes=["vbfhmm"],
)
muon_fsrPhoton_phi_1 = Producer(
    name="muon_fsrPhoton_phi_1",
    #call="basefunctions::getvar<float>({df}, {output}, 0, {input})",
    call="basefunctions::getvar<float>({df}, {output}, {input})",
    input=[q.fsrPhotonIdx_1, nanoAOD.FsrPhoton_phi],
    output=[q.fsrPhoton_phi_1],
    scopes=["vbfhmm"],
)
muon_fsrPhoton_dROverEt2_1 = Producer(
    name="muon_fsrPhoton_dROverEt2_1",
    #call="basefunctions::getvar<float>({df}, {output}, 0, {input})",
    call="basefunctions::getvar<float>({df}, {output}, {input})",
    input=[q.fsrPhotonIdx_1, nanoAOD.FsrPhoton_dROverEt2],
    output=[q.fsrPhoton_dROverEt2_1],
    scopes=["vbfhmm"],
)
muon_fsrPhoton_relIso03_1 = Producer(
    name="muon_fsrPhoton_relIso03_1",
    #call="basefunctions::getvar<float>({df}, {output}, 0, {input})",
    call="basefunctions::getvar<float>({df}, {output}, {input})",
    input=[q.fsrPhotonIdx_1, nanoAOD.FsrPhoton_relIso03],
    output=[q.fsrPhoton_relIso03_1],
    scopes=["vbfhmm"],
)
muon_fsrPhoton_pt_2 = Producer(
    name="muon_fsrPhoton_pt_2",
    #call="basefunctions::getvar<float>({df}, {output}, 0, {input})",
    call="basefunctions::getvar<float>({df}, {output}, {input})",
    input=[q.fsrPhotonIdx_2, nanoAOD.FsrPhoton_pt],
    output=[q.fsrPhoton_pt_2],
    scopes=["vbfhmm"],
)
muon_fsrPhoton_eta_2 = Producer(
    name="muon_fsrPhoton_eta_2",
    #call="basefunctions::getvar<float>({df}, {output}, 0, {input})",
    call="basefunctions::getvar<float>({df}, {output}, {input})",
    input=[q.fsrPhotonIdx_2, nanoAOD.FsrPhoton_eta],
    output=[q.fsrPhoton_eta_2],
    scopes=["vbfhmm"],
)
muon_fsrPhoton_phi_2 = Producer(
    name="muon_fsrPhoton_phi_2",
    #call="basefunctions::getvar<float>({df}, {output}, 0, {input})",
    call="basefunctions::getvar<float>({df}, {output}, {input})",
    input=[q.fsrPhotonIdx_2, nanoAOD.FsrPhoton_phi],
    output=[q.fsrPhoton_phi_2],
    scopes=["vbfhmm"],
)
muon_fsrPhoton_dROverEt2_2 = Producer(
    name="muon_fsrPhoton_dROverEt2_2",
    #call="basefunctions::getvar<float>({df}, {output}, 0, {input})",
    call="basefunctions::getvar<float>({df}, {output}, {input})",
    input=[q.fsrPhotonIdx_2, nanoAOD.FsrPhoton_dROverEt2],
    output=[q.fsrPhoton_dROverEt2_2],
    scopes=["vbfhmm"],
)
muon_fsrPhoton_relIso03_2 = Producer(
    name="muon_fsrPhoton_relIso03_2",
    #call="basefunctions::getvar<float>({df}, {output}, 0, {input})",
    call="basefunctions::getvar<float>({df}, {output}, {input})",
    input=[q.fsrPhotonIdx_2, nanoAOD.FsrPhoton_relIso03],
    output=[q.fsrPhoton_relIso03_2],
    scopes=["vbfhmm"],
)
##
