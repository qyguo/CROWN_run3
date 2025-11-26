from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

####################
# Set of producers used for jec uncertainty
####################

### energy corrections
# vh these pT corrections are copied from Htautau
# TODO check if L1FastJet L2L3 and residual corrections are consistent with hmm
JetPtCorrection_2022_jerUp = Producer(
    name="JetPtCorrection_2022_jerUp",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jerUp],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jerUp_GenMatch = Producer(
    name="JetPtCorrection_2022_jerUp_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jerUp],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jerUp = Producer(
    name="JetMassCorrection_jerUp",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jerUp,
    ],
    output=[q.Jet_mass_corrected_jerUp],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jerUp = ProducerGroup(
    name="JetEnergyCorrection_2022_jerUp",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jerUp, JetMassCorrection_jerUp],
)
JetEnergyCorrection_2022_jerUp_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jerUp_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jerUp_GenMatch, JetMassCorrection_jerUp],
)
### selecting jets
LVJet1_jerUp = Producer(
    name="LVJet1_jerUp",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jerUp,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jerUp,
    ],
    output=[q.jet_p4_1_jerUp],
    scopes=["global","vbfhmm"],
)
LVJet2_jerUp = Producer(
    name="LVJet2_jerUp",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jerUp,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jerUp,
    ],
    output=[q.jet_p4_2_jerUp],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jerUp = Producer(
    name="jet1_pt_jerUp",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jerUp,
    ],
    output=[q.jet1_pt_jerUp],
    scopes=["vbfhmm"],
)
jet1_eta_jerUp = Producer(
    name="jet1_eta_jerUp",
    call='quantities::eta({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jerUp,
    ],
    output=[q.jet1_eta_jerUp],
    scopes=["vbfhmm"],
)
jet1_phi_jerUp = Producer(
    name="jet1_phi_jerUp",
    call='quantities::phi({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jerUp,
    ],
    output=[q.jet1_phi_jerUp],
    scopes=["vbfhmm"],
)
jet1_mass_jerUp = Producer(
    name="jet1_mass_jerUp",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jerUp,
    ],
    output=[q.jet1_mass_jerUp],
    scopes=["vbfhmm"],
)

jet2_pt_jerUp = Producer(
    name="jet2_pt_jerUp",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jerUp,
    ],
    output=[q.jet2_pt_jerUp],
    scopes=["vbfhmm"],
)
jet2_eta_jerUp = Producer(
    name="jet2_eta_jerUp",
    call='quantities::eta({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jerUp,
    ],
    output=[q.jet2_eta_jerUp],
    scopes=["vbfhmm"],
)
jet2_phi_jerUp = Producer(
    name="jet2_phi_jerUp",
    call='quantities::phi({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jerUp,
    ],
    output=[q.jet2_phi_jerUp],
    scopes=["vbfhmm"],
)
jet2_mass_jerUp = Producer(
    name="jet2_mass_jerUp",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jerUp,
    ],
    output=[q.jet2_mass_jerUp],
    scopes=["vbfhmm"],
)
#####end of jerUp#####
#####begin of jerDown#####
JetPtCorrection_2022_jerDown = Producer(
    name="JetPtCorrection_2022_jerDown",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"down\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jerDown],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jerDown_GenMatch = Producer(
    name="JetPtCorrection_2022_jerDown_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"down\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jerDown],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jerDown = Producer(
    name="JetMassCorrection_jerDown",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jerDown,
    ],
    output=[q.Jet_mass_corrected_jerDown],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jerDown = ProducerGroup(
    name="JetEnergyCorrection_2022_jerDown",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jerDown, JetMassCorrection_jerDown],
)
JetEnergyCorrection_2022_jerDown_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jerDown_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jerDown_GenMatch, JetMassCorrection_jerDown],
)
### selecting jets
LVJet1_jerDown = Producer(
    name="LVJet1_jerDown",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jerDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jerDown,
    ],
    output=[q.jet_p4_1_jerDown],
    scopes=["global","vbfhmm"],
)
LVJet2_jerDown = Producer(
    name="LVJet2_jerDown",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jerDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jerDown,
    ],
    output=[q.jet_p4_2_jerDown],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jerDown = Producer(
    name="jet1_pt_jerDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jerDown,
    ],
    output=[q.jet1_pt_jerDown],
    scopes=["vbfhmm"],
)
jet1_eta_jerDown = Producer(
    name="jet1_eta_jerDown",
    call='quantities::eta({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jerDown,
    ],
    output=[q.jet1_eta_jerDown],
    scopes=["vbfhmm"],
)
jet1_phi_jerDown = Producer(
    name="jet1_phi_jerDown",
    call='quantities::phi({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jerDown,
    ],
    output=[q.jet1_phi_jerDown],
    scopes=["vbfhmm"],
)
jet1_mass_jerDown = Producer(
    name="jet1_mass_jerDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jerDown,
    ],
    output=[q.jet1_mass_jerDown],
    scopes=["vbfhmm"],
)

jet2_pt_jerDown = Producer(
    name="jet2_pt_jerDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jerDown,
    ],
    output=[q.jet2_pt_jerDown],
    scopes=["vbfhmm"],
)
jet2_eta_jerDown = Producer(
    name="jet2_eta_jerDown",
    call='quantities::eta({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jerDown,
    ],
    output=[q.jet2_eta_jerDown],
    scopes=["vbfhmm"],
)
jet2_phi_jerDown = Producer(
    name="jet2_phi_jerDown",
    call='quantities::phi({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jerDown,
    ],
    output=[q.jet2_phi_jerDown],
    scopes=["vbfhmm"],
)
jet2_mass_jerDown = Producer(
    name="jet2_mass_jerDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jerDown,
    ],
    output=[q.jet2_mass_jerDown],
    scopes=["vbfhmm"],
)
#####end of jerDown#####

####begin of jes FlavorQCD up#####
JetPtCorrection_2022_jesFlavorQCDUp = Producer(
    name="JetPtCorrection_2022_jesFlavorQCDUp",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_FlavorQCD\"}}, 1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesFlavorQCDUp],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesFlavorQCDUp_GenMatch = Producer(
    name="JetPtCorrection_2022_jesFlavorQCDUp_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_FlavorQCD\"}}, 1,  {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesFlavorQCDUp],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesFlavorQCDUp = Producer(
    name="JetMassCorrection_jesFlavorQCDUp",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesFlavorQCDUp,
    ],
    output=[q.Jet_mass_corrected_jesFlavorQCDUp],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesFlavorQCDUp = ProducerGroup(
    name="JetEnergyCorrection_2022_jesFlavorQCDUp",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesFlavorQCDUp, JetMassCorrection_jesFlavorQCDUp],
)
JetEnergyCorrection_2022_jesFlavorQCDUp_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesFlavorQCDUp_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesFlavorQCDUp_GenMatch, JetMassCorrection_jesFlavorQCDUp],
)
### selecting jets
LVJet1_jesFlavorQCDUp = Producer(
    name="LVJet1_jesFlavorQCDUp",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesFlavorQCDUp,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesFlavorQCDUp,
    ],
    output=[q.jet_p4_1_jesFlavorQCDUp],
    scopes=["global","vbfhmm"],
)
LVJet2_jesFlavorQCDUp = Producer(
    name="LVJet2_jesFlavorQCDUp",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesFlavorQCDUp,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesFlavorQCDUp,
    ],
    output=[q.jet_p4_2_jesFlavorQCDUp],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesFlavorQCDUp = Producer(
    name="jet1_pt_jesFlavorQCDUp",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesFlavorQCDUp,
    ],
    output=[q.jet1_pt_jesFlavorQCDUp],
    scopes=["vbfhmm"],
)
jet1_mass_jesFlavorQCDUp = Producer(
    name="jet1_mass_jesFlavorQCDUp",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesFlavorQCDUp,
    ],
    output=[q.jet1_mass_jesFlavorQCDUp],
    scopes=["vbfhmm"],
)

jet2_pt_jesFlavorQCDUp = Producer(
    name="jet2_pt_jesFlavorQCDUp",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesFlavorQCDUp,
    ],
    output=[q.jet2_pt_jesFlavorQCDUp],
    scopes=["vbfhmm"],
)
jet2_mass_jesFlavorQCDUp = Producer(
    name="jet2_mass_jesFlavorQCDUp",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesFlavorQCDUp,
    ],
    output=[q.jet2_mass_jesFlavorQCDUp],
    scopes=["vbfhmm"],
)
#####end of jes FlavorQCD up#####
####begin of jes FlavorQCD down#####
JetPtCorrection_2022_jesFlavorQCDDown = Producer(
    name="JetPtCorrection_2022_jesFlavorQCDDown",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_FlavorQCD\"}}, -1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesFlavorQCDDown],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesFlavorQCDDown_GenMatch = Producer(
    name="JetPtCorrection_2022_jesFlavorQCDDown_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_FlavorQCD\"}}, -1,  {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesFlavorQCDDown],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesFlavorQCDDown = Producer(
    name="JetMassCorrection_jesFlavorQCDDown",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesFlavorQCDDown,
    ],
    output=[q.Jet_mass_corrected_jesFlavorQCDDown],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesFlavorQCDDown = ProducerGroup(
    name="JetEnergyCorrection_2022_jesFlavorQCDDown",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesFlavorQCDDown, JetMassCorrection_jesFlavorQCDDown],
)
JetEnergyCorrection_2022_jesFlavorQCDDown_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesFlavorQCDDown_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesFlavorQCDDown_GenMatch, JetMassCorrection_jesFlavorQCDDown],
)
### selecting jets
LVJet1_jesFlavorQCDDown = Producer(
    name="LVJet1_jesFlavorQCDDown",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesFlavorQCDDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesFlavorQCDDown,
    ],
    output=[q.jet_p4_1_jesFlavorQCDDown],
    scopes=["global","vbfhmm"],
)
LVJet2_jesFlavorQCDDown = Producer(
    name="LVJet2_jesFlavorQCDDown",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesFlavorQCDDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesFlavorQCDDown,
    ],
    output=[q.jet_p4_2_jesFlavorQCDDown],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesFlavorQCDDown = Producer(
    name="jet1_pt_jesFlavorQCDDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesFlavorQCDDown,
    ],
    output=[q.jet1_pt_jesFlavorQCDDown],
    scopes=["vbfhmm"],
)
jet1_mass_jesFlavorQCDDown = Producer(
    name="jet1_mass_jesFlavorQCDDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesFlavorQCDDown,
    ],
    output=[q.jet1_mass_jesFlavorQCDDown],
    scopes=["vbfhmm"],
)

jet2_pt_jesFlavorQCDDown = Producer(
    name="jet2_pt_jesFlavorQCDDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesFlavorQCDDown,
    ],
    output=[q.jet2_pt_jesFlavorQCDDown],
    scopes=["vbfhmm"],
)
jet2_mass_jesFlavorQCDDown = Producer(
    name="jet2_mass_jesFlavorQCDDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesFlavorQCDDown,
    ],
    output=[q.jet2_mass_jesFlavorQCDDown],
    scopes=["vbfhmm"],
)
#####end of jes FlavorQCD down#####
####begin of jes RelativeBal Up#####
JetPtCorrection_2022_jesRelativeBalUp = Producer(
    name="JetPtCorrection_2022_jesRelativeBalUp",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_RelativeBal\"}}, 1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesRelativeBalUp],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesRelativeBalUp_GenMatch = Producer(
    name="JetPtCorrection_2022_jesRelativeBalUp_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_RelativeBal\"}}, 1,  {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesRelativeBalUp],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesRelativeBalUp = Producer(
    name="JetMassCorrection_jesRelativeBalUp",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesRelativeBalUp,
    ],
    output=[q.Jet_mass_corrected_jesRelativeBalUp],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesRelativeBalUp = ProducerGroup(
    name="JetEnergyCorrection_2022_jesRelativeBalUp",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesRelativeBalUp, JetMassCorrection_jesRelativeBalUp],
)
JetEnergyCorrection_2022_jesRelativeBalUp_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesRelativeBalUp_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesRelativeBalUp_GenMatch, JetMassCorrection_jesRelativeBalUp],
)
### selecting jets
LVJet1_jesRelativeBalUp = Producer(
    name="LVJet1_jesRelativeBalUp",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesRelativeBalUp,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesRelativeBalUp,
    ],
    output=[q.jet_p4_1_jesRelativeBalUp],
    scopes=["global","vbfhmm"],
)
LVJet2_jesRelativeBalUp = Producer(
    name="LVJet2_jesRelativeBalUp",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesRelativeBalUp,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesRelativeBalUp,
    ],
    output=[q.jet_p4_2_jesRelativeBalUp],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesRelativeBalUp = Producer(
    name="jet1_pt_jesRelativeBalUp",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesRelativeBalUp,
    ],
    output=[q.jet1_pt_jesRelativeBalUp],
    scopes=["vbfhmm"],
)
jet1_mass_jesRelativeBalUp = Producer(
    name="jet1_mass_jesRelativeBalUp",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesRelativeBalUp,
    ],
    output=[q.jet1_mass_jesRelativeBalUp],
    scopes=["vbfhmm"],
)

jet2_pt_jesRelativeBalUp = Producer(
    name="jet2_pt_jesRelativeBalUp",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesRelativeBalUp,
    ],
    output=[q.jet2_pt_jesRelativeBalUp],
    scopes=["vbfhmm"],
)
jet2_mass_jesRelativeBalUp = Producer(
    name="jet2_mass_jesRelativeBalUp",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesRelativeBalUp,
    ],
    output=[q.jet2_mass_jesRelativeBalUp],
    scopes=["vbfhmm"],
)
#####end of jes RelativeBal Up#####
####begin of jes RelativeBal down#####
JetPtCorrection_2022_jesRelativeBalDown = Producer(
    name="JetPtCorrection_2022_jesRelativeBalDown",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_RelativeBal\"}}, -1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesRelativeBalDown],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesRelativeBalDown_GenMatch = Producer(
    name="JetPtCorrection_2022_jesRelativeBalDown_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_RelativeBal\"}}, -1,  {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesRelativeBalDown],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesRelativeBalDown = Producer(
    name="JetMassCorrection_jesRelativeBalDown",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesRelativeBalDown,
    ],
    output=[q.Jet_mass_corrected_jesRelativeBalDown],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesRelativeBalDown = ProducerGroup(
    name="JetEnergyCorrection_2022_jesRelativeBalDown",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesRelativeBalDown, JetMassCorrection_jesRelativeBalDown],
)
JetEnergyCorrection_2022_jesRelativeBalDown_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesRelativeBalDown_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesRelativeBalDown_GenMatch, JetMassCorrection_jesRelativeBalDown],
)
### selecting jets
LVJet1_jesRelativeBalDown = Producer(
    name="LVJet1_jesRelativeBalDown",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesRelativeBalDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesRelativeBalDown,
    ],
    output=[q.jet_p4_1_jesRelativeBalDown],
    scopes=["global","vbfhmm"],
)
LVJet2_jesRelativeBalDown = Producer(
    name="LVJet2_jesRelativeBalDown",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesRelativeBalDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesRelativeBalDown,
    ],
    output=[q.jet_p4_2_jesRelativeBalDown],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesRelativeBalDown = Producer(
    name="jet1_pt_jesRelativeBalDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesRelativeBalDown,
    ],
    output=[q.jet1_pt_jesRelativeBalDown],
    scopes=["vbfhmm"],
)
jet1_mass_jesRelativeBalDown = Producer(
    name="jet1_mass_jesRelativeBalDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesRelativeBalDown,
    ],
    output=[q.jet1_mass_jesRelativeBalDown],
    scopes=["vbfhmm"],
)

jet2_pt_jesRelativeBalDown = Producer(
    name="jet2_pt_jesRelativeBalDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesRelativeBalDown,
    ],
    output=[q.jet2_pt_jesRelativeBalDown],
    scopes=["vbfhmm"],
)
jet2_mass_jesRelativeBalDown = Producer(
    name="jet2_mass_jesRelativeBalDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesRelativeBalDown,
    ],
    output=[q.jet2_mass_jesRelativeBalDown],
    scopes=["vbfhmm"],
)
#####end of jes RelativeBal down#####
#####begin of jes HF up#####
JetPtCorrection_2022_jesHFUp = Producer(
    name="JetPtCorrection_2022_jesHFUp",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_HF\"}}, 1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesHFUp],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesHFUp_GenMatch = Producer(
    name="JetPtCorrection_2022_jesHFUp_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_HF\"}}, 1,  {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesHFUp],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesHFUp = Producer(
    name="JetMassCorrection_jesHFUp",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesHFUp,
    ],
    output=[q.Jet_mass_corrected_jesHFUp],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesHFUp = ProducerGroup(
    name="JetEnergyCorrection_2022_jesHFUp",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesHFUp, JetMassCorrection_jesHFUp],
)
JetEnergyCorrection_2022_jesHFUp_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesHFUp_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesHFUp_GenMatch, JetMassCorrection_jesHFUp],
)
### selecting jets
LVJet1_jesHFUp = Producer(
    name="LVJet1_jesHFUp",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesHFUp,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesHFUp,
    ],
    output=[q.jet_p4_1_jesHFUp],
    scopes=["global","vbfhmm"],
)
LVJet2_jesHFUp = Producer(
    name="LVJet2_jesHFUp",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesHFUp,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesHFUp,
    ],
    output=[q.jet_p4_2_jesHFUp],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesHFUp = Producer(
    name="jet1_pt_jesHFUp",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesHFUp,
    ],
    output=[q.jet1_pt_jesHFUp],
    scopes=["vbfhmm"],
)
jet1_mass_jesHFUp = Producer(
    name="jet1_mass_jesHFUp",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesHFUp,
    ],
    output=[q.jet1_mass_jesHFUp],
    scopes=["vbfhmm"],
)

jet2_pt_jesHFUp = Producer(
    name="jet2_pt_jesHFUp",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesHFUp,
    ],
    output=[q.jet2_pt_jesHFUp],
    scopes=["vbfhmm"],
)
jet2_mass_jesHFUp = Producer(
    name="jet2_mass_jesHFUp",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesHFUp,
    ],
    output=[q.jet2_mass_jesHFUp],
    scopes=["vbfhmm"],
)
#####end of jes HF up#####
####begin of jes HF down#####
JetPtCorrection_2022_jesHFDown = Producer(
    name="JetPtCorrection_2022_jesHFDown",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_HF\"}}, -1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesHFDown],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesHFDown_GenMatch = Producer(
    name="JetPtCorrection_2022_jesHFDown_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_HF\"}}, -1,  {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesHFDown],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesHFDown = Producer(
    name="JetMassCorrection_jesHFDown",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesHFDown,
    ],
    output=[q.Jet_mass_corrected_jesHFDown],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesHFDown = ProducerGroup(
    name="JetEnergyCorrection_2022_jesHFDown",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesHFDown, JetMassCorrection_jesHFDown],
)
JetEnergyCorrection_2022_jesHFDown_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesHFDown_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesHFDown_GenMatch, JetMassCorrection_jesHFDown],
)
### selecting jets
LVJet1_jesHFDown = Producer(
    name="LVJet1_jesHFDown",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesHFDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesHFDown,
    ],
    output=[q.jet_p4_1_jesHFDown],
    scopes=["global","vbfhmm"],
)
LVJet2_jesHFDown = Producer(
    name="LVJet2_jesHFDown",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesHFDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesHFDown,
    ],
    output=[q.jet_p4_2_jesHFDown],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesHFDown = Producer(
    name="jet1_pt_jesHFDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesHFDown,
    ],
    output=[q.jet1_pt_jesHFDown],
    scopes=["vbfhmm"],
)
jet1_mass_jesHFDown = Producer(
    name="jet1_mass_jesHFDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesHFDown,
    ],
    output=[q.jet1_mass_jesHFDown],
    scopes=["vbfhmm"],
)

jet2_pt_jesHFDown = Producer(
    name="jet2_pt_jesHFDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesHFDown,
    ],
    output=[q.jet2_pt_jesHFDown],
    scopes=["vbfhmm"],
)
jet2_mass_jesHFDown = Producer(
    name="jet2_mass_jesHFDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesHFDown,
    ],
    output=[q.jet2_mass_jesHFDown],
    scopes=["vbfhmm"],
)
#####end of jes HF down#####
#####begin of jes BBEC1 Up#####
JetPtCorrection_2022_jesBBEC1Up = Producer(
    name="JetPtCorrection_2022_jesBBEC1Up",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_BBEC1\"}}, 1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesBBEC1Up],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesBBEC1Up_GenMatch = Producer(
    name="JetPtCorrection_2022_jesBBEC1Up_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_BBEC1\"}}, 1,  {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesBBEC1Up],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesBBEC1Up = Producer(
    name="JetMassCorrection_jesBBEC1Up",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesBBEC1Up,
    ],
    output=[q.Jet_mass_corrected_jesBBEC1Up],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesBBEC1Up = ProducerGroup(
    name="JetEnergyCorrection_2022_jesBBEC1Up",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesBBEC1Up, JetMassCorrection_jesBBEC1Up],
)
JetEnergyCorrection_2022_jesBBEC1Up_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesBBEC1Up_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesBBEC1Up_GenMatch, JetMassCorrection_jesBBEC1Up],
)
### selecting jets
LVJet1_jesBBEC1Up = Producer(
    name="LVJet1_jesBBEC1Up",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesBBEC1Up,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesBBEC1Up,
    ],
    output=[q.jet_p4_1_jesBBEC1Up],
    scopes=["global","vbfhmm"],
)
LVJet2_jesBBEC1Up = Producer(
    name="LVJet2_jesBBEC1Up",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesBBEC1Up,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesBBEC1Up,
    ],
    output=[q.jet_p4_2_jesBBEC1Up],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesBBEC1Up = Producer(
    name="jet1_pt_jesBBEC1Up",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesBBEC1Up,
    ],
    output=[q.jet1_pt_jesBBEC1Up],
    scopes=["vbfhmm"],
)
jet1_mass_jesBBEC1Up = Producer(
    name="jet1_mass_jesBBEC1Up",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesBBEC1Up,
    ],
    output=[q.jet1_mass_jesBBEC1Up],
    scopes=["vbfhmm"],
)

jet2_pt_jesBBEC1Up = Producer(
    name="jet2_pt_jesBBEC1Up",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesBBEC1Up,
    ],
    output=[q.jet2_pt_jesBBEC1Up],
    scopes=["vbfhmm"],
)
jet2_mass_jesBBEC1Up = Producer(
    name="jet2_mass_jesBBEC1Up",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesBBEC1Up,
    ],
    output=[q.jet2_mass_jesBBEC1Up],
    scopes=["vbfhmm"],
)
#####end of jes BBEC1 up#####
####begin of jes BBEC1 down#####
JetPtCorrection_2022_jesBBEC1Down = Producer(
    name="JetPtCorrection_2022_jesBBEC1Down",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_BBEC1\"}}, -1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesBBEC1Down],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesBBEC1Down_GenMatch = Producer(
    name="JetPtCorrection_2022_jesBBEC1Down_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_BBEC1\"}}, -1,  {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesBBEC1Down],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesBBEC1Down = Producer(
    name="JetMassCorrection_jesBBEC1Down",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesBBEC1Down,
    ],
    output=[q.Jet_mass_corrected_jesBBEC1Down],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesBBEC1Down = ProducerGroup(
    name="JetEnergyCorrection_2022_jesBBEC1Down",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesBBEC1Down, JetMassCorrection_jesBBEC1Down],
)
JetEnergyCorrection_2022_jesBBEC1Down_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesBBEC1Down_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesBBEC1Down_GenMatch, JetMassCorrection_jesBBEC1Down],
)
### selecting jets
LVJet1_jesBBEC1Down = Producer(
    name="LVJet1_jesBBEC1Down",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesBBEC1Down,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesBBEC1Down,
    ],
    output=[q.jet_p4_1_jesBBEC1Down],
    scopes=["global","vbfhmm"],
)
LVJet2_jesBBEC1Down = Producer(
    name="LVJet2_jesBBEC1Down",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesBBEC1Down,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesBBEC1Down,
    ],
    output=[q.jet_p4_2_jesBBEC1Down],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesBBEC1Down = Producer(
    name="jet1_pt_jesBBEC1Down",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesBBEC1Down,
    ],
    output=[q.jet1_pt_jesBBEC1Down],
    scopes=["vbfhmm"],
)
jet1_mass_jesBBEC1Down = Producer(
    name="jet1_mass_jesBBEC1Down",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesBBEC1Down,
    ],
    output=[q.jet1_mass_jesBBEC1Down],
    scopes=["vbfhmm"],
)

jet2_pt_jesBBEC1Down = Producer(
    name="jet2_pt_jesBBEC1Down",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesBBEC1Down,
    ],
    output=[q.jet2_pt_jesBBEC1Down],
    scopes=["vbfhmm"],
)
jet2_mass_jesBBEC1Down = Producer(
    name="jet2_mass_jesBBEC1Down",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesBBEC1Down,
    ],
    output=[q.jet2_mass_jesBBEC1Down],
    scopes=["vbfhmm"],
)
#####end of jes BBEC1 down#####
#####begin of jes EC2 Up#####
JetPtCorrection_2022_jesEC2Up = Producer(
    name="JetPtCorrection_2022_jesEC2Up",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_EC2\"}}, 1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesEC2Up],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesEC2Up_GenMatch = Producer(
    name="JetPtCorrection_2022_jesEC2Up_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_EC2\"}}, 1,  {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesEC2Up],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesEC2Up = Producer(
    name="JetMassCorrection_jesEC2Up",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesEC2Up,
    ],
    output=[q.Jet_mass_corrected_jesEC2Up],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesEC2Up = ProducerGroup(
    name="JetEnergyCorrection_2022_jesEC2Up",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesEC2Up, JetMassCorrection_jesEC2Up],
)
JetEnergyCorrection_2022_jesEC2Up_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesEC2Up_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesEC2Up_GenMatch, JetMassCorrection_jesEC2Up],
)
### selecting jets
LVJet1_jesEC2Up = Producer(
    name="LVJet1_jesEC2Up",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesEC2Up,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesEC2Up,
    ],
    output=[q.jet_p4_1_jesEC2Up],
    scopes=["global","vbfhmm"],
)
LVJet2_jesEC2Up = Producer(
    name="LVJet2_jesEC2Up",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesEC2Up,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesEC2Up,
    ],
    output=[q.jet_p4_2_jesEC2Up],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesEC2Up = Producer(
    name="jet1_pt_jesEC2Up",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesEC2Up,
    ],
    output=[q.jet1_pt_jesEC2Up],
    scopes=["vbfhmm"],
)
jet1_mass_jesEC2Up = Producer(
    name="jet1_mass_jesEC2Up",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesEC2Up,
    ],
    output=[q.jet1_mass_jesEC2Up],
    scopes=["vbfhmm"],
)

jet2_pt_jesEC2Up = Producer(
    name="jet2_pt_jesEC2Up",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesEC2Up,
    ],
    output=[q.jet2_pt_jesEC2Up],
    scopes=["vbfhmm"],
)
jet2_mass_jesEC2Up = Producer(
    name="jet2_mass_jesEC2Up",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesEC2Up,
    ],
    output=[q.jet2_mass_jesEC2Up],
    scopes=["vbfhmm"],
)
#####end of jes EC2 up#####
####begin of jes EC2 down#####
JetPtCorrection_2022_jesEC2Down = Producer(
    name="JetPtCorrection_2022_jesEC2Down",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_EC2\"}}, -1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesEC2Down],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesEC2Down_GenMatch = Producer(
    name="JetPtCorrection_2022_jesEC2Down_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_EC2\"}}, -1,  {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesEC2Down],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesEC2Down = Producer(
    name="JetMassCorrection_jesEC2Down",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesEC2Down,
    ],
    output=[q.Jet_mass_corrected_jesEC2Down],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesEC2Down = ProducerGroup(
    name="JetEnergyCorrection_2022_jesEC2Down",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesEC2Down, JetMassCorrection_jesEC2Down],
)
JetEnergyCorrection_2022_jesEC2Down_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesEC2Down_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesEC2Down_GenMatch, JetMassCorrection_jesEC2Down],
)
### selecting jets
LVJet1_jesEC2Down = Producer(
    name="LVJet1_jesEC2Down",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesEC2Down,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesEC2Down,
    ],
    output=[q.jet_p4_1_jesEC2Down],
    scopes=["global","vbfhmm"],
)
LVJet2_jesEC2Down = Producer(
    name="LVJet2_jesEC2Down",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesEC2Down,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesEC2Down,
    ],
    output=[q.jet_p4_2_jesEC2Down],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesEC2Down = Producer(
    name="jet1_pt_jesEC2Down",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesEC2Down,
    ],
    output=[q.jet1_pt_jesEC2Down],
    scopes=["vbfhmm"],
)
jet1_mass_jesEC2Down = Producer(
    name="jet1_mass_jesEC2Down",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesEC2Down,
    ],
    output=[q.jet1_mass_jesEC2Down],
    scopes=["vbfhmm"],
)

jet2_pt_jesEC2Down = Producer(
    name="jet2_pt_jesEC2Down",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesEC2Down,
    ],
    output=[q.jet2_pt_jesEC2Down],
    scopes=["vbfhmm"],
)
jet2_mass_jesEC2Down = Producer(
    name="jet2_mass_jesEC2Down",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesEC2Down,
    ],
    output=[q.jet2_mass_jesEC2Down],
    scopes=["vbfhmm"],
)
#####end of jes EC2 down#####
#####begin of jes Absolute Up#####
JetPtCorrection_2022_jesAbsoluteUp = Producer(
    name="JetPtCorrection_2022_jesAbsoluteUp",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_Absolute\"}}, 1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesAbsoluteUp],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesAbsoluteUp_GenMatch = Producer(
    name="JetPtCorrection_2022_jesAbsoluteUp_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_Absolute\"}}, 1,  {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesAbsoluteUp],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesAbsoluteUp = Producer(
    name="JetMassCorrection_jesAbsoluteUp",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesAbsoluteUp,
    ],
    output=[q.Jet_mass_corrected_jesAbsoluteUp],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesAbsoluteUp = ProducerGroup(
    name="JetEnergyCorrection_2022_jesAbsoluteUp",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesAbsoluteUp, JetMassCorrection_jesAbsoluteUp],
)
JetEnergyCorrection_2022_jesAbsoluteUp_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesAbsoluteUp_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesAbsoluteUp_GenMatch, JetMassCorrection_jesAbsoluteUp],
)
### selecting jets
LVJet1_jesAbsoluteUp = Producer(
    name="LVJet1_jesAbsoluteUp",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesAbsoluteUp,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesAbsoluteUp,
    ],
    output=[q.jet_p4_1_jesAbsoluteUp],
    scopes=["global","vbfhmm"],
)
LVJet2_jesAbsoluteUp = Producer(
    name="LVJet2_jesAbsoluteUp",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesAbsoluteUp,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesAbsoluteUp,
    ],
    output=[q.jet_p4_2_jesAbsoluteUp],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesAbsoluteUp = Producer(
    name="jet1_pt_jesAbsoluteUp",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesAbsoluteUp,
    ],
    output=[q.jet1_pt_jesAbsoluteUp],
    scopes=["vbfhmm"],
)
jet1_mass_jesAbsoluteUp = Producer(
    name="jet1_mass_jesAbsoluteUp",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesAbsoluteUp,
    ],
    output=[q.jet1_mass_jesAbsoluteUp],
    scopes=["vbfhmm"],
)

jet2_pt_jesAbsoluteUp = Producer(
    name="jet2_pt_jesAbsoluteUp",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesAbsoluteUp,
    ],
    output=[q.jet2_pt_jesAbsoluteUp],
    scopes=["vbfhmm"],
)
jet2_mass_jesAbsoluteUp = Producer(
    name="jet2_mass_jesAbsoluteUp",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesAbsoluteUp,
    ],
    output=[q.jet2_mass_jesAbsoluteUp],
    scopes=["vbfhmm"],
)
#####end of jes Absolute up#####
####begin of jes Absolute down#####
JetPtCorrection_2022_jesAbsoluteDown = Producer(
    name="JetPtCorrection_2022_jesAbsoluteDown",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_Absolute\"}}, -1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesAbsoluteDown],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesAbsoluteDown_GenMatch = Producer(
    name="JetPtCorrection_2022_jesAbsoluteDown_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_Absolute\"}}, -1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag},{jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesAbsoluteDown],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesAbsoluteDown = Producer(
    name="JetMassCorrection_jesAbsoluteDown",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesAbsoluteDown,
    ],
    output=[q.Jet_mass_corrected_jesAbsoluteDown],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesAbsoluteDown = ProducerGroup(
    name="JetEnergyCorrection_2022_jesAbsoluteDown",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesAbsoluteDown, JetMassCorrection_jesAbsoluteDown],
)
JetEnergyCorrection_2022_jesAbsoluteDown_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesAbsoluteDown_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesAbsoluteDown_GenMatch, JetMassCorrection_jesAbsoluteDown],
)
### selecting jets
LVJet1_jesAbsoluteDown = Producer(
    name="LVJet1_jesAbsoluteDown",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesAbsoluteDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesAbsoluteDown,
    ],
    output=[q.jet_p4_1_jesAbsoluteDown],
    scopes=["global","vbfhmm"],
)
LVJet2_jesAbsoluteDown = Producer(
    name="LVJet2_jesAbsoluteDown",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesAbsoluteDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesAbsoluteDown,
    ],
    output=[q.jet_p4_2_jesAbsoluteDown],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesAbsoluteDown = Producer(
    name="jet1_pt_jesAbsoluteDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesAbsoluteDown,
    ],
    output=[q.jet1_pt_jesAbsoluteDown],
    scopes=["vbfhmm"],
)
jet1_mass_jesAbsoluteDown = Producer(
    name="jet1_mass_jesAbsoluteDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesAbsoluteDown,
    ],
    output=[q.jet1_mass_jesAbsoluteDown],
    scopes=["vbfhmm"],
)

jet2_pt_jesAbsoluteDown = Producer(
    name="jet2_pt_jesAbsoluteDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesAbsoluteDown,
    ],
    output=[q.jet2_pt_jesAbsoluteDown],
    scopes=["vbfhmm"],
)
jet2_mass_jesAbsoluteDown = Producer(
    name="jet2_mass_jesAbsoluteDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesAbsoluteDown,
    ],
    output=[q.jet2_mass_jesAbsoluteDown],
    scopes=["vbfhmm"],
)
#####end of jes Absolute down#####
#####begin of jes BBEC1 era Up#####
JetPtCorrection_2022_jesBBEC1_eraUp = Producer(
    name="JetPtCorrection_2022_jesBBEC1_eraUp",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_BBEC1\"}}, 1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesBBEC1_eraUp],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesBBEC1_eraUp_GenMatch = Producer(
    name="JetPtCorrection_2022_jesBBEC1_eraUp_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_BBEC1\"}}, 1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesBBEC1_eraUp],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesBBEC1_eraUp = Producer(
    name="JetMassCorrection_jesBBEC1_eraUp",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesBBEC1_eraUp,
    ],
    output=[q.Jet_mass_corrected_jesBBEC1_eraUp],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesBBEC1_eraUp = ProducerGroup(
    name="JetEnergyCorrection_2022_jesBBEC1_eraUp",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesBBEC1_eraUp, JetMassCorrection_jesBBEC1_eraUp],
)
JetEnergyCorrection_2022_jesBBEC1_eraUp_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesBBEC1_eraUp_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesBBEC1_eraUp_GenMatch, JetMassCorrection_jesBBEC1_eraUp],
)
### selecting jets
LVJet1_jesBBEC1_eraUp = Producer(
    name="LVJet1_jesBBEC1_eraUp",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesBBEC1_eraUp,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesBBEC1_eraUp,
    ],
    output=[q.jet_p4_1_jesBBEC1_eraUp],
    scopes=["global","vbfhmm"],
)
LVJet2_jesBBEC1_eraUp = Producer(
    name="LVJet2_jesBBEC1_eraUp",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesBBEC1_eraUp,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesBBEC1_eraUp,
    ],
    output=[q.jet_p4_2_jesBBEC1_eraUp],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesBBEC1_eraUp = Producer(
    name="jet1_pt_jesBBEC1_eraUp",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesBBEC1_eraUp,
    ],
    output=[q.jet1_pt_jesBBEC1_eraUp],
    scopes=["vbfhmm"],
)
jet1_mass_jesBBEC1_eraUp = Producer(
    name="jet1_mass_jesBBEC1_eraUp",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesBBEC1_eraUp,
    ],
    output=[q.jet1_mass_jesBBEC1_eraUp],
    scopes=["vbfhmm"],
)

jet2_pt_jesBBEC1_eraUp = Producer(
    name="jet2_pt_jesBBEC1_eraUp",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesBBEC1_eraUp,
    ],
    output=[q.jet2_pt_jesBBEC1_eraUp],
    scopes=["vbfhmm"],
)
jet2_mass_jesBBEC1_eraUp = Producer(
    name="jet2_mass_jesBBEC1_eraUp",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesBBEC1_eraUp,
    ],
    output=[q.jet2_mass_jesBBEC1_eraUp],
    scopes=["vbfhmm"],
)
#####end of jes BBEC1 era up#####
####begin of jes BBEC1 era down#####
JetPtCorrection_2022_jesBBEC1_eraDown = Producer(
    name="JetPtCorrection_2022_jesBBEC1_eraDown",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_BBEC1\"}}, -1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesBBEC1_eraDown],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesBBEC1_eraDown_GenMatch = Producer(
    name="JetPtCorrection_2022_jesBBEC1_eraDown_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_BBEC1\"}}, -1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesBBEC1_eraDown],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesBBEC1_eraDown = Producer(
    name="JetMassCorrection_jesBBEC1_eraDown",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesBBEC1_eraDown,
    ],
    output=[q.Jet_mass_corrected_jesBBEC1_eraDown],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesBBEC1_eraDown = ProducerGroup(
    name="JetEnergyCorrection_2022_jesBBEC1_eraDown",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesBBEC1_eraDown, JetMassCorrection_jesBBEC1_eraDown],
)
JetEnergyCorrection_2022_jesBBEC1_eraDown_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesBBEC1_eraDown_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesBBEC1_eraDown_GenMatch, JetMassCorrection_jesBBEC1_eraDown],
)
### selecting jets
LVJet1_jesBBEC1_eraDown = Producer(
    name="LVJet1_jesBBEC1_eraDown",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesBBEC1_eraDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesBBEC1_eraDown,
    ],
    output=[q.jet_p4_1_jesBBEC1_eraDown],
    scopes=["global","vbfhmm"],
)
LVJet2_jesBBEC1_eraDown = Producer(
    name="LVJet2_jesBBEC1_eraDown",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesBBEC1_eraDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesBBEC1_eraDown,
    ],
    output=[q.jet_p4_2_jesBBEC1_eraDown],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesBBEC1_eraDown = Producer(
    name="jet1_pt_jesBBEC1_eraDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesBBEC1_eraDown,
    ],
    output=[q.jet1_pt_jesBBEC1_eraDown],
    scopes=["vbfhmm"],
)
jet1_mass_jesBBEC1_eraDown = Producer(
    name="jet1_mass_jesBBEC1_eraDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesBBEC1_eraDown,
    ],
    output=[q.jet1_mass_jesBBEC1_eraDown],
    scopes=["vbfhmm"],
)

jet2_pt_jesBBEC1_eraDown = Producer(
    name="jet2_pt_jesBBEC1_eraDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesBBEC1_eraDown,
    ],
    output=[q.jet2_pt_jesBBEC1_eraDown],
    scopes=["vbfhmm"],
)
jet2_mass_jesBBEC1_eraDown = Producer(
    name="jet2_mass_jesBBEC1_eraDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesBBEC1_eraDown,
    ],
    output=[q.jet2_mass_jesBBEC1_eraDown],
    scopes=["vbfhmm"],
)
#####end of jes BBEC1 era down#####
#####begin of jes RelativeSample Up#####
JetPtCorrection_2022_jesRelativeSample_eraUp = Producer(
    name="JetPtCorrection_2022_jesRelativeSample_eraUp",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_RelativeSample\"}}, 1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesRelativeSample_eraUp],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesRelativeSample_eraUp_GenMatch = Producer(
    name="JetPtCorrection_2022_jesRelativeSample_eraUp_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_RelativeSample\"}}, 1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesRelativeSample_eraUp],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesRelativeSample_eraUp = Producer(
    name="JetMassCorrection_jesRelativeSample_eraUp",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesRelativeSample_eraUp,
    ],
    output=[q.Jet_mass_corrected_jesRelativeSample_eraUp],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesRelativeSample_eraUp = ProducerGroup(
    name="JetEnergyCorrection_2022_jesRelativeSample_eraUp",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesRelativeSample_eraUp, JetMassCorrection_jesRelativeSample_eraUp],
)
JetEnergyCorrection_2022_jesRelativeSample_eraUp_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesRelativeSample_eraUp_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesRelativeSample_eraUp_GenMatch, JetMassCorrection_jesRelativeSample_eraUp],
)
### selecting jets
LVJet1_jesRelativeSample_eraUp = Producer(
    name="LVJet1_jesRelativeSample_eraUp",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesRelativeSample_eraUp,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesRelativeSample_eraUp,
    ],
    output=[q.jet_p4_1_jesRelativeSample_eraUp],
    scopes=["global","vbfhmm"],
)
LVJet2_jesRelativeSample_eraUp = Producer(
    name="LVJet2_jesRelativeSample_eraUp",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesRelativeSample_eraUp,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesRelativeSample_eraUp,
    ],
    output=[q.jet_p4_2_jesRelativeSample_eraUp],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesRelativeSample_eraUp = Producer(
    name="jet1_pt_jesRelativeSample_eraUp",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesRelativeSample_eraUp,
    ],
    output=[q.jet1_pt_jesRelativeSample_eraUp],
    scopes=["vbfhmm"],
)
jet1_mass_jesRelativeSample_eraUp = Producer(
    name="jet1_mass_jesRelativeSample_eraUp",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesRelativeSample_eraUp,
    ],
    output=[q.jet1_mass_jesRelativeSample_eraUp],
    scopes=["vbfhmm"],
)

jet2_pt_jesRelativeSample_eraUp = Producer(
    name="jet2_pt_jesRelativeSample_eraUp",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesRelativeSample_eraUp,
    ],
    output=[q.jet2_pt_jesRelativeSample_eraUp],
    scopes=["vbfhmm"],
)
jet2_mass_jesRelativeSample_eraUp = Producer(
    name="jet2_mass_jesRelativeSample_eraUp",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesRelativeSample_eraUp,
    ],
    output=[q.jet2_mass_jesRelativeSample_eraUp],
    scopes=["vbfhmm"],
)
#####end of jes RelativeSample era up#####
####begin of jes RelativeSample era down#####
JetPtCorrection_2022_jesRelativeSample_eraDown = Producer(
    name="JetPtCorrection_2022_jesRelativeSample_eraDown",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_RelativeSample\"}}, -1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesRelativeSample_eraDown],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesRelativeSample_eraDown_GenMatch = Producer(
    name="JetPtCorrection_2022_jesRelativeSample_eraDown_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_RelativeSample\"}}, -1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesRelativeSample_eraDown],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesRelativeSample_eraDown = Producer(
    name="JetMassCorrection_jesRelativeSample_eraDown",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesRelativeSample_eraDown,
    ],
    output=[q.Jet_mass_corrected_jesRelativeSample_eraDown],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesRelativeSample_eraDown = ProducerGroup(
    name="JetEnergyCorrection_2022_jesRelativeSample_eraDown",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesRelativeSample_eraDown, JetMassCorrection_jesRelativeSample_eraDown],
)
JetEnergyCorrection_2022_jesRelativeSample_eraDown_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesRelativeSample_eraDown_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesRelativeSample_eraDown_GenMatch, JetMassCorrection_jesRelativeSample_eraDown],
)
### selecting jets
LVJet1_jesRelativeSample_eraDown = Producer(
    name="LVJet1_jesRelativeSample_eraDown",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesRelativeSample_eraDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesRelativeSample_eraDown,
    ],
    output=[q.jet_p4_1_jesRelativeSample_eraDown],
    scopes=["global","vbfhmm"],
)
LVJet2_jesRelativeSample_eraDown = Producer(
    name="LVJet2_jesRelativeSample_eraDown",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesRelativeSample_eraDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesRelativeSample_eraDown,
    ],
    output=[q.jet_p4_2_jesRelativeSample_eraDown],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesRelativeSample_eraDown = Producer(
    name="jet1_pt_jesRelativeSample_eraDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesRelativeSample_eraDown,
    ],
    output=[q.jet1_pt_jesRelativeSample_eraDown],
    scopes=["vbfhmm"],
)
jet1_mass_jesRelativeSample_eraDown = Producer(
    name="jet1_mass_jesRelativeSample_eraDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesRelativeSample_eraDown,
    ],
    output=[q.jet1_mass_jesRelativeSample_eraDown],
    scopes=["vbfhmm"],
)

jet2_pt_jesRelativeSample_eraDown = Producer(
    name="jet2_pt_jesRelativeSample_eraDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesRelativeSample_eraDown,
    ],
    output=[q.jet2_pt_jesRelativeSample_eraDown],
    scopes=["vbfhmm"],
)
jet2_mass_jesRelativeSample_eraDown = Producer(
    name="jet2_mass_jesRelativeSample_eraDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesRelativeSample_eraDown,
    ],
    output=[q.jet2_mass_jesRelativeSample_eraDown],
    scopes=["vbfhmm"],
)
#####end of jes RelativeSample era down#####
#####begin of jes EC2 era Up#####
JetPtCorrection_2022_jesEC2_eraUp = Producer(
    name="JetPtCorrection_2022_jesEC2_eraUp",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_EC2\"}}, 1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesEC2_eraUp],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesEC2_eraUp_GenMatch = Producer(
    name="JetPtCorrection_2022_jesEC2_eraUp_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_EC2\"}}, 1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesEC2_eraUp],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesEC2_eraUp = Producer(
    name="JetMassCorrection_jesEC2_eraUp",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesEC2_eraUp,
    ],
    output=[q.Jet_mass_corrected_jesEC2_eraUp],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesEC2_eraUp = ProducerGroup(
    name="JetEnergyCorrection_2022_jesEC2_eraUp",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesEC2_eraUp, JetMassCorrection_jesEC2_eraUp],
)
JetEnergyCorrection_2022_jesEC2_eraUp_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesEC2_eraUp_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesEC2_eraUp_GenMatch, JetMassCorrection_jesEC2_eraUp],
)
### selecting jets
LVJet1_jesEC2_eraUp = Producer(
    name="LVJet1_jesEC2_eraUp",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesEC2_eraUp,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesEC2_eraUp,
    ],
    output=[q.jet_p4_1_jesEC2_eraUp],
    scopes=["global","vbfhmm"],
)
LVJet2_jesEC2_eraUp = Producer(
    name="LVJet2_jesEC2_eraUp",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesEC2_eraUp,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesEC2_eraUp,
    ],
    output=[q.jet_p4_2_jesEC2_eraUp],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesEC2_eraUp = Producer(
    name="jet1_pt_jesEC2_eraUp",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesEC2_eraUp,
    ],
    output=[q.jet1_pt_jesEC2_eraUp],
    scopes=["vbfhmm"],
)
jet1_mass_jesEC2_eraUp = Producer(
    name="jet1_mass_jesEC2_eraUp",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesEC2_eraUp,
    ],
    output=[q.jet1_mass_jesEC2_eraUp],
    scopes=["vbfhmm"],
)

jet2_pt_jesEC2_eraUp = Producer(
    name="jet2_pt_jesEC2_eraUp",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesEC2_eraUp,
    ],
    output=[q.jet2_pt_jesEC2_eraUp],
    scopes=["vbfhmm"],
)
jet2_mass_jesEC2_eraUp = Producer(
    name="jet2_mass_jesEC2_eraUp",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesEC2_eraUp,
    ],
    output=[q.jet2_mass_jesEC2_eraUp],
    scopes=["vbfhmm"],
)
#####end of jes EC2 era up#####
####begin of jes EC2 era down#####
JetPtCorrection_2022_jesEC2_eraDown = Producer(
    name="JetPtCorrection_2022_jesEC2_eraDown",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_EC2\"}}, -1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesEC2_eraDown],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesEC2_eraDown_GenMatch = Producer(
    name="JetPtCorrection_2022_jesEC2_eraDown_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_EC2\"}}, -1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesEC2_eraDown],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesEC2_eraDown = Producer(
    name="JetMassCorrection_jesEC2_eraDown",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesEC2_eraDown,
    ],
    output=[q.Jet_mass_corrected_jesEC2_eraDown],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesEC2_eraDown = ProducerGroup(
    name="JetEnergyCorrection_2022_jesEC2_eraDown",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesEC2_eraDown, JetMassCorrection_jesEC2_eraDown],
)
JetEnergyCorrection_2022_jesEC2_eraDown_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesEC2_eraDown_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesEC2_eraDown_GenMatch, JetMassCorrection_jesEC2_eraDown],
)
### selecting jets
LVJet1_jesEC2_eraDown = Producer(
    name="LVJet1_jesEC2_eraDown",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesEC2_eraDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesEC2_eraDown,
    ],
    output=[q.jet_p4_1_jesEC2_eraDown],
    scopes=["global","vbfhmm"],
)
LVJet2_jesEC2_eraDown = Producer(
    name="LVJet2_jesEC2_eraDown",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesEC2_eraDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesEC2_eraDown,
    ],
    output=[q.jet_p4_2_jesEC2_eraDown],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesEC2_eraDown = Producer(
    name="jet1_pt_jesEC2_eraDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesEC2_eraDown,
    ],
    output=[q.jet1_pt_jesEC2_eraDown],
    scopes=["vbfhmm"],
)
jet1_mass_jesEC2_eraDown = Producer(
    name="jet1_mass_jesEC2_eraDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesEC2_eraDown,
    ],
    output=[q.jet1_mass_jesEC2_eraDown],
    scopes=["vbfhmm"],
)

jet2_pt_jesEC2_eraDown = Producer(
    name="jet2_pt_jesEC2_eraDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesEC2_eraDown,
    ],
    output=[q.jet2_pt_jesEC2_eraDown],
    scopes=["vbfhmm"],
)
jet2_mass_jesEC2_eraDown = Producer(
    name="jet2_mass_jesEC2_eraDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesEC2_eraDown,
    ],
    output=[q.jet2_mass_jesEC2_eraDown],
    scopes=["vbfhmm"],
)
#####end of jes EC2 era down#####
#####begin of jes HF era Up#####
JetPtCorrection_2022_jesHF_eraUp = Producer(
    name="JetPtCorrection_2022_jesHF_eraUp",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_HF\"}}, 1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesHF_eraUp],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesHF_eraUp_GenMatch = Producer(
    name="JetPtCorrection_2022_jesHF_eraUp_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_HF\"}}, 1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesHF_eraUp],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesHF_eraUp = Producer(
    name="JetMassCorrection_jesHF_eraUp",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesHF_eraUp,
    ],
    output=[q.Jet_mass_corrected_jesHF_eraUp],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesHF_eraUp = ProducerGroup(
    name="JetEnergyCorrection_2022_jesHF_eraUp",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesHF_eraUp, JetMassCorrection_jesHF_eraUp],
)
JetEnergyCorrection_2022_jesHF_eraUp_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesHF_eraUp_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesHF_eraUp_GenMatch, JetMassCorrection_jesHF_eraUp],
)
### selecting jets
LVJet1_jesHF_eraUp = Producer(
    name="LVJet1_jesHF_eraUp",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesHF_eraUp,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesHF_eraUp,
    ],
    output=[q.jet_p4_1_jesHF_eraUp],
    scopes=["global","vbfhmm"],
)
LVJet2_jesHF_eraUp = Producer(
    name="LVJet2_jesHF_eraUp",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesHF_eraUp,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesHF_eraUp,
    ],
    output=[q.jet_p4_2_jesHF_eraUp],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesHF_eraUp = Producer(
    name="jet1_pt_jesHF_eraUp",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesHF_eraUp,
    ],
    output=[q.jet1_pt_jesHF_eraUp],
    scopes=["vbfhmm"],
)
jet1_mass_jesHF_eraUp = Producer(
    name="jet1_mass_jesHF_eraUp",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesHF_eraUp,
    ],
    output=[q.jet1_mass_jesHF_eraUp],
    scopes=["vbfhmm"],
)

jet2_pt_jesHF_eraUp = Producer(
    name="jet2_pt_jesHF_eraUp",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesHF_eraUp,
    ],
    output=[q.jet2_pt_jesHF_eraUp],
    scopes=["vbfhmm"],
)
jet2_mass_jesHF_eraUp = Producer(
    name="jet2_mass_jesHF_eraUp",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesHF_eraUp,
    ],
    output=[q.jet2_mass_jesHF_eraUp],
    scopes=["vbfhmm"],
)
#####end of jes HF era up#####
####begin of jes HF era Down#####
JetPtCorrection_2022_jesHF_eraDown = Producer(
    name="JetPtCorrection_2022_jesHF_eraDown",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_HF\"}}, -1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesHF_eraDown],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesHF_eraDown_GenMatch = Producer(
    name="JetPtCorrection_2022_jesHF_eraDown_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_HF\"}}, -1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesHF_eraDown],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesHF_eraDown = Producer(
    name="JetMassCorrection_jesHF_eraDown",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesHF_eraDown,
    ],
    output=[q.Jet_mass_corrected_jesHF_eraDown],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesHF_eraDown = ProducerGroup(
    name="JetEnergyCorrection_2022_jesHF_eraDown",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesHF_eraDown, JetMassCorrection_jesHF_eraDown],
)
JetEnergyCorrection_2022_jesHF_eraDown_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesHF_eraDown_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesHF_eraDown_GenMatch, JetMassCorrection_jesHF_eraDown],
)
### selecting jets
LVJet1_jesHF_eraDown = Producer(
    name="LVJet1_jesHF_eraDown",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesHF_eraDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesHF_eraDown,
    ],
    output=[q.jet_p4_1_jesHF_eraDown],
    scopes=["global","vbfhmm"],
)
LVJet2_jesHF_eraDown = Producer(
    name="LVJet2_jesHF_eraDown",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesHF_eraDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesHF_eraDown,
    ],
    output=[q.jet_p4_2_jesHF_eraDown],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesHF_eraDown = Producer(
    name="jet1_pt_jesHF_eraDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesHF_eraDown,
    ],
    output=[q.jet1_pt_jesHF_eraDown],
    scopes=["vbfhmm"],
)
jet1_mass_jesHF_eraDown = Producer(
    name="jet1_mass_jesHF_eraDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesHF_eraDown,
    ],
    output=[q.jet1_mass_jesHF_eraDown],
    scopes=["vbfhmm"],
)

jet2_pt_jesHF_eraDown = Producer(
    name="jet2_pt_jesHF_eraDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesHF_eraDown,
    ],
    output=[q.jet2_pt_jesHF_eraDown],
    scopes=["vbfhmm"],
)
jet2_mass_jesHF_eraDown = Producer(
    name="jet2_mass_jesHF_eraDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesHF_eraDown,
    ],
    output=[q.jet2_mass_jesHF_eraDown],
    scopes=["vbfhmm"],
)
#####end of jes HF era down#####
#####begin of jes Absolute era Up#####
JetPtCorrection_2022_jesAbsolute_eraUp = Producer(
    name="JetPtCorrection_2022_jesAbsolute_eraUp",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_Absolute\"}}, 1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesAbsolute_eraUp],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesAbsolute_eraUp_GenMatch = Producer(
    name="JetPtCorrection_2022_jesAbsolute_eraUp_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_Absolute\"}}, 1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesAbsolute_eraUp],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesAbsolute_eraUp = Producer(
    name="JetMassCorrection_jesAbsolute_eraUp",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesAbsolute_eraUp,
    ],
    output=[q.Jet_mass_corrected_jesAbsolute_eraUp],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesAbsolute_eraUp = ProducerGroup(
    name="JetEnergyCorrection_2022_jesAbsolute_eraUp",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesAbsolute_eraUp, JetMassCorrection_jesAbsolute_eraUp],
)
JetEnergyCorrection_2022_jesAbsolute_eraUp_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesAbsolute_eraUp_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesAbsolute_eraUp_GenMatch, JetMassCorrection_jesAbsolute_eraUp],
)
### selecting jets
LVJet1_jesAbsolute_eraUp = Producer(
    name="LVJet1_jesAbsolute_eraUp",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesAbsolute_eraUp,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesAbsolute_eraUp,
    ],
    output=[q.jet_p4_1_jesAbsolute_eraUp],
    scopes=["global","vbfhmm"],
)
LVJet2_jesAbsolute_eraUp = Producer(
    name="LVJet2_jesAbsolute_eraUp",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesAbsolute_eraUp,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesAbsolute_eraUp,
    ],
    output=[q.jet_p4_2_jesAbsolute_eraUp],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesAbsolute_eraUp = Producer(
    name="jet1_pt_jesAbsolute_eraUp",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesAbsolute_eraUp,
    ],
    output=[q.jet1_pt_jesAbsolute_eraUp],
    scopes=["vbfhmm"],
)
jet1_mass_jesAbsolute_eraUp = Producer(
    name="jet1_mass_jesAbsolute_eraUp",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesAbsolute_eraUp,
    ],
    output=[q.jet1_mass_jesAbsolute_eraUp],
    scopes=["vbfhmm"],
)

jet2_pt_jesAbsolute_eraUp = Producer(
    name="jet2_pt_jesAbsolute_eraUp",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesAbsolute_eraUp,
    ],
    output=[q.jet2_pt_jesAbsolute_eraUp],
    scopes=["vbfhmm"],
)
jet2_mass_jesAbsolute_eraUp = Producer(
    name="jet2_mass_jesAbsolute_eraUp",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesAbsolute_eraUp,
    ],
    output=[q.jet2_mass_jesAbsolute_eraUp],
    scopes=["vbfhmm"],
)
#####end of jes Absolute era up#####
####begin of jes Absolute era Down#####
JetPtCorrection_2022_jesAbsolute_eraDown = Producer(
    name="JetPtCorrection_2022_jesAbsolute_eraDown",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_202223({df}, {output}, {input}, true, {{\"Regrouped_Absolute\"}}, -1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected_jesAbsolute_eraDown],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesAbsolute_eraDown_GenMatch = Producer(
    name="JetPtCorrection_2022_jesAbsolute_eraDown_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, true, {{\"Regrouped_Absolute\"}}, -1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesAbsolute_eraDown],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesAbsolute_eraDown = Producer(
    name="JetMassCorrection_jesAbsolute_eraDown",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesAbsolute_eraDown,
    ],
    output=[q.Jet_mass_corrected_jesAbsolute_eraDown],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesAbsolute_eraDown = ProducerGroup(
    name="JetEnergyCorrection_2022_jesAbsolute_eraDown",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesAbsolute_eraDown, JetMassCorrection_jesAbsolute_eraDown],
)
JetEnergyCorrection_2022_jesAbsolute_eraDown_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesAbsolute_eraDown_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesAbsolute_eraDown_GenMatch, JetMassCorrection_jesAbsolute_eraDown],
)
### selecting jets
LVJet1_jesAbsolute_eraDown = Producer(
    name="LVJet1_jesAbsolute_eraDown",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesAbsolute_eraDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesAbsolute_eraDown,
    ],
    output=[q.jet_p4_1_jesAbsolute_eraDown],
    scopes=["global","vbfhmm"],
)
LVJet2_jesAbsolute_eraDown = Producer(
    name="LVJet2_jesAbsolute_eraDown",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesAbsolute_eraDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesAbsolute_eraDown,
    ],
    output=[q.jet_p4_2_jesAbsolute_eraDown],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesAbsolute_eraDown = Producer(
    name="jet1_pt_jesAbsolute_eraDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesAbsolute_eraDown,
    ],
    output=[q.jet1_pt_jesAbsolute_eraDown],
    scopes=["vbfhmm"],
)
jet1_mass_jesAbsolute_eraDown = Producer(
    name="jet1_mass_jesAbsolute_eraDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesAbsolute_eraDown,
    ],
    output=[q.jet1_mass_jesAbsolute_eraDown],
    scopes=["vbfhmm"],
)

jet2_pt_jesAbsolute_eraDown = Producer(
    name="jet2_pt_jesAbsolute_eraDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesAbsolute_eraDown,
    ],
    output=[q.jet2_pt_jesAbsolute_eraDown],
    scopes=["vbfhmm"],
)
jet2_mass_jesAbsolute_eraDown = Producer(
    name="jet2_mass_jesAbsolute_eraDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesAbsolute_eraDown,
    ],
    output=[q.jet2_mass_jesAbsolute_eraDown],
    scopes=["vbfhmm"],
)
#####end of jes Absolute era down#####