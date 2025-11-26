    cp Job_template.sub Job_EWK_LLJJ_MLL_105-160_SM_5f_LO_TuneCH3_13TeV-madgraph-herwig7_corrected_18.sub
    PDs=()
    if [ -e "Sample_list/EWK_LLJJ_MLL_105-160_SM_5f_LO_TuneCH3_13TeV-madgraph-herwig7_corrected.txt" ]; then
        # Read the file line by line
        while IFS= read -r PD; do
            PDs+=("$PD")
        done < "Sample_list/EWK_LLJJ_MLL_105-160_SM_5f_LO_TuneCH3_13TeV-madgraph-herwig7_corrected.txt"
    fi
    for index in "${PDs[@]}";do
        echo -e "input_name = root://xrootd-cms.infn.it/${index}\nQueue" >>Job_EWK_LLJJ_MLL_105-160_SM_5f_LO_TuneCH3_13TeV-madgraph-herwig7_corrected.sub
    done
    echo Job_EWK_LLJJ_MLL_105-160_SM_5f_LO_TuneCH3_13TeV-madgraph-herwig7_corrected.sub
