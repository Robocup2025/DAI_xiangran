# 方法1：通过数值交换实现升序排序
def sort_by_swap():
    x = int(input("请输入第一个整数x: "))
    y = int(input("请输入第二个整数y: "))
    z = int(input("请输入第三个整数z: "))
  # 确保x是最小值
    if x > y:
        x, y = y, x  # 交换x和y
    if x > z:
        x, z = z, x  # 交换x和z
    # 确保y是中间值
    if y > z:
        y, z = z, y

    print(f"从小到大排序结果：{x}, {y}, {z}")5

# 方法2：通过列表排序实现
def sort_by_list():
    x = int(input("请输入第一个整数x: "))
    y = int(input("请输入第二个整数y: "))
    z = int(input("请输入第三个整数z: "))

    num_list = [x, y, z]
    num_list.sort()  # 列表自带升序排序方法
    print(f"从小到大排序结果：{num_list[0]}, {num_list[1]}, {num_list[2]}")


# 调用其中一种方法（这里以方法2为例）
sort_by_list()