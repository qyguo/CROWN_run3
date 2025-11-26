import os

def split_txt_file(filepath, max_lines=110, split_threshold=200):
    # 检查文件是否存在
    if not os.path.isfile(filepath):
        print(f"Error: File '{filepath}' not found.")
        return

    # 读取所有行
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # 如果不需要分割就返回
    if len(lines) <= split_threshold:
        print(f"No need to split. File has {len(lines)} lines.")
        return

    # 构造输出文件前缀
    base, ext = os.path.splitext(filepath)
    total_parts = (len(lines) + max_lines - 1) // max_lines

    for i in range(total_parts):
        start = i * max_lines
        end = min((i + 1) * max_lines, len(lines))
        new_filename = f"{base}_{i+1}{ext}"
        with open(new_filename, 'w') as f_out:
            f_out.writelines(lines[start:end])
        print(f"Wrote {end - start} lines to {new_filename}")

# 使用示例
split_txt_file("Muon_Run2022F-19Dec2023-v1.txt")

