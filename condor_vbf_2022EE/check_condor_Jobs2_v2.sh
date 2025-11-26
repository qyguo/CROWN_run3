#for file in Jobs/DoubleMuon_UL18A_9163602_*.out; do     echo -e "$file -> $(sed -n 's/LeptonChargeSum/&/p' "$file")"; done
output_Path=/eos/user/j/jiahua/MC_2022EE_inc/MC_2022EE_vbf
build_name=build_vbf
DataName=*
JobID_condor=
addition=
resubOr=resub1
DataName=*
config=_run3_vbf_uncertainty_2022EE
JobID_condor=*
JobID_condor=130877
#Jobs_Name=Jobs${addition}/${DataName}*${JobID_condor}*.out
Jobs_Name=Jobs/${DataName}*${JobID_condor}*.out
DataOrMC=false
for file in ${Jobs_Name};
do
    DataName=$(echo "$file" | sed 's|.*/||')
    DataName="${DataName%_*_*.out}"
    DataName=$(echo "$DataName" | sed 's|_resub.||')
    echo $DataName
    Job_sub_Name=Job_${DataName}_${resubOr}${addition}.sub

    check=$(sed -n 's/Overall runtime/&/p' "$file")
    check2=$(sed -n 's/Finished Evaluation/&/p' "$file")
    checkmain=$(sed -n 's/main/&/p' "$file")
    if [[ $check && $check2 ]]; then
        printOut="finished"
        echo "${file} finished"
        echo "------><-------"
    ##elif [[ ! $checkmain ]]; then
    else
        echo "$file -> " >> fail.sh
        check_1=$(sed -n 's/\[critical\]/&/p' "$file")
        echo "    [critical => " "${check_1}"
        output_File=$(sed -n 's|^${output_Path}|&|p' "$file")
        #output_File=$(sed -n 's|^/eos/user/q/qguo/vbfhmm/UL18|&|p' "$file")
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

        #######888
        if [[ $DataName == WWW_* || $DataName == WWZ_* || $DataName == WZZ_* ]]; then
            Job_type=triboson
        elif [[ $DataName == DYJets* ]]; then
            Job_type=dyjets
        elif [[ $DataName == GluGluToContin* || $DataName == ZZTo4L* || $DataName == ZZTo2L2Nu* || $DataName == WZTo3LNu* || $DataName == WWTo2L2Nu* || $DataName == WZTo2L2Q* || $DataName == ZZTo2L2Q* ]]; then
            Job_type=diboson
        elif [[ $DataName == EWK_LLJJ* ]]; then
           Job_type=zjjew
        elif [[ $DataName == GluGluHToMuMu* ]]; then
            Job_type=gghmm
        elif [[ $DataName == VBFHToMuMu* ]]; then
            Job_type=vbfhmm
        elif [[ $DataName == TTTo2L2Nu* || $DataName == TTToSemiLeptonic* || $DataName == *top* || $DataName == ST_s-channel_4f_leptonDecays* ]]; then
            Job_type=top
        fi
        echo "What!!!", $Job_type
        #######888
        uuid=$(basename "$input_File" | sed 's/\.root$//')
        output_File="${output_Path}/${DataName}/${uuid}"
        echo "    running localy"
        if [[ ${DataOrMC} == true ]]; then
            run_script_tmp=./vbfhmm_config_run3_vbf_uncertainty_data_2022EE
        else
            run_script_tmp=./vbfhmm_config_run3_vbf_uncertainty_top_2022EE
        fi
        echo -e "${run_script_tmp} ${output_File} ${input_File}"
        echo -e "${run_script_tmp} ${output_File} ${input_File}" >> ${DataName}_rerunning_locally${addition}.sh
        # Check if the path exists
        #Job_sub_Name=Job_${DataName}_${resubOr}${addition}.sub
        if [ -e "$Job_sub_Name" ]; then
            echo "${Job_sub_Name} already exists."
        else
            echo "${output_Dir} creating"
            if ${DataOrMC}; then
                cp Job_template_data.sub ${Job_sub_Name}
            else
                cp Job_template.sub ${Job_sub_Name}
            fi
            #cp Job_template.sub ${Job_sub_Name}

            if [[ $build_name != build ]]; then
                sed -i "s/\/build\//\/${build_name}\//g" ${Job_sub_Name}
            fi
            #sed -i "2,5s/Job_test_1/Job_test_${Job_type}/" ${Job_sub_Name}
            sed -i "4s/vbfhmm_config_dyjets/vbfhmm_config_${config}_${Job_type}/" ${Job_sub_Name}
            sed -i "8,10s/hello_/${DataName}_${resubOr}_/" ${Job_sub_Name}
            sed -i "8,10s/Jobs/Jobs${addition}/" ${Job_sub_Name}
            sed -i "6s|$|${output_Path}\/${DataName}|" ${Job_sub_Name}
        fi
        ##
        if [[ ${input_File} ]]; then
            echo -e "input_name = ${input_File}\nQueue" >>${Job_sub_Name}
        fi
        #echo "input_File", ${input_File}
        #echo $file
        if [[ (! $checkmain) && -z $input_File ]]; then
            echo "AHAHHAHAHAHAH!"
            file_err="${file%.out}.err"
            #check=$(sed -n 's/SYSTEM_PERIODIC_REMOVE/&/p' "$file_log");
            check_err=$(sed -n 's/No such file or directory/&/p' "$file_err");
            if [[ $check_err ]]; then
                #echo -e "$file -> $(sed -n 's/SYSTEM_PERIODIC_REMOVE/&/p' "$file_log")";
                echo -e "$file -> $(sed -n 's/No such file or directory/&/p' "$file_err")";
            fi
            output_path=$(grep "/eos/user/j/jiahua/MC_2022EE_inc/" ${file})
            echo $output_path
            root=$(echo "$output_path" | awk -F'/'  '{print $NF}' )
            echo $root
            Sam=Sample_list/${DataName}*.txt
            input=$(grep $root ${Sam})
            echo $input
            input_File="root://cms-xrd-global.cern.ch/"${input}
            echo -e "input_name = ${input_File}\nQueue" >>${Job_sub_Name}

        fi
        echo "condor_submit ${Job_sub_Name}"
        echo "condor_submit ${Job_sub_Name}" >>sub_${resubOr}${addition}.sh
    fi
    echo "-------------------><--------------------"
done
