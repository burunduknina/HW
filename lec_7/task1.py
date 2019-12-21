"""

Реализовать такой метакласс, что экземпляры класса созданного с помощью него
будут удовлетворять следующим требованиям:

* объекты созданные с одинаковыми аттрибутами будут одним и тем же объектом
* объекты созданные с разными аттрибутами будут разными объектами
* у любого объекта есть мозможность получить доступ к другим объектам
    того же класса


>>> unit1 = SiamObj('1', '2', a=1)
>>> unit2 = SiamObj('1', '2', a=1)
>>> unit1 is unit2
True
>>> unit3 = SiamObj('2', '2', a=1)
>>> unit3.connect('1', '2', 1).a = 2
>>> unit2.a == 2
True
>>> pool = unit3.pool
>>> print(len(pool))
2
>>> del unit3
>>> print(len(pool))
1

"""
import inspect
import weakref


class SiamMeta(type):
    _instances = {}

    @classmethod
    def __prepare__(mcs, name, bases):
        return {'connect': mcs.connect, 'pool': weakref.WeakSet()}

    def __call__(cls, *args, **kwargs):
        inst_args = str(inspect.signature(
            cls.__init__).bind_partial(None, *args, **kwargs))
        if cls not in cls._instances:
            cls._instances[cls] = weakref.WeakValueDictionary()
        if inst_args not in SiamMeta._instances[cls]:
            instance = super(SiamMeta, cls).__call__(*args, **kwargs)
            SiamMeta._instances[cls][inst_args] = instance
        cls.pool.add(cls._instances[cls][inst_args])
        return SiamMeta._instances[cls][inst_args]

    def connect(self, *args, **kwargs):
        cls = self.__class__
        inst_args = str(inspect.signature(
            cls.__init__).bind_partial(None, *args, **kwargs))
        inst_ref = SiamMeta._instances[cls].get(inst_args, None)
        if inst_ref:
            return inst_ref
        else:
            raise ValueError('There is no instance for these arguments')
