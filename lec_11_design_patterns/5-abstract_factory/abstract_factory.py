"""
Представьте, что вы пишите программу по формированию и выдачи комплексных обедов для сети столовых, которая стала
расширяться и теперь предлагает комплексные обеды для вегетарианцев, детей и любителей китайской кухни.

С помощью паттерна "Абстрактная фабрика" вам необходимо реализовать выдачу комплексного обеда, состоящего из трёх
позиций (первое, второе и напиток).
В файле menu.yml находится меню на каждый день, в котором указаны позиции и их принадлежность к
определенному типу блюд.
"""
import yaml
from abc import ABC, abstractmethod


class DayException(Exception):
    pass


class AbstractMenu(ABC):
    @abstractmethod
    def __init__(self):
        first_course = None
        second_course = None
        drink = None

    def get_first_course(self, day):
        print('first course: ', self.first_course[day])

    def get_second_course(self, day):
        print('second course: ', self.second_course[day])

    def get_drink(self, day):
        print('drink: ', self.drink[day])


class VeganMenu(AbstractMenu):
    def __init__(self, menu):
        super().__init__()
        self.first_course = {
            key: value['first_courses']['vegan']
            for key, value in menu.items()
        }
        self.second_course = {
            key: value['second_courses']['vegan']
            for key, value in menu.items()
        }
        self.drink = {
            key: value['drinks']['vegan']
            for key, value in menu.items()
        }


class ChildMenu(AbstractMenu):
    def __init__(self, menu):
        super().__init__()
        self.first_course = {
            key: value['first_courses']['child']
            for key, value in menu.items()
        }
        self.second_course = {
            key: value['second_courses']['child']
            for key, value in menu.items()
        }
        self.drink = {
            key: value['drinks']['child']
            for key, value in menu.items()
        }


class ChineseMenu(AbstractMenu):
    def __init__(self, menu):
        super().__init__()
        self.first_course = {
            key: value['first_courses']['chinese']
            for key, value in menu.items()
        }
        self.second_course = {
            key: value['second_courses']['chinese']
            for key, value in menu.items()
        }
        self.drink = {
            key: value['drinks']['chinese']
            for key, value in menu.items()
        }


class AbstractFactory(ABC):
    @abstractmethod
    def get_lunch(self, menu):
        pass


class MondayFactory(AbstractFactory):
    def get_lunch(self, menu):
        menu.get_first_course('Monday')
        menu.get_second_course('Monday')
        menu.get_drink('Monday')


class TuesdayFactory(AbstractFactory):
    def get_lunch(self, menu):
        menu.get_first_course('Tuesday')
        menu.get_second_course('Tuesday')
        menu.get_drink('Tuesday')


class WednesdayFactory(AbstractFactory):
    def get_lunch(self, menu):
        menu.get_first_course('Wednesday')
        menu.get_second_course('Wednesday')
        menu.get_drink('Wednesday')


class ThursdayFactory(AbstractFactory):
    def get_lunch(self, menu):
        menu.get_first_course('Thursday')
        menu.get_second_course('Thursday')
        menu.get_drink('Thursday')


class FridayFactory(AbstractFactory):
    def get_lunch(self, menu):
        menu.get_first_course('Friday')
        menu.get_second_course('Friday')
        menu.get_drink('Friday')


class SaturdayFactory(AbstractFactory):
    def get_lunch(self, menu):
        menu.get_first_course('Saturday')
        menu.get_second_course('Saturday')
        menu.get_drink('Saturday')


class SundayFactory(AbstractFactory):
    def get_lunch(self, menu):
        menu.get_first_course('Sunday')
        menu.get_second_course('Sunday')
        menu.get_drink('Sunday')


def get_lunch(day, kind):
    lunch_day = {
        'Monday': MondayFactory(),
        'Tuesday': TuesdayFactory(),
        'Wednesday': WednesdayFactory(),
        'Thursday': ThursdayFactory(),
        'Friday': FridayFactory(),
        'Saturday': SaturdayFactory(),
        'Sunday': SundayFactory()
    }.get(day)
    if lunch_day:
        return lunch_day.get_lunch(kind)
    else:
        raise DayException


if __name__ == '__main__':
    with open('menu.yml', encoding="utf8") as file:
        menu = yaml.safe_load(file)
    vegan = VeganMenu(menu)
    child = ChildMenu(menu)
    chinese = ChineseMenu(menu)
    try:
        get_lunch('Friday', child)
    except DayException:
        print('Такого дня не существует.')
