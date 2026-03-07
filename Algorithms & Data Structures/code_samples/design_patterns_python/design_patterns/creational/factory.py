from abc import ABC, abstractmethod


class DeliveryRoute:
    """DeliveryRoute class"""

    def __init__(self, fr: str, to: str,) -> None:
        self.fr = fr
        self.to = to

    def reverse(self) -> None:
        self.to, self.fr = self.fr, self.to

    def __str__(self) -> str:
        return f'Route from {self.fr} to {self.to}'


class Transport(ABC):
    """Abstract transport class"""

    def __init__(self, route: DeliveryRoute) -> None:
        self.route = route

    @property
    def fr(self) -> str:
        return self.route.fr

    @property
    def to(self) -> str:
        return self.route.to

    @property
    def name(self) -> str:
        return type(self).__name__

    def _deliver(self) -> None:
        self.route.reverse()

    @abstractmethod
    def deliver(self) -> None:
        """Delivery abstract transport implementation """
        pass


class Truck(Transport):
    """Concrete Truck transport class"""

    def deliver(self) -> None:
        self._deliver()
        print('Truck delivered')


class Ship(Transport):
    """Concrete Ship transport class"""

    def deliver(self) -> None:
        self._deliver()
        print('Ship delivered')


class Train(Transport):
    """Concrete Train transport class"""

    def deliver(self) -> None:
        self._deliver()
        print('Train delivered')


class Logistics:
    """Logistics Class"""

    def __init__(self) -> None:
        self.queue: list[Transport] = []

    def __len__(self) -> int:
        return len(self.queue)

    def __str__(self) -> str:
        return f'Logistics ({len(self)} in queue) {", ".join([x.name for x in self.queue])}'

    def add_transport(self, transport: Transport) -> None:
        """Add transport"""
        self.queue.append(transport)

    def deliver(self) -> None:
        """Deliver first transport in queue"""

        if not len(self):
            print('No transport in queue')
            return
        t = self.queue.pop(0)
        t.deliver()
        print(f'Delivered {t.name} on {t.route}')


class Factory:
    """Transport factory class"""

    @staticmethod
    def createDeliveryRoute(*args, **kwargs) -> DeliveryRoute:
        return DeliveryRoute(*args, **kwargs)

    @staticmethod
    def createTruck(*args, **kwargs) -> Truck:
        return Truck(*args, **kwargs)

    @staticmethod
    def createTrain(*args, **kwargs) -> Train:
        return Train(*args, **kwargs)

    @staticmethod
    def createShip(*args, **kwargs) -> Ship:
        return Ship(*args, **kwargs)

    @staticmethod
    def createLogistics() -> Logistics:
        return Logistics()
