from pathlib import Path


def modify_test_file():
    """在test.txt的开头和结尾添加字符串'python'"""
    test_path = Path("test.txt")
    if not test_path.exists():
        print("❌ test.txt不存在，请先运行文件复制题")
        return

    # 读取原内容
    with open(test_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 修改内容（开头+python，结尾+python）
    modified_content = "python" + content + "python"

    # 写回文件
    with open(test_path, "w", encoding="utf-8") as f:
        f.write(modified_content)

    print(f"✅ 已在 {test_path} 开头和结尾添加'python'")


# 调用
modify_test_file()