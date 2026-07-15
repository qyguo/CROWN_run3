from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup
# write by jiahua

####################
# Set of producers used for syst uncertainties    
####################

CalPDFUncertainty_up = Producer(
    name="CalPDFUncertainty",
    call="reweighting::LHEpdf({df}, {output}, {input}, \"up\")",
    input=[
        nanoAOD.LHEPdfWeight,
    ],
    output=[q.PDF_uncertainty_up],
    scopes=["global", "vbfhmm"],
)

CalPDFUncertainty_down = Producer(
    name="CalPDFUncertainty",
    call="reweighting::LHEpdf({df}, {output}, {input}, \"down\")",
    input=[
        nanoAOD.LHEPdfWeight,
    ],
    output=[q.PDF_uncertainty_down],
    scopes=["global", "vbfhmm"],
)

CalQCDScaleUncertainty_up = Producer(
    name="CalQCDScaleUncertainty_up",
    call="reweighting::LHEscale({df}, {output}, {input}, \"up\")",
    input=[
        nanoAOD.LHEScaleWeight,
    ],
    output=[q.qcd_unc_up],
    scopes=["global", "vbfhmm"],
)

CalQCDScaleUncertainty_down = Producer(
    name="CalQCDScaleUncertainty_down",
    call="reweighting::LHEscale({df}, {output}, {input}, \"down\")",
    input=[
        nanoAOD.LHEScaleWeight,
    ],
    output=[q.qcd_unc_down],
    scopes=["global", "vbfhmm"],
)

CalPDFUncertainty = Producer(
    name="CalPDFUncertainty",
    call="reweighting::LHEpdfUncertainty({df}, {output}, {input})",
    input=[nanoAOD.LHEPdfWeight],
    output=[q.PDF_uncertainty],
    scopes=["global"],
)

CalAlphaSUncertainty = Producer(
    name="CalAlphaSUncertainty",
    call="reweighting::LHEalphaSUncertainty({df}, {output}, {input})",
    input=[nanoAOD.LHEPdfWeight],
    output=[q.alphaS_uncertainty],
    scopes=["global"],
)

StoreLHEScaleWeights = Producer(
    name="StoreLHEScaleWeights",
    call="reweighting::LHEscaleWeights({df}, {output_vec}, {input})",
    input=[nanoAOD.LHEScaleWeight],
    output=[
        q.LHEScaleWeight_0,
        q.LHEScaleWeight_1,
        q.LHEScaleWeight_2,
        q.LHEScaleWeight_3,
        q.LHEScaleWeight_4,
        q.LHEScaleWeight_5,
    ],
    scopes=["global"],
)
