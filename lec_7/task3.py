"""
Написать тесты(pytest or unittest) к предыдущим 2 заданиям, запустив которые, я бы смог бы проверить их корректность
Обязательно проверить всю критическую функциональность
"""
import time
import uuid

import pytest

from .task1 import SiamMeta
from .task2 import timer_property


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


class TestTimerPropertyFunc:
    def setup(self):
        class Message:

            def msg_get(self):
                self._msg = self.get_message()
                return self._msg

            def msg_set(self, param):
                self._msg = param

            def msg_del(self):
                self._msg = None

            def get_message(self):
                """
                Return random string
                """
                return uuid.uuid4()

            msg = timer_property(t=1)(msg_get, msg_set, msg_del)

        self.message_class = Message

    def test_get_method(self):
        """
        Check that __get__ save data and refresh it after timeout.
        """
        message = self.message_class()
        initial = message.msg
        assert initial is message.msg, "Data is not saved to cash"
        time.sleep(1)
        assert initial is not message.msg,\
            "Data is not refreshed after timeout"

    def test_set_method(self):
        """
        Check that __set__ save new data and reset timer.
        """
        message = self.message_class()
        initial = message.msg
        message.msg = 'test'
        assert message._msg is 'test', 'Data is not saved to attribute'
        assert message.msg is not initial, 'Timer is not reset'

    def test_delete_method(self):
        """
        Check that __delete__ set value to None data and reset timer.
        """
        message = self.message_class()
        initial = message.msg
        del message.msg
        assert message._msg is None
        assert message.msg is not initial


class TestTimerPropertyDecorators:
    def setup(self):
        class Message:
            @timer_property(t=1)
            def msg(self):
                self._msg = self.get_message()
                return self._msg

            @msg.setter  # reset timer also
            def msg(self, param):
                self._msg = param

            @msg.deleter
            def msg(self):
                self._msg = None

            def get_message(self):
                """
                Return random string
                """
                return uuid.uuid4()

        self.message_class = Message

    def test_getter_method(self):
        """
        Check that __getter__ call __get__ method.
        """
        message = self.message_class()
        initial = message.msg
        assert initial is message.msg, "Data is not saved to cash"
        time.sleep(1)
        assert initial is not message.msg,\
            "Data is not refreshed after timeout"

    def test_setter_method(self):
        """
        Check that __setter__ call __set__ method.
        """
        message = self.message_class()
        initial = message.msg
        message.msg = 'test'
        assert message._msg is 'test', 'Data is not saved to attribute'
        assert message.msg is not initial, 'Timer is not reset'

    def test_deleter_method(self):
        """
        Check that __setter__ call __set__ method.
        """
        message = self.message_class()
        initial = message.msg
        del message.msg
        assert message._msg is None
        assert message.msg is not initial


class TestTimerPropertyNotDefined:
    def setup(self):
        class Message:
            msg = timer_property(t=1)()

            def msg_get(self):
                self._msg = self.get_message()
                return self._msg

            def msg_set(self, param):
                self._msg = param

            def msg_del(self):
                self._msg = None

            def get_message(self):
                """
                Return random string
                """
                return uuid.uuid4()

        self.message_class = Message

    def test_get_not_defined(self):
        """
        Check that not defined __get__ is handled correctly.
        """
        message = self.message_class()
        with pytest.raises(AttributeError) as exc:
            message.msg
        assert "can't read attr" in str(exc.value)

    def test_set_not_defined(self):
        """
        Check that not defined __set__ is handled correctly.
        """
        message = self.message_class()
        with pytest.raises(AttributeError) as exc:
            message.msg = 'test'
        assert "can't set attr" in str(exc.value)

    def test_delete_not_defined(self):
        """
        Check that not defined __delete__ is handled correctly.
        """
        message = self.message_class()
        with pytest.raises(AttributeError) as exc:
            del message.msg
        assert "can't del attr" in str(exc.value)
