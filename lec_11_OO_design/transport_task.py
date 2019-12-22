from abc import ABC, abstractmethod
from collections import deque
from functools import reduce


class InaccessibleMethodError(Exception):
    """
    Error if method is not allowed in this point.
    """


class Point(ABC):

    def __init__(self, containers=[], transport=[], distance=0):
        self._storage = deque(containers)
        self._garage = transport
        self._distance = distance
        super().__init__()

    def get_time(self):
        return self._storage and reduce(
            max, [container.time for container in self._storage]) or 0

    def send_container(self, destination):
        container = self._storage.popleft()
        transport = self.get_transport()
        start_time = max(container.time, transport.time)
        container.time = start_time + destination.distance
        transport.time = start_time + 2 * destination.distance
        destination.add_container(container)

    def add_container(self, container):
        return self._storage.append(container)

    @abstractmethod
    def get_transport(self):
        pass

    @property
    def distance(self):
        return self._distance

    @property
    def containers(self):
        return self._storage

    @property
    def ready(self):
        return self._storage[0]


class Factory(Point):

    def add_container(self, container):
        raise InaccessibleMethodError("We can't add containers to this point")

    def get_transport(self):
        min_trans = self._garage[0]
        for transport in self._garage:
            if transport.time < min_trans.time:
                min_trans = transport
        return min_trans


class Port(Point):

    def get_transport(self):
        return self._garage


class Warehouse(Point):

    def get_transport(self):
        raise InaccessibleMethodError("There is no transport at this point")

    def send_container(self, destination):
        raise InaccessibleMethodError(
            "We can't send containers from this destination")


class Transport(ABC):

    def __init__(self):
        self._busy_time = 0

    @property
    def time(self):
        return self._busy_time

    @time.setter
    def time(self, time):
        self._busy_time = time


class Truck(Transport):
    pass


class Ship(Transport):
    pass


class Container:
    def __init__(self, destination):
        self._destination = destination
        self._arrival_time = 0

    @property
    def time(self):
        return self._arrival_time

    @time.setter
    def time(self, time):
        self._arrival_time = time

    @property
    def destination(self):
        return self._destination


class Dispatcher(ABC):

    @abstractmethod
    def deliver_containers(self):
        pass

    @abstractmethod
    def get_result_time(self):
        pass


class HWTaskDispatcher(Dispatcher):

    def __init__(self, distance_port, distance_a, distance_b, containers):
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
    dispatcher = HWTaskDispatcher(1, 4, 5, input(
        'Please, enter container sequence:\n'))
    dispatcher.deliver_containers()
    print('Delivery time:', dispatcher.get_result_time())
