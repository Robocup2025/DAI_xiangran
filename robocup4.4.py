from pathlib import Path


def compare_files():
    """对比test.txt和copy_test.txt，输出不同的行"""
    test_path = Path("test.txt")
    copy_path = Path("copy_test.txt")
    if not (test_path.exists() and copy_path.exists()):
        print("❌ test.txt或copy_test.txt不存在，请先运行文件复制题")
        return

    # 逐行读取并对比
    with open(test_path, "r", encoding="utf-8") as t, open(copy_path, "r", encoding="utf-8") as c:
        line_num = 1
        has_diff = False
        while True:
            t_line = t.readline()
            c_line = c.readline()

            # 都读完则退出
            if not t_line and not c_line:
                break

            # 行内容不同
            if t_line != c_line:
                has_diff = True
                print(f"❌ 第{line_num}行不同：")
                print(f"test.txt: {t_line.strip() or '[空行]'}")
                print(f"copy_test.txt: {c_line.strip() or '[空行]'}\n")

            line_num += 1

    if not has_diff:
        print("✅ 两个文件内容完全相同")


# 调用
compare_files()