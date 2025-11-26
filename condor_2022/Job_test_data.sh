#!/bin/bash
echo "Starting job on `data`\n" #Data/time of start of job
echo "Running on: `uname -a`\n" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`\n" #Operating System on that node

source /afs/cern.ch/cms/cmsset_default.sh

cd /afs/cern.ch/user/j/jiahua/CROWN_run3

source init.sh vbfhmm

cd build_2022/bin
export X509_USER_PROXY=$1
voms-proxy-info -all
voms-proxy-info -all -file $1
out_name=$(echo "$3" | awk -F'/' '{print $NF}')
echo ${2}/${out_name}
./vbfhmm_config_run3_vbf_test_data_2022 ${2}/${out_name} $3
