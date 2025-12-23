class Person:
    """Person类：包含姓名、年龄、性别属性，以及信息打印方法"""
    def __init__(self, name: str, age: int, gender: str):
        # 初始化Person类的核心属性
        self.name = name
        self.age = age
        self.gender = gender

    def personInfo(self) -> None:
        """打印Person类的信息"""
        print(f"姓名：{self.name}，年龄：{self.age}，性别：{self.gender}")


class Student(Person):
    """Student类：继承自Person，新增学院、班级属性，重写信息方法与魔术方法"""
    def __init__(self, name: str, age: int, gender: str, college: str, class_: str):
        # 调用父类Person的初始化方法，继承姓名、年龄、性别属性
        super().__init__(name, age, gender)
        # 新增Student独有的属性（class是Python关键字，用class_替代）
        self.college = college
        self.class_ = class_

    def personInfo(self) -> None:
        """重写personInfo：先打印父类信息，再打印Student独有的信息"""
        # 调用父类的personInfo方法，复用父类逻辑
        super().personInfo()
        # 补充打印学院、班级信息
        print(f"学院：{self.college}，班级：{self.class_}")

    def __str__(self) -> str:
        """重写__str__魔术方法：返回Student的完整信息字符串"""
        return (
            f"Student信息：\n"
            f"姓名：{self.name}\n"
            f"年龄：{self.age}\n"
            f"性别：{self.gender}\n"
            f"学院：{self.college}\n"
            f"班级：{self.class_}"
        )


# 测试代码（验证类的功能）
if __name__ == "__main__":
    # 1. 测试Person类
    print("=== Person类测试 ===")
    person = Person(name="张三", age=25, gender="男")
    person.personInfo()  # 打印Person信息

    # 2. 测试Student类
    print("\n=== Student类测试（personInfo方法） ===")
    student = Student(
        name="李四",
        age=20,
        gender="女",
        college="计算机学院",
        class_="计科2023-1班"
    )
    student.personInfo()  # 打印Student的完整信息

    # 3. 测试Student的__str__魔术方法
    print("\n=== Student类测试（__str__方法） ===")
    print(student)  # 直接打印Student实例，触发__str__方法