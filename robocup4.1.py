import random
import statistics
from pathlib import Path


def process_3col_file():
    """生成10行3列的随机数文件，统计第二列的最大/最小/平均/中位数"""
    # 1. 生成10行3列的文件（逗号分隔）
    file_path = Path("3col_data.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        for _ in range(10):
            # 每行3个1~100的随机数
            row = [str(random.randint(1, 100)) for _ in range(3)]
            f.write(",".join(row) + "\n")

    # 2. 读取文件，提取第二列数据
    second_col = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            cols = line.strip().split(",")
            second_col.append(int(cols[1]))  # 第二列（索引1）

    # 3. 计算统计量
    max_val = max(second_col)
    min_val = min(second_col)
    avg_val = sum(second_col) / len(second_col)
    median_val = statistics.median(second_col)

    # 输出结果
    print(f"📊 第二列统计结果：")
    print(f"最大值：{max_val} | 最小值：{min_val}")
    print(f"平均值：{avg_val:.2f} | 中位数：{median_val}")


# 调用
process_3col_file()