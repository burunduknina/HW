"""
Написать тесты(pytest or unittest) к предыдущим 2 заданиям, запустив которые, я бы смог бы проверить их корректность
Обязательно проверить всю критическую функциональность
"""
import pytest

from .task1 import SiamMeta


class TestSiamMeta:
    def setup(self):

        class SiamObj_1(metaclass=SiamMeta):
            def __init__(self, k, p, a):
                self.k = k
                self.p = p
                self.a = a

        class SiamObj_2(metaclass=SiamMeta):
            def __init__(self, k, p, a):
                self.k = k
                self.p = p
                self.a = a

        self.class_1 = SiamObj_1
        self.class_2 = SiamObj_2

    def test_classes_not_equal(self):
        """
        Check that classes with the same metaclass and __init__ don't match.
        """
        assert self.class_1 is not self.class_2

    def test_equal_args(self):
        """
        Check that instances with the same arguments match.
        """
        unit_1 = self.class_1('1', '2', a=1)
        unit_2 = self.class_1('1', '2', a=1)
        assert unit_1 is unit_2

    def test_differ_args(self):
        """
        Check that instances with the same arguments match.
        """
        unit_1 = self.class_1('1', '2', 1)
        unit_2 = self.class_1('12', '2', 1)
        assert unit_1 is not unit_2

    def test_args_and_kwargs(self):
        """
        Check that different ways of passing arguments don't affect instance
        creation
        """
        unit_1 = self.class_1('1', '2', a=1)
        unit_2 = self.class_1('1', '2', 1)
        assert unit_1 is unit_2

    def test_instances_from_deffer_classes(self):
        """
        Check that instances from different classes with the same arguments
        don't match.
        """
        unit_1 = self.class_1('1', '2', a=1)
        unit_2 = self.class_2('1', '2', a=1)
        assert unit_1 is not unit_2

    def test_connect_to_existing_instance(self):
        """
        Check that instance has access to others by using their arguments.
        """
        unit_1 = self.class_1('1', '2', a=1)
        unit_2 = self.class_1('1', '2', a=1)
        unit_3 = self.class_1('1', '2', a=2)
        unit_2.connect('1', '2', a=1).a = 3
        assert unit_1.a == 3
        assert unit_2.a == 3
        assert unit_3.a == 2

    def test_connect_to_non_existing_instance(self):
        """
        Check that connect to non existing instance is handled correctly.
        """
        unit_1 = self.class_1('1', '2', a=1)
        with pytest.raises(ValueError) as exc:
            unit_1.connect('1', '2', a=3)
        assert 'There is no instance for these arguments' in str(exc.value)

    def test_connect_to_self(self):
        """
        Check that instance can connect to itself.
        """
        unit_1 = self.class_1('1', '2', a=1)
        unit_1.connect('1', '2', a=1).a = 5
        assert unit_1.a == 5

    def test_pool_wo_instances(self):
        """
        Check that pool of class w/o instances is empty.
        """
        assert len(self.class_1.pool) == 0

    def test_pool_with_equal_instances(self):
        """
        Check that pool contains one reference for equal instances.
        """
        unit_1 = self.class_1('1', '2', a=1)
        unit_2 = self.class_1('1', '2', a=1)
        assert len(self.class_1.pool) == 1

    def test_pool_with_differ_instances(self):
        """
        Check that pool contains references for all unique instances.
        """
        unit_1 = self.class_1('1', '2', a=1)
        unit_2 = self.class_1('2', '2', a=1)
        assert len(self.class_1.pool) == 2

    def test_pool_after_del_unique(self):
        """
        Check that pool decreases after delete of unique instance.
        """
        unit_1 = self.class_1('1', '2', a=1)
        unit_2 = self.class_1('2', '2', a=1)
        del unit_1
        assert len(self.class_1.pool) == 1

    def test_pool_after_del_not_unique(self):
        """
        Check that pool doesn't change after delete of unique instance.
        """
        unit_1 = self.class_1('1', '2', a=1)
        unit_2 = self.class_1('1', '2', a=1)
        del unit_1
        assert len(self.class_1.pool) == 1

    def test_pool_after_del_all_instances(self):
        """
        Check that pool is empty after delete of all instances.
        """
        unit_1 = self.class_1('1', '2', a=1)
        del unit_1
        assert len(self.class_1.pool) == 0

    def test_pool_independence(self):
        """
        Check that pool of one class is independent of other class.
        """
        unit_1 = self.class_1('1', '2', a=1)
        assert len(self.class_2.pool) == 0
