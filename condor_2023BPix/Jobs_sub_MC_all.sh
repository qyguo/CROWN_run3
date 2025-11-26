DataOrMC=MC
lines=()
PDs=()
addition=
addition=
conf_name=vbfhmm_config_run3_Inc_v4_JetVeto_top_2023BPix
build_name=build
output_Path=/eos/user/j/jiahua/MC_2023BPix_inc/
file_path=/afs/cern.ch/user/j/jiahua/CROWN_run3/condor_2023BPix/Sample_list/ewk.txt
#file_path=/afs/cern.ch/user/j/jiahua/CROWN_run3/condor_2023BPix/Sample_list/mc_2023BPix_run3.txt
SamListPath=/afs/cern.ch/user/j/jiahua/CROWN_run3/condor_2023BPix/Sample_list
# Check if the file exists
if [ -e "$file_path" ]; then
    # Read the file line by line
    while IFS= read -r line; do
        #echo "$line"
        lines+=("$line")
    done < "$file_path"
else
    echo "File not found: $file_path"
    exit 0
fi

i=-1
for element in "${lines[@]}"; do
    ((i += 1))
    if [[ $element == "#"* ]]; then
        continue
    fi
    echo "----->><<-----"
    dataSet__=$(echo "$element" | awk -F'/'  '{print $2}')
    dataSet__=$(echo "$dataSet__" | sed 's/-pythia8//')
    dataSet__=$(echo "$dataSet__" | sed 's/_TuneCP5_13p6TeV//')
    dataSet__=$(echo "$dataSet__" | sed 's/_TuneCP5_withDipoleRecoil_13p6TeV//')
    Sam_version=$(echo "$element" | awk -F'/'  '{print $3}')
    Sam_version=$(echo "$Sam_version" | sed 's/Run3Summer//')
    #Sam_version=$(echo "$Sam_version" | sed 's/NanoAODv9-106X_mcRun2_asymptotic_v17-v1//')
    ###
    if [[ $DataOrMC == *Data* ]]; then
        if [[ $Sam_version == *HIPM_UL* ]]; then
            Sam_version=$(echo "$Sam_version" | sed 's/Run20//')
            Sam_version="UL"$(echo "$Sam_version" | sed 's/-.*//')
            Sam_version+="_APV"
        else
            Sam_version=$(echo "$Sam_version" | sed 's/Run20//')
            Sam_version="UL"$(echo "$Sam_version" | sed 's/-UL201.*//')
        fi
    elif [[ $DataOrMC == *MC* ]]; then
        if [[ $Sam_version == *preVFP* ]]; then
            Sam_version=$(echo "$Sam_version" | sed 's/Run3Summer//')
            Sam_version=$(echo "$Sam_version" | sed 's/NanoAOD.*//')
            Sam_version+="_preVFP"
        else
            Sam_version=$(echo "$Sam_version" | sed 's/Run3Summer//')
            Sam_version=$(echo "$Sam_version" | sed 's/NanoAOD.*//')
        fi
        #
    else
        echo "What do you want to run?"
        continue
    fi
    ####
    tmp=$(echo "$element" | awk -F'/'  '{print $3}')
    if [[ $tmp == *_ext* ]]; then
        tmp=$(echo "$tmp" | sed 's/.*ext/_ext/')
        Sam_version+=$tmp
    fi
    Sam=${SamListPath}/${dataSet__}_${Sam_version}${addition}.txt
    echo $Sam
    echo ${dataSet__}_${Sam_version}${addition}
    output_Dir=${output_Path}${dataSet__}_${Sam_version}${addition} 
    # Check if the path exists
    if [ -d "$output_Dir" ]; then
        echo "${output_Dir} already exists."
    else
        mkdir -p "${output_Dir}"
        echo "${output_Dir} created"
    fi
    Job_sub_Name=Job_${dataSet__}_${Sam_version}${addition}.sub
    cp Job_template.sub ${Job_sub_Name}
    ##

    ###

    sed -i "8,10s/hello_/${dataSet__}_${Sam_version}_/" ${Job_sub_Name}
    sed -i "8,10s/Jobs/Jobs${addition}/" ${Job_sub_Name}
    sed -i "6s|$|${output_Dir}|" ${Job_sub_Name}
    #sed -i "6s/$/\/${dataSet__}_${Sam_version}${addition}/" ${Job_sub_Name}
    #cp Job_template.sub Job_${dataSet__}_${Sam_version}.sub
    #sed -i "8,10s/hello_/${dataSet__}_${Sam_version}_/" Job_${dataSet__}_${Sam_version}.sub
    #sed -i "6s/$/\/${dataSet__}_${Sam_version}/" Job_${dataSet__}_${Sam_version}.sub
    #echo "Dir_Out_Name = ${dataSet__}_${Sam_version}" >>Job_${dataSet__}_${Sam_version}.sub
    /cvmfs/cms.cern.ch/common/dasgoclient --limit=0 --query "file dataset=${element} instance=prod/global" >& $Sam

    PDs=()
    if [ -e "$Sam" ]; then
        # Read the file line by line
        while IFS= read -r PD; do
            PDs+=("$PD")
        done < "$Sam"
    fi
    for index in "${PDs[@]}";do
        #echo -e "input_name = root://cms-xrd-global.cern.ch/${index}\nQueue" >>Job_${dataSet__}_${Sam_version}.sub
        echo -e "input_name = root://cms-xrd-global.cern.ch/${index}\nQueue" >>${Job_sub_Name}
    done
    echo "condor_submit ${Job_sub_Name}"
    echo "condor_submit ${Job_sub_Name}" >> UL18_slc7.log

done
