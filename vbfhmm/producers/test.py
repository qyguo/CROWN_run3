JetPtCorrection_2022_jesAbsolute_era_eraDown = Producer(
    name="JetPtCorrection_2022_jesAbsolute_era_eraDown",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo})",
    call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, True, {{\"Absolute_era_era\"}}, -1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesAbsolute_era_eraDown],
    scopes=["global", "vbfhmm"],
)
JetPtCorrection_2022_jesAbsolute_era_eraDown_GenMatch = Producer(
    name="JetPtCorrection_2022_jesAbsolute_era_eraDown_GenMatch",
    #call="physicsobject::jet::JetPtCorrection_2022({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, \"up\", {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo}, {jet_veto_map}, {jet_veto_tag})",
    call="physicsobject::jet::JetPtCorrection_2022_GenMatch({df}, {output}, {input}, True, {{\"Absolute_era_era\"}}, -1, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_era_algo}, {jet_veto_map}, {jet_veto_tag})",
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
    output=[q.Jet_pt_corrected_jesAbsolute_era_eraDown],
    scopes=["global", "vbfhmm"],
)
#
JetMassCorrection_jesAbsolute_era_eraDown = Producer(
    name="JetMassCorrection_jesAbsolute_era_eraDown",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected_jesAbsolute_era_eraDown,
    ],
    output=[q.Jet_mass_corrected_jesAbsolute_era_eraDown],
    scopes=["global", "vbfhmm"],
)
JetEnergyCorrection_2022_jesAbsolute_era_eraDown = ProducerGroup(
    name="JetEnergyCorrection_2022_jesAbsolute_era_eraDown",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesAbsolute_era_eraDown, JetMassCorrection_jesAbsolute_era_eraDown],
)
JetEnergyCorrection_2022_jesAbsolute_era_eraDown_GenMatch = ProducerGroup(
    name="JetEnergyCorrection_2022_jesAbsolute_era_eraDown_GenMatch",
    call=None,
    input=None,
    output=None,
    scopes=["global", "vbfhmm"],
    subproducers=[JetPtCorrection_2022_jesAbsolute_era_eraDown_GenMatch, JetMassCorrection_jesAbsolute_era_eraDown],
)
### selecting jets
LVJet1_jesAbsolute_era_eraDown = Producer(
    name="LVJet1_jesAbsolute_era_eraDown",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesAbsolute_era_eraDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesAbsolute_era_eraDown,
    ],
    output=[q.jet_p4_1_jesAbsolute_era_eraDown],
    scopes=["global","vbfhmm"],
)
LVJet2_jesAbsolute_era_eraDown = Producer(
    name="LVJet2_jesAbsolute_era_eraDown",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_jet_collection,
        q.Jet_pt_corrected_jesAbsolute_era_eraDown,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_jesAbsolute_era_eraDown,
    ],
    output=[q.jet_p4_2_jesAbsolute_era_eraDown],
    scopes=["global","vbfhmm"],
)
### jet kinematics
jet1_pt_jesAbsolute_era_eraDown = Producer(
    name="jet1_pt_jesAbsolute_era_eraDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesAbsolute_era_eraDown,
    ],
    output=[q.jet1_pt_jesAbsolute_era_eraDown],
    scopes=["vbfhmm"],
)
jet1_mass_jesAbsolute_era_eraDown = Producer(
    name="jet1_mass_jesAbsolute_era_eraDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_1_jesAbsolute_era_eraDown,
    ],
    output=[q.jet1_mass_jesAbsolute_era_eraDown],
    scopes=["vbfhmm"],
)

jet2_pt_jesAbsolute_era_eraDown = Producer(
    name="jet2_pt_jesAbsolute_era_eraDown",
    call='quantities::pt({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesAbsolute_era_eraDown,
    ],
    output=[q.jet2_pt_jesAbsolute_era_eraDown],
    scopes=["vbfhmm"],
)
jet2_mass_jesAbsolute_era_eraDown = Producer(
    name="jet2_mass_jesAbsolute_era_eraDown",
    call='quantities::mass({df}, {output}, {input})',
    input=[
      q.jet_p4_2_jesAbsolute_era_eraDown,
    ],
    output=[q.jet2_mass_jesAbsolute_era_eraDown],
    scopes=["vbfhmm"],
)
Jet_pt_corrected_jesAbsolute_era_eraDown = Quantity("Jet_pt_corrected_jesAbsolute_era_eraDown")
Jet_mass_corrected_jesAbsolute_era_eraDown = Quantity("Jet_mass_corrected_jesAbsolute_era_eraDown")
jet_p4_1_jesAbsolute_era_eraDown = Quantity("jet_p4_1_jesAbsolute_era_eraDown")
jet_p4_2_jesAbsolute_era_eraDown = Quantity("jet_p4_2_jesAbsolute_era_eraDown")

jet1_pt_jesAbsolute_era_eraDown = Quantity("jet1_pt_jesAbsolute_era_eraDown")
jet1_mass_jesAbsolute_era_eraDown = Quantity("jet1_mass_jesAbsolute_era_eraDown")
jet1_eta_jesAbsolute_era_eraDown = Quantity("jet1_eta_jesAbsolute_era_eraDown")
jet1_phi_jesAbsolute_era_eraDown = Quantity("jet1_phi_jesAbsolute_era_eraDown")
jet2_pt_jesAbsolute_era_eraDown = Quantity("jet2_pt_jesAbsolute_era_eraDown")
jet2_mass_jesAbsolute_era_eraDown = Quantity("jet2_mass_jesAbsolute_era_eraDown")
jet2_eta_jesAbsolute_era_eraDown = Quantity("jet2_eta_jesAbsolute_era_eraDown")
jet2_phi_jesAbsolute_era_eraDown = Quantity("jet2_phi_jesAbsolute_era_eraDown")

                jet_jer.LVJet1_jesAbsolute_eraUp,
                jet_jer.LVJet2_jesAbsolute_eraUp,
                jet_jer.jet1_pt_jesAbsolute_eraUp,
                jet_jer.jet1_mass_jesAbsolute_eraUp,
                jet_jer.jet2_pt_jesAbsolute_eraUp,
                jet_jer.jet2_mass_jesAbsolute_eraUp,

                jet_jer.LVJet1_jesAbsolute_eraDown,
                jet_jer.LVJet2_jesAbsolute_eraDown,
                jet_jer.jet1_pt_jesAbsolute_eraDown,
                jet_jer.jet1_mass_jesAbsolute_eraDown,
                jet_jer.jet2_pt_jesAbsolute_eraDown,
                jet_jer.jet2_mass_jesAbsolute_eraDown,

                q.jet1_pt_jesAbsolute_eraUp,
                q.jet1_mass_jesAbsolute_eraUp,
                q.jet2_pt_jesAbsolute_eraUp,
                q.jet2_mass_jesAbsolute_eraUp,

                q.jet1_pt_jesAbsolute_eraDown,
                q.jet1_mass_jesAbsolute_eraDown,
                q.jet2_pt_jesAbsolute_eraDown,
                q.jet2_mass_jesAbsolute_eraDown,

                jet_jer.JetEnergyCorrection_2022_jesAbsolute_eraUp,
                jet_jer.JetEnergyCorrection_2022_jesAbsolute_eraDown,
