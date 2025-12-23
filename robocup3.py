# 生成斐波那契数列前20项
def fibonacci(n):
    # 初始化前两项
    fib = [0, 1]
    # 生成后续项（第3项到第n项）
    for i in range(2, n):
        next_num = fib[i-1] + fib[i-2]
        fib.append(next_num)
    return fib

# 获取前20项并输出
fib_20 = fibonacci(20)
print("斐波那契数列前20项为：")
print(fib_20)