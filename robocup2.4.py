def check_palindrome():
    # 输入验证：确保获取正整数
    while True:
        try:
            num = int(input("\n\n请输入一个任意位数的正整数："))
            if num <= 0:
                print("❌ 请输入正整数！")
                continue
            break
        except ValueError:
            print("❌ 输入无效，请输入整数！")

    # 方法1：字符串方法（简洁高效）
    print("\n=== 方法1：字符串比较法 ===")
    num_str = str(num)
    if num_str == num_str[::-1]:  # 原字符串与逆序字符串比较
        print(f"{num} 是回文数")
    else:
        print(f"{num} 不是回文数")

    # 方法2：数值运算判断（不依赖字符串）
    print("\n=== 方法2：数值反转法 ===")
    temp_num = num
    reversed_num = 0  # 存储反转后的数字
    while temp_num > 0:
        reversed_num = reversed_num * 10 + temp_num % 10  # 拼接最后一位
        temp_num = temp_num // 10  # 去掉最后一位
    if num == reversed_num:
        print(f"{num} 是回文数")
    else:
        print(f"{num} 不是回文数")


# 调用函数
check_palindrome()