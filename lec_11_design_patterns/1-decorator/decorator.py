"""
Используя паттерн "Декоратор" реализуйте возможность дополнительно добавлять к кофе
    маршмеллоу, взбитые сливки и сироп, а затем вычислить итоговую стоимость напитка.
"""


class Component:
    def get_cost(self):
        raise NotImplementedError("Override get_cost method")


class BaseCoffe(Component):
    def __init__(self, component=None):
        self.component = component

    def get_cost(self):
        return 90


class Marshmallow(BaseCoffe):
    def get_cost(self):
        return self.component.get_cost() + 20


class Whip(BaseCoffe):
    def get_cost(self):
        return self.component.get_cost() + 30


class Syrup(BaseCoffe):
    def get_cost(self):
        return self.component.get_cost() + 10


if __name__ == "__main__":
    coffe = BaseCoffe()
    coffe = Whip(coffe)
    coffe = Marshmallow(coffe)
    coffe = Syrup(coffe)
    print("Итоговая стоимость за кофе: {}".format(str(coffe.get_cost())))
