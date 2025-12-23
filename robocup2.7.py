def find_last_person(total_people, count_num):
    # 初始化：1~total_people的编号列表
    people = list(range(1, total_people + 1))
    current_idx = 0  # 当前报数的起始位置

    while len(people) > 1:
        # 报数到count_num对应的索引：当前位置 + (count_num-1)，取余保证环形
        remove_idx = (current_idx + count_num - 1) % len(people)
        people.pop(remove_idx)
        # 下一次报数的起始位置是被移除元素的下一个（即当前remove_idx，因为pop后后续元素前移）
        current_idx = remove_idx

    return people[0]


if __name__ == "__main__":
    last_num = find_last_person(233, 3)
    print(f"最后留下的是原来的第 {last_num} 号")