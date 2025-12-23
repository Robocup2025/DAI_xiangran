import random
import string
from pathlib import Path


def create_img_files():
    """在当前目录创建img目录，生成100个不同名的.png文件"""
    # 创建img目录（不存在则创建）
    img_dir = Path("img")
    img_dir.mkdir(exist_ok=True)

    # 生成100个不重复的4位文件名（字母+数字）
    file_names = set()
    while len(file_names) < 100:
        # 生成4位随机字符（如X4G5）
        name = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
        file_names.add(f"{name}.png")

    # 创建文件（空文件）
    for fname in file_names:
        file_path = img_dir / fname
        file_path.touch()  # 创建空文件

    print(f"✅ 已在 {img_dir} 中创建100个不同名的.png文件")


# 调用
create_img_files()