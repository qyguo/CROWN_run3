#!/usr/bin/env python3
"""
Generate Condor submit files for processing fullsim dataset files
"""

import subprocess
import os
import re
import argparse
import sys

# Output directory for ntuples
OUTPUT_DIR = "/eos/user/j/jiehan/HMuMuShare/flashsimNtuple/"
# OUTPUT_DIR = "/eos/user/j/jiehan/HMuMuShare/fullsimNtuple/"

# Command details
ANALYSIS_BIN = "/afs/cern.ch/user/j/jiehan/private/CROWN_run3/build/bin/vbfhmm_config_run3_Inc_v4_JetVeto_jetID_PU_24_KIT_fsim_fsim_2024"
SUBMIT_PATH = "/afs/cern.ch/user/j/jiehan/private/CROWN_run3/flashsim_process.sub"
WRAPPER_PATH = "/afs/cern.ch/user/j/jiehan/private/CROWN_run3/process_flashsim_file.sh"
ANALYSIS_ENV = "fsim"
OUTPUT_SCOPE = "fsim"

# ANALYSIS_BIN = "/afs/cern.ch/user/j/jiehan/private/CROWN_run3/build/bin/vbfhmm_config_run3_Inc_v4_JetVeto_jetID_PU_24_KIT_dyjets_2024"
# SUBMIT_PATH = "/afs/cern.ch/user/j/jiehan/private/CROWN_run3/fullsim_process.sub"
# WRAPPER_PATH = "/afs/cern.ch/user/j/jiehan/private/CROWN_run3/process_fullsim_file.sh"
# ANALYSIS_ENV = "vbfhmm"
# OUTPUT_SCOPE = "vbfhmm"

INIT_SCRIPT = "/afs/cern.ch/user/j/jiehan/private/CROWN_run3/init.sh"
WORK_DIR = "/afs/cern.ch/user/j/jiehan/private/CROWN_run3"
PROXY_PATH = "/afs/cern.ch/user/j/jiehan/x509up_u152815"


def run_interactive_command(cmd, env=None):
    """Run a command interactively so passphrase prompts work in terminal."""
    return subprocess.run(cmd, env=env, check=False).returncode


def init_and_verify_proxy(proxy_path):
    """Initialize and validate VOMS proxy, then export it for child processes."""
    print(f"Initializing proxy at: {proxy_path}")

    # Ensure parent directory exists for proxy file output.
    proxy_dir = os.path.dirname(proxy_path)
    if proxy_dir and not os.path.isdir(proxy_dir):
        os.makedirs(proxy_dir, exist_ok=True)

    init_cmd = [
        "voms-proxy-init",
        "--rfc",
        "--voms",
        "cms",
        "-valid",
        "192:00",
        "-out",
        proxy_path,
    ]
    rc = run_interactive_command(init_cmd)
    if rc != 0:
        print("ERROR: voms-proxy-init failed")
        return False

    # Export for all subprocesses started by this Python process.
    os.environ["X509_USER_PROXY"] = proxy_path
    print(f"Exported X509_USER_PROXY={proxy_path}")

    verify_cmd = ["voms-proxy-info", "-all", "-file", proxy_path]
    rc = run_interactive_command(verify_cmd, env=os.environ.copy())
    if rc != 0:
        print("ERROR: voms-proxy-info verification failed")
        return False

    return True

# Get file list from DAS
def get_file_list():
    """Query DAS for file list"""
    # query = 'file dataset=/DYto2Mu-2Jets_Bin-MLL-105to160_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/rucio-flashsim_DY2Mu_2Jets_MLL-105to160-RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-limit-TrkGJ_eta-to-tracker_Oversampling5-66034083b387d860d393385d18a4f59d/USER instance=prod/phys03'
    query = 'file dataset=/DYto2Mu-2Jets_Bin-MLL-105to160_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/rucio-flashsim_DY2Mu_2Jets_MLL-105to160-April2026_IreneFakes_Oversampling9-89578c67bc58e175e14cb8efc9d9e047/USER instance=prod/phys03'
    # query = 'file dataset=/DYto2Mu-2Jets_Bin-MLL-105to160_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/RunIII2024Summer24NanoAODv15-150X_mcRun3_2024_realistic_v2-v2/NANOAODSIM'
    
    cmd = ['dasgoclient', '--query=' + query]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        files = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        return files
    except Exception as e:
        print(f"Error getting file list: {e}")
        return []

# Generate wrapper script
def generate_wrapper_script():
    """Generate the wrapper script for job execution"""
    wrapper_content = '''#!/bin/bash
# Wrapper script for processing fullsim files on Condor

# Input parameters
INPUT_FILE=$1
OUTPUT_NAME=$2

# Setup environment
cd {work_dir}
source {init_script} {analysis_env}

# Create output directory if needed
mkdir -p {output_dir}

# Extract xrootd URL
INPUT_URL="root://cms-xrd-global.cern.ch//$INPUT_FILE"
OUTPUT_BASE="{output_dir}${{OUTPUT_NAME}}.root"
EXPECTED_OUTPUT="{output_dir}${{OUTPUT_NAME}}_{output_scope}.root"

# Run analysis - output name matches input file naming convention
{analysis_bin} "${{OUTPUT_BASE}}" "${{INPUT_URL}}"

# Check if the scoped CROWN output file was created
if [ -f "${{EXPECTED_OUTPUT}}" ]; then
    echo "Successfully processed ${{EXPECTED_OUTPUT}}"
else
    echo "ERROR: Output file ${{EXPECTED_OUTPUT}} was not created"
    exit 1
fi
'''.format(
        work_dir=WORK_DIR,
        init_script=INIT_SCRIPT,
        analysis_bin=ANALYSIS_BIN,
        analysis_env=ANALYSIS_ENV,
        output_dir=OUTPUT_DIR,
        output_scope=OUTPUT_SCOPE,
    )
    
    wrapper_path = WRAPPER_PATH
    with open(wrapper_path, 'w') as f:
        f.write(wrapper_content)
    
    os.chmod(wrapper_path, 0o755)
    print(f"Created wrapper script: {wrapper_path}")
    return wrapper_path

# Extract file name from path
def get_file_name(file_path):
    """Extract output name from a DAS file path."""
    base_name = os.path.basename(file_path)
    match = re.match(r'(tree_\d+)\.root$', base_name)
    if match:
        return match.group(1)
    if base_name.endswith(".root"):
        return os.path.splitext(base_name)[0]
    return None

# Generate Condor submit file
def generate_submit_file(files, wrapper_path):
    """Generate Condor submit file"""
    
    submit_content = '''# Condor submit file for fullsim ntuple processing

universe = vanilla
executable = {wrapper}
log = /afs/cern.ch/user/j/jiehan/private/CROWN_run3/logs/condor_$(Cluster).log
output = /afs/cern.ch/user/j/jiehan/private/CROWN_run3/logs/job_$(ClusterID)_$(ProcID).out
error = /afs/cern.ch/user/j/jiehan/private/CROWN_run3/logs/job_$(ClusterID)_$(ProcID).err

# X509 proxy for remote xrootd file access
x509userproxy = {proxy_path}
environment = "X509_USER_PROXY={proxy_path}"

# Job requirements
+JobFlavour = "workday"
request_cpus = 1

# Transfer files
should_transfer_files = NO

'''.format(wrapper=wrapper_path, proxy_path=PROXY_PATH)
    
    # Add job queue entries
    queued_jobs = 0
    skipped_files = []
    for i, file_path in enumerate(files, 1):
        file_name = get_file_name(file_path)
        if file_name:
            # Arguments: input_file output_name
            submit_content += f'arguments = "{file_path} {file_name}"\nqueue\n\n'
            queued_jobs += 1
        else:
            skipped_files.append(file_path)
    
    if queued_jobs == 0:
        raise RuntimeError("No jobs queued. Check the DAS file naming pattern.")
    
    # submit_path = "/afs/cern.ch/user/j/jiehan/private/CROWN_run3/flashsim_process.sub"
    submit_path = SUBMIT_PATH
    with open(submit_path, 'w') as f:
        f.write(submit_content)
    
    print(f"Created Condor submit file: {submit_path}")
    print(f"Input files: {len(files)}")
    print(f"Queued jobs: {queued_jobs}")
    if skipped_files:
        print(f"Skipped files without .root output names: {len(skipped_files)}")
    return submit_path

# Main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Condor files and optionally initialize X509 proxy"
    )
    parser.add_argument(
        "--init-proxy",
        action="store_true",
        help="Run voms-proxy-init and voms-proxy-info before generating files",
    )
    parser.add_argument(
        "--proxy-path",
        default=PROXY_PATH,
        help="Proxy file path used for init/verify and Condor submit environment",
    )
    args = parser.parse_args()

    # Keep global path in sync with CLI input for submit file generation.
    PROXY_PATH = args.proxy_path

    if args.init_proxy:
        ok = init_and_verify_proxy(PROXY_PATH)
        if not ok:
            sys.exit(1)

    # If user already has a proxy file, still export for current process.
    os.environ["X509_USER_PROXY"] = PROXY_PATH

    # Create logs directory
    log_dir = "/afs/cern.ch/user/j/jiehan/private/CROWN_run3/logs"
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("Getting file list from DAS...")
    files = get_file_list()
    
    if not files:
        print("ERROR: No files found!")
        exit(1)
    
    print(f"Found {len(files)} files")
    
    print("Generating wrapper script...")
    wrapper = generate_wrapper_script()
    
    print("Generating Condor submit file...")
    try:
        submit = generate_submit_file(files, wrapper)
    except RuntimeError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    
    print("\nReady to submit!")
    print(f"Run: condor_submit {submit}")
