from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import ExtendedVectorProducer

####################
# Set of producers used for trigger flags
####################

GenerateSingleMuonTriggerFlags = ExtendedVectorProducer(
    name="GenerateSingleMuonTriggerFlags",
    call='trigger::GenerateTripleTriggerORFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {ptcut}, {ptcut}, {etacut}, {etacut}, {etacut}, {trigger_particle_id}, {trigger_particle_id}, {trigger_particle_id}, {filterbit}, {filterbit}, {filterbit}, {max_deltaR_triggermatch} )',
    input=[
        q.muon_p4_1,
        q.muon_p4_2,
        q.muon_p4_3,
        nanoAOD.TriggerObject_bit,
        nanoAOD.TriggerObject_id,
        nanoAOD.TriggerObject_pt,
        nanoAOD.TriggerObject_eta,
        nanoAOD.TriggerObject_phi,
    ],
    output="flagname",
    scope=["m2m"],
    vec_config="singlemuon_trigger",
)
GenerateSingleMuonTriggerFlagsForDiMuChannel = ExtendedVectorProducer(
    name="GenerateSingleMuonTriggerFlagsForDiMuChannel",
    call='trigger::GenerateDoubleTriggerORFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {ptcut}, {etacut}, {etacut}, {trigger_particle_id}, {trigger_particle_id}, {filterbit}, {filterbit}, {max_deltaR_triggermatch} )',
    input=[
        q.muon_p4_1,
        q.muon_p4_2,
        nanoAOD.TriggerObject_bit,
        nanoAOD.TriggerObject_id,
        nanoAOD.TriggerObject_pt,
        nanoAOD.TriggerObject_eta,
        nanoAOD.TriggerObject_phi,
    ],
    output="flagname",
    scope=["gghmm","vbfhmm","e2m","eemm","nnmm","fjmm"],
    vec_config="singlemuon_trigger",
)
###
GenerateSingleMuonTriggerFlagsForDiMuChannel_2022 = ExtendedVectorProducer(
    name="GenerateSingleMuonTriggerFlagsForDiMuChannel_2022",
    call='trigger::GenerateDoubleTriggerORFlag_2022({df}, {output}, {input}, "{hlt_path}", {ptcut}, {ptcut}, {etacut}, {etacut}, {trigger_particle_id}, {trigger_particle_id}, {filterbit}, {filterbit}, {max_deltaR_triggermatch} )',
    input=[
        q.muon_p4_1,
        q.muon_p4_2,
        nanoAOD.TriggerObject_bit,
        nanoAOD.TriggerObject_id,
        nanoAOD.TriggerObject_pt,
        nanoAOD.TriggerObject_eta,
        nanoAOD.TriggerObject_phi,
    ],
    output="flagname",
    scope=["gghmm","vbfhmm","e2m","eemm","nnmm","fjmm"],
    vec_config="singlemuon_trigger",
)
 
GenerateSingleMuonTriggerFlagsForDiMuChannelFSIM = ExtendedVectorProducer(
    name="GenerateSingleMuonTriggerFlagsForDiMuChannelFSIM",
    call='trigger::GenerateDoubleTriggerFlagFromEfficiency({df}, {output}, {input}, "{eff_json}", "{eff_name}", {ptcut}, {ptcut}, {etacut}, {etacut})',
    input=[
        nanoAOD.run,
        nanoAOD.luminosityBlock,
        nanoAOD.event,
        q.muon_p4_1,
        q.muon_p4_2,
    ],
    output="flagname",
    scope=["fsim"],
    vec_config="singlemuon_trigger_eff",
)

GenerateSingleMuonTriggerFlagsForQuadMuChannel = ExtendedVectorProducer(
    name="GenerateSingleMuonTriggerFlagsForQuadMuChannel",
    call='trigger::GenerateQuadTriggerORFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {ptcut}, {ptcut}, {ptcut}, {etacut}, {etacut}, {etacut}, {etacut}, {trigger_particle_id}, {trigger_particle_id}, {trigger_particle_id}, {trigger_particle_id}, {filterbit}, {filterbit}, {filterbit}, {filterbit}, {max_deltaR_triggermatch} )',
    input=[
        q.muon_p4_1,
        q.muon_p4_2,
        q.muon_p4_3,
        q.muon_p4_4,
        nanoAOD.TriggerObject_bit,
        nanoAOD.TriggerObject_id,
        nanoAOD.TriggerObject_pt,
        nanoAOD.TriggerObject_eta,
        nanoAOD.TriggerObject_phi,
    ],
    output="flagname",
    scope=["mmmm"],
    vec_config="singlemuon_trigger",
)
