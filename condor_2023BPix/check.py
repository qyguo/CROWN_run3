import os

def filter_and_format_dy_file(folder_path, dy_file, output_file):
    """
    根据 .root 文件的前缀过滤 dy.txt 并按照指定格式输出未被删除的行 
    格式：./vbfhmm <字符串> <行内容>
    """
    # 获取文件夹中所有以 _vbfhmm.root 结尾的文件
    root_files = [f for f in os.listdir(folder_path) if f.endswith("_vbfhmm.root")]
    
    # 提取文件名前缀（去掉 _vbfhmm.root 部分）
    root_prefixes = {f.replace("_vbfhmm.root", "") for f in root_files}
    
    # 读取 dy.txt 文件的所有行
    with open(dy_file, 'r') as f:
        dy_lines = f.readlines()
    
    # 创建输出行列表
    output_lines = []

    for line in dy_lines:
        stripped_line = line.strip()  # 去掉首尾空白字符
        
        # 如果是 "Queue"，直接跳过
        if stripped_line == "Queue":
            continue

        # 检查行是否包含任意前缀
        if any(prefix in line for prefix in root_prefixes):
            continue  # 如果包含前缀，跳过这行（删除）
        
        processed_line = stripped_line.replace("input_name = ", "")

        # 提取行中最后一个斜杠后到 .root 之间的字符串
        last_slash_idx = processed_line.rfind('/')  # 找到最后一个斜杠的位置
        dot_root_idx = processed_line.rfind('.root')  # 找到 ".root" 的位置

        if last_slash_idx != -1 and dot_root_idx != -1 and last_slash_idx < dot_root_idx:
            extracted_string = processed_line[last_slash_idx + 1:dot_root_idx]
        else:
            continue

        # 格式化输出行
        formatted_line = f"./vbfhmm_config_run3_Inc_v4_JetVeto_diboson_2022 {folder_path}/{extracted_string}.root root://cms-xrd-global.cern.ch/{processed_line} > {log_path}/{extracted_string}.log 2>&1 \n"
        #formatted_line = f"input_name = {processed_line}\n"
        #formatted_line = f"{processed_line} "
        #line = f"Queue\n"
        output_lines.append(formatted_line)
        #output_lines.append(line)
    
    # 将结果写入输出文件
    with open(output_file, 'w') as f:
        f.writelines(output_lines)
    
    print(f"处理完成！结果已保存到 {output_file}")




# 使用示例

dy_file = '/afs/cern.ch/user/j/jiahua/CROWN_run3/condor/Sample_list/ZZto2L2Nu_powheg_22_ext1-v2.txt'  # DY.txt 文件路径
folder_path = '/afs/cern.ch/user/j/jiahua/work/MC_2022_inc/ZZto2L2Nu_powheg_22_ext1-v2'  # 包含 .root 文件的文件夹路径
log_path = '/afs/cern.ch/user/j/jiahua/work/MC_2022_inc/log/log_ZZto2L2Nu_powheg_22_ext1-v2'  # 输出未找到条目的文件
output_file = 'top.sub'

filter_and_format_dy_file(folder_path, dy_file, output_file)
