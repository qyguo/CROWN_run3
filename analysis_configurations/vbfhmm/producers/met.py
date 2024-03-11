from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup
# write by botao

BuildMetVector = Producer(
    name="BuildMetVector",
    call="lorentzvectors::buildMet({df}, {input}, {output})",
    input=[
        nanoAOD.MET_pt,
        nanoAOD.MET_phi,
    ],
    output=[q.met_p4],
    scopes=["global"],
)
BuildPFMetVector = Producer(
    name="BuildPFMetVector",
    call="lorentzvectors::buildMet({df}, {input}, {output})",
    input=[
        nanoAOD.PFMET_pt,
        nanoAOD.PFMET_phi,
    ],
    output=[q.pfmet_p4],
    scopes=["global"],
)
BuildGenMetVector = Producer(
    name="BuildGenMetVector",
    call="lorentzvectors::buildMet({df}, {input}, {output})",
    input=[
        nanoAOD.GenMET_pt,
        nanoAOD.GenMET_phi,
    ],
    output=[q.genmet_p4],
    scopes=["global"],
)
MetBasics = ProducerGroup(
    name="MetBasics",
    call=None,
    input=None,
    output=None,
    scopes=["global"],
    subproducers=[
        BuildPFMetVector,
        BuildMetVector,
        # BuildGenMetVector,
    ],
)