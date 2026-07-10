
<img src="docs/logos/crown_logo_outline.svg"><br>

<p align="left">
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://app.codacy.com/gh/KIT-CMS/CROWN/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade"><img src="https://app.codacy.com/project/badge/Grade/681a25523b544d788155696eb829e38b"/></a>
<a href="https://crown.readthedocs.io/en/latest/?badge=latest"><img alt="Documentation Status" src="https://readthedocs.org/projects/crown/badge/?version=latest"></a>
<a href="https://doi.org/10.5281/zenodo.8325327"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.8325327.svg" alt="DOI"></a>
</p>

---

[![Repobeats analytics image](https://repobeats.axiom.co/api/embed/bac34668655cc1118c86a0b1831cf095e159606f.svg "Repobeats analytics image")](https://github.com/KIT-CMS/CROWN/pulse)

---

Crown
=======

The C++-based ROot Workflow for N-tuples (CROWN)  framework is a fast way, of converting CMS NanoAOD samples into analysis N-tuples.


Getting Started
----------------

Installing the framework is easy (not much more than a `git clone`), check the [Installation Guide](https://crown.readthedocs.io/en/latest/introduction.html#getting-started)

A small introduction on how to run the framework can be found in this [Running the framework Guide](https://crown.readthedocs.io/en/latest/introduction.html#running-the-framework)


Documentation
--------------

The full documentation can be found at https://crown.readthedocs.io/en/latest/.

How to Run
--------------
```
source init.sh fsim
cd build
cmake .. -DANALYSIS=fsim -DCONFIG=vbfhmm_config_run3_Inc_v4_JetVeto_jetID_PU_24_KIT_fsim -DSAMPLES=fsim -DERAS=2024 -DSCOPES=fsim
make install -j 16
cd bin
voms-proxy-init -voms cms --valid 200:00
xrdcp root://xrootd-cms.infn.it//store/group/rucio/flashsim/DYto2Mu-2Jets_Bin-MLL-105to160_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/flashsim_DY2Mu_2Jets_MLL-105to160-April2026_IreneFakes_Oversampling9/260421_142939/0000/tree_1.root ./
./vbfhmm_config_run3_Inc_v4_JetVeto_jetID_PU_24_KIT_fsim_fsim_2024 flashsim_test.root /eos/user/j/jiehan/tree_1.root
```