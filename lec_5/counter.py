"""
Написать декоратор instances_counter, который применяется к любому классу
и добавляет ему 2 метода:
get_created_instances - возвращает количество созданых экземпляров класса
reset_instances_counter - сбросить счетчик экземпляров,
возвращает значение до сброса
Имя декоратора и методов не менять

Ниже пример использования
"""


def instances_counter(cls):
    cls.counter = 0
    cls_init = cls.__init__

    def __init__(self, *args, **kwargs):
        cls.counter += 1
        cls_init(self, *args, **kwargs)

    @staticmethod
    def get_created_instances():
        return cls.counter

    @staticmethod
    def reset_instances_counter():
        counter = cls.counter
        cls.counter = 0
        return counter

    cls.__init__ = __init__
    cls.get_created_instances = get_created_instances
    cls.reset_instances_counter = reset_instances_counter
    return cls


@instances_counter
class User:
    pass


if __name__ == '__main__':

    User.get_created_instances()  # 0
    user, _, _ = User(), User(), User()
    user.get_created_instances()  # 3
    user.reset_instances_counter()  # 3
    User.get_created_instances()  # 0
