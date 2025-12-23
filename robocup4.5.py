import random
import string
from pathlib import Path


def batch_create_and_modify_files():
    """创建test目录，生成指定数量的文件，修改文件名和内容"""
    # 1. 创建test目录
    test_dir = Path("test")
    test_dir.mkdir(exist_ok=True)

    # 2. 用户输入文件数量
    while True:
        try:
            file_count = int(input("请输入要创建的文件数量："))
            if file_count <= 0:
                print("❌ 请输入正整数")
                continue
            break
        except ValueError:
            print("❌ 输入无效，请输入整数")

    # 3. 生成文件并写入随机内容
    file_paths = []
    for i in range(file_count):
        # 原文件名（如file_0.txt）
        file_path = test_dir / f"file_{i}.txt"
        file_paths.append(file_path)
        # 写入随机内容（5行，每行10个ASCII字符）
        with open(file_path, "w", encoding="utf-8") as f:
            for _ in range(5):
                line = "".join(random.choices(string.ascii_letters + string.digits, k=10))
                f.write(line + "\n")

    # 4. 修改文件名（加"-python"）和内容（每行加"-python"）
    for file in file_paths:
        # 重命名文件
        new_name = file.stem + "-python" + file.suffix
        new_file_path = file.with_name(new_name)
        file.rename(new_file_path)

        # 修改内容：每行末尾加"-python"
        with open(new_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        modified_lines = [line.strip() + "-python\n" for line in lines]
        with open(new_file_path, "w", encoding="utf-8") as f:
            f.writelines(modified_lines)

    print(f"✅ 已在 {test_dir} 中创建并修改{file_count}个文件")


# 调用
batch_create_and_modify_files()