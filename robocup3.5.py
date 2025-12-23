import random
from pathlib import Path


def rename_random_files():
    """将img目录中随机50个.png文件改名为.jpg"""
    img_dir = Path("img")
    # 获取img目录下所有.png文件
    png_files = list(img_dir.glob("*.png"))
    if len(png_files) < 50:
        print("❌ img目录中.png文件不足50个")
        return

    # 随机选50个文件
    selected_files = random.sample(png_files, 50)
    for file in selected_files:
        # 重命名：后缀改为.jpg
        new_path = file.with_suffix(".jpg")
        file.rename(new_path)

    print(f"✅ 已将img目录中50个文件的后缀改为.jpg")


# 调用
rename_random_files()