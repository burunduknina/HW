"""HW for lecture#11 'OO-design.'"""
from abc import ABC, abstractmethod
from functools import reduce

from lec_12.transport_logger import LOGGER


class Point(ABC):
    """Interface for location"""

    def __init__(
            self, containers=None, transport=None, distance=0, routs=None):
        """
        :param (list, optional) containers: list of containers
        :param (list, optional) transport: list of transport
        :param (int, optional) distance: distance to the previous point
        :param (dict, optional) distance: distance to the previous point
        """
        self._storage = containers or []
        self._garage = transport or []
        self._distance = distance
        self._routs = routs
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

    def get_containers(self):
        """Return list of containers in the storage.
        :return:
            list: container in storage.
        """
        return self._storage

    def get_routs(self):
        """Return dict of routs from this point.
        :return:
            dict: possible destinations.
        """
        return self._routs

    @property
    def distance(self):
        """
        :return:
            int: distance to the previous point.
        """
        return self._distance

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
        self.get_containers().append(container)


class SendContainerMixin:
    """Mixin for Point to send containers."""

    def send_container(self):
        """Send container to other Point
        """
        container = self.get_containers().pop(0)
        transport = self.get_transport_to_send()
        destination = self.get_routs().get(container.destination)
        start_time = max(container.time, transport.time)
        LOGGER.info(f'Container {container.destination} started from '
                    f'{self.__class__.__name__} to '
                    f'{destination.__class__.__name__} at {start_time}')
        container.time = start_time + destination.distance
        transport.time = start_time + 2 * destination.distance
        destination.add_container(container)
        LOGGER.info(f'Container {container.destination} delivered from to '
                    f'{destination.__class__.__name__} at {container.time}')


class GetTransportMixin:
    """Mixin for select transport."""

    def get_transport_to_send(self):
        """Calculates what transport can start earlier.
        :return:
            Transport: transport to deliver next container
        """
        min_trans = self.get_transport()[0]
        for transport in self.get_transport():
            if transport.time < min_trans.time:
                min_trans = transport
        return min_trans


class Factory(GetTransportMixin, SendContainerMixin, Point):
    """Factory: starting point."""

    def send_containers(self):
        """Send all containers to next Point
        """
        for i in range(len(self.get_containers())):
            self.send_container()


class Port(GetTransportMixin, AddContainerMixin, SendContainerMixin, Point):
    """Port: intermediate point."""

    def sort_containers(self):
        self._storage.sort(key=lambda x: x.time)

    def send_containers(self):
        """Send all containers to next Point
        """
        self.sort_containers()
        for i in range(len(self.get_containers())):
            self.send_container()


class Warehouse(AddContainerMixin, Point,):
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


# class HWTaskDispatcher(Dispatcher):
#     """Solution of HW task."""
#
#     def __init__(self, distance_port, distance_a, distance_b, containers):
#         """
#         :param (int) distance_port: distance from Factory to Port
#         :param (int) distance_a: distance from Port to WarehouseA
#         :param (int) distance_b: distance from Port to WarehouseB
#         :param (str) containers: Container sequence
#         """
#         LOGGER.info(f'Containers to delivery: {containers}')
#         self._warehouse_a = Warehouse(distance=distance_a)
#         self._warehouse_b = Warehouse(distance=distance_b)
#         self._containers = [Container(dest) for dest in containers]
#         self._truck1, self._truck2 = Truck(), Truck()
#         self._ship = Ship()
#         self._factory = Factory(
#             self._containers, [self._truck1, self._truck2])
#         self._port = Port([], self._ship, distance_port)
#
#     def deliver_containers(self):
#         for idx in range(len(self._factory.get_containers())):
#             if self._factory.ready.destination == 'A':
#                 self._factory.send_container(self._port)
#             else:
#                 self._factory.send_container(self._warehouse_b)
#         for idx in range(len(self._port.get_containers())):
#             self._port.send_container(self._warehouse_a)
#
#     def get_result_time(self):
#         return max(
#         self._warehouse_a.get_time(), self._warehouse_b.get_time())
#

class HWTaskDispatcherPlus(Dispatcher):
    """Solution of HW+ task."""

    def __init__(self, warehouses, ports, factories, containers):
        """
        :param (dict) warehouses: dict{warehouse_name: distance}
        :param (dict) ports: dict{port_name: [distance, amount of ships]}
        :param (list) factories: list[[destinations, amount of tracks]]
        :param (list) containers: list[str]
        """
        LOGGER.info(f'Containers to delivery: {containers}')
        self.warehouses = {key: Warehouse(
            distance=value) for key, value in warehouses.items()}
        ships = {key: [Ship() for i in range(
            value[1])] for key, value in ports.items()}
        self.ports = {key: Port([], ships.get(key), value[0], {
            key: self.warehouses.get(key)}) for key, value in ports.items()}
        self.factories = []
        for i, factory in enumerate(factories):
            factory_containers = [Container(dest) for dest in containers[i]]
            factory_trucks = [Truck() for i in range(factory[1])]
            factory_routs = {key: self.ports.get(key) or self.warehouses.get(
                key) for key in factory[0]}
            self.factories.append(Factory(
                factory_containers, factory_trucks, 0, factory_routs))

    def deliver_containers(self):
        for factory in self.factories:
            factory.send_containers()
        for port in self.ports.values():
            port.send_containers()

    def get_result_time(self):
        return max([w.get_time() for w in self.warehouses.values()])


if __name__ == '__main__':
    LOGGER.info("Program started")
    warehouses1 = {'A': 4, 'B': 5}
    ports1 = {'A': [1, 1]}
    factories1 = [['AB', 2]]
    containers1 = ['AABABBAB']
    warehouses2 = {'A': 5, 'B': 4}
    ports2 = {'B': [1, 1]}
    factories2 = [['AB', 2], ['B', 2]]
    containers2 = ['AAB', 'BB']
    # dispatcher = HWTaskDispatcher(1, 4, 5, input(
    #     'Please, enter container sequence:\n'))
    dispatcher1 = HWTaskDispatcherPlus(
        warehouses1, ports1, factories1, containers1)
    dispatcher1.deliver_containers()
    delivery_time1 = dispatcher1.get_result_time()
    print(f'Delivery time for hw task and input '
          f'{containers1[0]}: {delivery_time1}')
    LOGGER.info(f'All containers delivered at {delivery_time1}')
    dispatcher2 = HWTaskDispatcherPlus(
        warehouses2, ports2, factories2, containers2)
    dispatcher2.deliver_containers()
    delivery_time2 = dispatcher2.get_result_time()
    print(f'Delivery time for hw+ task and input {containers2[0]},'
          f' {containers2[1]} : {delivery_time2}')
    LOGGER.info(f'All containers delivered at {delivery_time2}')
    LOGGER.info("Program finished")
