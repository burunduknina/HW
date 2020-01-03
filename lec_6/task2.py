"""
Реализовать класс Quaternion, позволяющий работать с кватернионами
https://ru.wikipedia.org/wiki/%D0%9A%D0%B2%D0%B0%D1%82%D0%B5%D1%80%D0%BD%D0%B8%D0%BE%D0%BD
Функциональность (магическими методами):
- сложение
- умножение
- деление
- сравнение
- нахождение модуля
- строковое представление и repr
По желанию:
- взаимодействие с числами других типов
"""
import math


class Quaternion:

    def __init__(self, a=0, b=0, c=0, d=0):
        self.real = a
        self.i = b
        self.j = c
        self.k = d

    def __str__(self):
        return f'{self.real} + {self.i}i + {self.j}j + {self.k}k'

    def __repr__(self):
        return f'Quaternion({self.real}, {self.i}, {self.j}, {self.k})'

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Quaternion(self.real + other, self.i, self.j, self.k)
        elif isinstance(other, Quaternion):
            a = self.real + other.real
            b = self.i + other.i
            c = self.j + other.j
            d = self.k + other.k
            return Quaternion(a, b, c, d)
        else:
            raise TypeError('This type is not supported')

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Quaternion(self.real * other, self.i * other,
                              self.j * other, self.k * other)
        elif isinstance(other, Quaternion):
            a = (self.real * other.real
                 - self.i * other.i
                 - self.j * other.j
                 - self.k * other.k)
            b = (self.real * other.i
                 + self.i * other.real
                 + self.j * other.k
                 - self.k * other.j)
            c = (self.real * other.j
                 + self.j * other.real
                 + self.k * other.i
                 - self.i * other. k)
            d = (self.real * other.k
                 + self.k * other.real
                 + self.i * other.j
                 - self.j * other.i)
            return Quaternion(a, b, c, d)
        else:
            raise ValueError('This type is not supported')

    def norm(self):
        return math.sqrt(
            self.real ** 2 + self.i ** 2 + self.j ** 2 + self.k ** 2)

    def convert(self):
        return Quaternion(
            self.real, - self.i, -self.j, -self.k) / (self.norm() ** 2)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Quaternion(
                self.real / other,
                self.i / other,
                self.j / other,
                self.k / other
            )
        elif isinstance(other, Quaternion):
            return self * other.convert()
        else:
            raise TypeError('This type is not supported')

    def __eq__(self, other):
        return all(
            [
                isinstance(self, Quaternion),
                isinstance(other, Quaternion),
                self.real == other.real,
                self.i == other.i,
                self.j == other.j,
                self.k == other.k,
            ]
        )
