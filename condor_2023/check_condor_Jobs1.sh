#for file in Jobs/DoubleMuon_UL18A_9163602_*.out; do     echo -e "$file -> $(sed -n 's/LeptonChargeSum/&/p' "$file")"; done
DataName=DYJetsToLL_M-50-madgraphMLM
#JobID_condor=*
JobID_condor=5851398
Jobs_Name=Jobs/${DataName}*${JobID_condor}*.out
resubOr=resub
for file in ${Jobs_Name};
do
    check=$(sed -n 's/Overall runtime/&/p' "$file")
    if [[ $check ]]; then
        printOut="finished"
        echo "${file} finished"
        echo "------><-------"
    else
        echo "$file -> " 
        check_1=$(sed -n 's/\[critical\]/&/p' "$file")
        echo "    [critical => " "${check_1}"
        output_File=$(sed -n 's|^/eos/user/j/jiahua/vbfhmm|&|p' "$file")
        input_File=$(sed -n 's/root:\/\/cms-xrd-global.cern.ch/\/&/p' "$file")
        output_File=$(echo "$output_File" | sed 's/.root/_resub.root/')
        #input_File=$(echo "$input_File" | awk -F  'File /' '{print $2}')
        #input_File=$(echo "$input_File" | sed 's/\.root.*/.root /')

        if [[ $check_1 ]]; then
            input_File=$(echo "$input_File" | awk -F  'File /' '{print $2}')
        else
            input_File=$(echo "$input_File" | awk -F  'NanoAOD input_file 1: /' '{print $2}')
        fi
        input_File=$(echo "$input_File" | sed 's/\.root.*/.root /')
        #

        echo "    running localy"
        echo -e "     ./vbfhmm_config_dyjets_2018 $output_File ${input_File}"
        echo -e "./vbfhmm_config_dyjets_2018 $output_File ${input_File}" >> ${DataName}_rerunning_locally.sh
        # Check if the path exists
        Job_sub_Name=Job_${DataName}_${resubOr}.sub
        if [ -e "$Job_sub_Name" ]; then
            echo "${Job_sub_Name} already exists."
        else
            echo "${output_Dir} creating"
            cp Job_template.sub $Job_sub_Name
            sed -i "9,11s/hello_/${DataName}_${resubOr}_/" $Job_sub_Name
            sed -i "7s/$/\/${DataName}/" $Job_sub_Name
        fi
        ##
        echo -e "input_name = ${input_File}\nQueue" >>${Job_sub_Name}
        echo "-------------------><--------------------"
    fi
done
