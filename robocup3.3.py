import random
from pathlib import Path

def create_random_num_file():
    """创建100000行、每行1~100随机整数的data.txt"""
    file_path = Path("data.txt")
    # 生成所有行（批量生成更高效）
    lines = [str(random.randint(1, 100)) + "\n" for _ in range(100000)]
    # 写入文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"✅ 已创建 {file_path}，共100000行随机数")

# 调用
create_random_num_file()