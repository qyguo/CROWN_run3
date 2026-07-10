#!/bin/bash
# Wrapper script for processing fullsim files on Condor

# Input parameters
INPUT_FILE=$1
OUTPUT_NAME=$2

# Setup environment
cd /afs/cern.ch/user/j/jiehan/private/CROWN_run3
source /afs/cern.ch/user/j/jiehan/private/CROWN_run3/init.sh vbfhmm

# Create output directory if needed
mkdir -p /eos/user/j/jiehan/HMuMuShare/fullsimNtuple/

# Extract xrootd URL
INPUT_URL="root://cms-xrd-global.cern.ch//$INPUT_FILE"
OUTPUT_BASE="/eos/user/j/jiehan/HMuMuShare/fullsimNtuple/${OUTPUT_NAME}.root"
EXPECTED_OUTPUT="/eos/user/j/jiehan/HMuMuShare/fullsimNtuple/${OUTPUT_NAME}_vbfhmm.root"

# Run analysis - output name matches input file naming convention
/afs/cern.ch/user/j/jiehan/private/CROWN_run3/build/bin/vbfhmm_config_run3_Inc_v4_JetVeto_jetID_PU_24_KIT_dyjets_2024 "${OUTPUT_BASE}" "${INPUT_URL}"

# Check if the scoped CROWN output file was created
if [ -f "${EXPECTED_OUTPUT}" ]; then
    echo "Successfully processed ${EXPECTED_OUTPUT}"
else
    echo "ERROR: Output file ${EXPECTED_OUTPUT} was not created"
    exit 1
fi
