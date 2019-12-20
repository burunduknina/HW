"""
С помощью паттерна "Цепочка обязанностей" составьте список покупок для выпечки блинов.
Необходимо осмотреть холодильник и поочередно проверить, есть ли у нас необходимые ингридиенты:
    2 яйца
    300 грамм муки
    0.5 л молока
    100 грамм сахара
    10 мл подсолнечного масла
    120 грамм сливочного масла

В итоге мы должны получить список недостающих ингридиентов.
"""
from abc import ABC, abstractmethod


EGGS = 2
FLOUR = 300
MILK = 500
SUGAR = 100
OIL = 10
BUTTER = 120


def ingredient_handler(refrigerator, ingredient_name):
    amount = refrigerator.content.get(ingredient_name)
    recipe_amount = globals()[ingredient_name.upper()]
    if not amount:
        print(f'{ingredient_name} - {recipe_amount}')
    elif amount < recipe_amount:
        print(f'{ingredient_name} - {recipe_amount - amount}')


class Handler(ABC):
    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, refrigerator):
        pass


class AbstractHandler(Handler):
    _next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, refrigerator):
        if self._next_handler:
            return self._next_handler.handle(refrigerator)


class EggHandler(AbstractHandler):
    def handle(self, refrigerator):
        ingredient_handler(refrigerator, 'eggs')
        super().handle(refrigerator)


class FlourHandler(AbstractHandler):
    def handle(self, refrigerator):
        ingredient_handler(refrigerator, 'flour')
        super().handle(refrigerator)


class MilkHandler(AbstractHandler):
    def handle(self, refrigerator):
        ingredient_handler(refrigerator, 'milk')
        super().handle(refrigerator)


class SugarHandler(AbstractHandler):
    def handle(self, refrigerator):
        ingredient_handler(refrigerator, 'sugar')
        super().handle(refrigerator)


class OilHandler(AbstractHandler):
    def handle(self, refrigerator):
        ingredient_handler(refrigerator, 'oil')
        super().handle(refrigerator)


class ButterHandler(AbstractHandler):
    def handle(self, refrigerator):
        ingredient_handler(refrigerator, 'butter')
        super().handle(refrigerator)


class Refrigerator:
    def __init__(self, content):
        self.content = content


def create_shopping_list(refrigerator):
    egg_handler = EggHandler()
    flour_handler = FlourHandler()
    milk_handler = MilkHandler()
    sugar_handler = SugarHandler()
    oil_handler = OilHandler()
    butter_handler = ButterHandler()

    egg_handler.set_next(
        flour_handler).set_next(
        milk_handler).set_next(
        sugar_handler).set_next(
        oil_handler).set_next(
        butter_handler
    )
    print('Shopping list:')
    egg_handler.handle(refrigerator)


if __name__ == '__main__':
    refrigerator_dict = {
        'eggs': 1,
        'milk': 200,
        'flour': 300,
        'oil': 15,
        'butter': 15,
        'ice-cream': 5
    }
    refrigerator = Refrigerator(refrigerator_dict)
    create_shopping_list(refrigerator)
