from abc import ABC
from dataclasses import dataclass
from enum import Enum


class Fuel(Enum):
    """Fuel Enum Class"""
    diesel = 1
    gasoline = 2
    methane = 3
    electric = 4


class Transmission(Enum):
    """Transmission Enum Class"""
    manual = 1
    automatic = 2


@dataclass
class Engine:
    """Engine Data Class"""

    def __init__(self, fuel: Fuel, cylinders: int = 0):
        if fuel == fuel.electric and cylinders > 0:
            raise Exception('And electric engine does not have cylinders')
        if fuel != fuel.electric and cylinders < 1:
            raise Exception('A non electric engine needs cylinders')
        self.fuel = fuel
        self.cylinders = cylinders

    def __str__(self) -> str:
        if self.fuel != Fuel.electric:
            return f'Engine ({self.fuel.name} V{self.cylinders})'
        return f'Engine ({self.fuel.name})'


@dataclass
class AbstractVehicle(ABC):
    """Abstract Vehicle Data Class"""
    engine = None
    transmission = None
    wheels = None
    seats = None

    def set_engine(self, engine: Engine) -> None:
        self.engine = engine

    def set_transmission(self, transmission: Transmission) -> None:
        self.transmission = transmission

    def set_wheels(self, wheels: int) -> None:
        self.wheels = wheels

    def set_seats(self, seats: int) -> None:
        self.seats = seats


@dataclass
class VehicleBlueprint(AbstractVehicle):
    """Vehicle Blueprint Data Class"""

    def __init__(self, engine: Engine, transmission: Transmission, wheels: int, seats: int):
        if wheels < 1:
            raise Exception('A vehicle must have wheels')
        if seats < 1:
            raise Exception('A vehicle must have seats')
        self.engine = engine
        self.transmission = transmission
        self.wheels = wheels
        self.seats = seats


@dataclass
class VehicleBuilt(AbstractVehicle):
    """Vehicle Built Data Class"""

    @property
    def is_built(self) -> bool:
        if None in (self.engine, self.transmission, self.wheels, self.seats):
            return False
        return True


class VehicleBuilder:
    """Vehicle Builder class"""

    vehicle = VehicleBuilt()

    def __init__(self, blueprint: VehicleBlueprint):
        self.blueprint = blueprint

    def build_engine(self):
        self.vehicle.set_engine(self.blueprint.engine)
        print(f'Engine for vehicle was installed')

    def build_transmission(self):
        self.vehicle.set_transmission(self.blueprint.transmission)
        print(f'Transmission for vehicle was installed')

    def build_wheels(self):
        self.vehicle.set_wheels(self.blueprint.wheels)
        print(f'Wheels for vehicle were installed')

    def build_seats(self):
        self.vehicle.set_seats(self.blueprint.seats)
        print(f'Seats for vehicle were installed')

    def export(self) -> VehicleBuilt | None:
        if self.vehicle.is_built:
            exported_vehicle, self.vehicle = self.vehicle, VehicleBuilt()
            print('Vehicle exported!')
            return exported_vehicle
        print('Vehicle is not built, cannot export!')
        return None
