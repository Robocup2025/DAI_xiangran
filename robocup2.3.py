def analyze_digit_info():
    # 输入验证：确保获取正整数
    while True:
        try:
            num = int(input("请输入一个任意位数的正整数："))
            if num <= 0:
                print("❌ 请输入正整数！")
                continue
            break
        except ValueError:
            print("❌ 输入无效，请输入整数！")

    # 方法1：数值运算拆分（纯数字逻辑）
    print("\n=== 方法1：数值运算实现 ===")
    temp_num = num
    digit_count = 0
    digit_list = []  # 存储各位数字（逆序收集）
    while temp_num > 0:
        last_digit = temp_num % 10  # 取最后一位
        digit_list.append(last_digit)
        temp_num = temp_num // 10   # 去掉最后一位
        digit_count += 1
    print(f"1. 该数是 {digit_count} 位数")
    print(f"2. 逆序打印各位数字：", end="")
    for d in digit_list:
        print(d, end=" ")

    # 方法2：字符串处理（更简洁）
    print("\n\n=== 方法2：字符串方法实现 ===")
    num_str = str(num)
    print(f"1. 该数是 {len(num_str)} 位数")
    print(f"2. 逆序打印各位数字：", end="")
    for d in num_str[::-1]:  # 字符串逆序切片
        print(d, end=" ")


# 调用函数
analyze_digit_info()