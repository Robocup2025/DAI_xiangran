# 生成所有无重复数字的三位数
count = 0  # 统计符合条件的三位数数量
result = []  # 存储符合条件的三位数

# 遍历百位、十位、个位（取值1-4）
for hundreds in range(1, 5):
    for tens in range(1, 5):
        for units in range(1, 5):
            # 确保三个位数字不重复
            if hundreds != tens and tens != units and hundreds != units:
                num = hundreds * 100 + tens * 10 + units
                result.append(num)
                count += 1

# 输出结果
print(f"能组成 {count} 个无重复数字的三位数，分别是：")
print(result)