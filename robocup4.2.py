import random
import string
from pathlib import Path


def create_and_copy_file():
    """生成test.txt（用户指定行数的ASCII字符），并复制为copy_test.txt"""
    # 1. 用户输入行数
    while True:
        try:
            line_count = int(input("请输入test.txt的行数："))
            if line_count <= 0:
                print("❌ 请输入正整数")
                continue
            break
        except ValueError:
            print("❌ 输入无效，请输入整数")

    # 2. 生成ASCII非控制字符（32~126，即空格到~）
    def get_random_ascii():
        return chr(random.randint(32, 126))  # 非控制字符范围

    # 3. 写入test.txt
    test_path = Path("test.txt")
    with open(test_path, "w", encoding="utf-8") as f:
        for _ in range(line_count):
            # 每行生成随机长度（10~20）的ASCII字符
            line = "".join([get_random_ascii() for _ in range(random.randint(10, 20))])
            f.write(line + "\n")

    # 4. 复制为copy_test.txt
    copy_path = Path("copy_test.txt")
    with open(test_path, "r", encoding="utf-8") as src, open(copy_path, "w", encoding="utf-8") as dst:
        dst.write(src.read())

    print(f"✅ 已生成 {test_path} 并复制为 {copy_path}")


# 调用
create_and_copy_file()