"""HW for lecture#11 'OO-design.'"""
from abc import ABC, abstractmethod
from collections import deque
from functools import reduce

from lec_11_OO_design.transport_logger import LOGGER


class Point(ABC):
    """Interface for location"""

    def __init__(self, containers=[], transport=[], distance=0):
        """
        :param (list, optional) containers: list of containers
        :param (list, optional) transport: list of transport
        :param (int, optional) distance: distance to the previous point
        """
        self._storage = deque(containers)
        self._garage = transport
        self._distance = distance
        super().__init__()
        LOGGER.info(f'{self.__class__.__name__} with distance '
                    f'{self._distance} and {len(self._storage)} '
                    f'containers is created.')

    def get_time(self):
        """Calculates the time at which the last container arrived.
        :return:
            int: time to deliver containers to this point
        """
        return self._storage and reduce(
            max, [container.time for container in self._storage]) or 0

    def get_transport(self):
        """Calculates what transport can start earlier.
        :return:
            Transport: transport to deliver next container
        """
        return self._garage

    @property
    def distance(self):
        """
        :return:
            int: distance to the previous point.
        """
        return self._distance

    @property
    def containers(self):
        """
        :return:
            list: container in storage.
        """
        return self._storage

    @property
    def ready(self):
        """
        :return:
            Container: container ready to start.
        """
        return self._storage[0]


class AddContainerMixin:
    """Mixin for Point to add containers."""

    def add_container(self, container):
        """Add container to Points storage
        :param (Container) container: container to add
        """
        self._storage.append(container)


class SendContainerMixin:
    """Mixin for Point to send containers."""

    def send_container(self, destination):
        """Send container to other Point
        :param (Point) destination: where to send
        """
        container = self._storage.popleft()
        transport = self.get_transport()
        start_time = max(container.time, transport.time)
        LOGGER.info(f'Container {container.destination} started from '
                    f'{self.__class__.__name__} to '
                    f'{destination.__class__.__name__} at {start_time}')
        container.time = start_time + destination.distance
        transport.time = start_time + 2 * destination.distance
        destination.add_container(container)
        LOGGER.info(f'Container {container.destination} delivered from to '
                    f'{destination.__class__.__name__} at {container.time}')


class Factory(Point, SendContainerMixin):
    """Factory: starting point."""

    def get_transport(self):
        min_trans = self._garage[0]
        for transport in self._garage:
            if transport.time < min_trans.time:
                min_trans = transport
        return min_trans


class Port(Point, AddContainerMixin, SendContainerMixin):
    """Port: intermediate point."""
    pass


class Warehouse(Point, AddContainerMixin):
    """Warehouse: final destination."""
    pass


class Transport(ABC):
    """Interface for transport"""

    def __init__(self):
        self._busy_time = 0

    @property
    def time(self):
        return self._busy_time

    @time.setter
    def time(self, time):
        self._busy_time = time


class Truck(Transport):
    """Truck: Transport for roads."""
    pass


class Ship(Transport):
    """Ship: Transport for sea."""
    pass


class Container:
    """Container"""

    def __init__(self, destination):
        """
        :param (str) destination: end point
        """
        self._destination = destination
        self._arrival_time = 0

    @property
    def time(self):
        """
        :return:
            int: arrival time.
        """
        return self._arrival_time

    @time.setter
    def time(self, time):
        self._arrival_time = time

    @property
    def destination(self):
        """
        :return:
            str: final destination
        """
        return self._destination


class Dispatcher(ABC):
    """Interface to delivering."""

    @abstractmethod
    def deliver_containers(self):
        """Deliver containers from start to final destination."""
        pass

    @abstractmethod
    def get_result_time(self):
        """
        Calculate time to delivery.
        :return:
            int: time to delivery
        """
        pass


class HWTaskDispatcher(Dispatcher):
    """Solution of HW task."""

    def __init__(self, distance_port, distance_a, distance_b, containers):
        """
        :param (int) distance_port: distance from Factory to Port
        :param (int) distance_a: distance from Port to WarehouseA
        :param (int) distance_b: distance from Port to WarehouseB
        :param (str) containers: Container sequence
        """
        LOGGER.info(f'Containers to delivery: {containers}')
        self._warehouse_a = Warehouse(distance=distance_a)
        self._warehouse_b = Warehouse(distance=distance_b)
        self._containers = [Container(dest) for dest in containers]
        self._truck1, self._truck2 = Truck(), Truck()
        self._ship = Ship()
        self._factory = Factory(self._containers, [self._truck1, self._truck2])
        self._port = Port([], self._ship, distance_port)

    def deliver_containers(self):
        for idx in range(len(self._factory.containers)):
            if self._factory.ready.destination == 'A':
                self._factory.send_container(self._port)
            else:
                self._factory.send_container(self._warehouse_b)
        for idx in range(len(self._port.containers)):
            self._port.send_container(self._warehouse_a)

    def get_result_time(self):
        return max(self._warehouse_a.get_time(), self._warehouse_b.get_time())


if __name__ == '__main__':
    LOGGER.info("Program started")
    dispatcher = HWTaskDispatcher(1, 4, 5, input(
        'Please, enter container sequence:\n'))
    dispatcher.deliver_containers()
    delivery_time = dispatcher.get_result_time()
    print('Delivery time:', delivery_time)
    LOGGER.info(f'All containers delivered at {delivery_time}')
    LOGGER.info("Program finished")
