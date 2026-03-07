from abc import ABC, abstractmethod, abstractproperty
from dataclasses import asdict, dataclass


@dataclass
class DeviceState:
    volume: int = 50
    enabled: bool = False
    channel: int = 1


class Device(ABC):
    """Abstract Device class"""

    def __init__(self) -> None:
        self.state = DeviceState()

    @abstractmethod
    def toggle_power(self) -> None:
        ...

    def is_enabled(self) -> bool:
        return self.state.enabled

    def get_volume(self) -> int:
        return self.state.volume

    def set_volume(self, volume: int) -> None:
        self.state.volume = volume

    def get_channel(self) -> int:
        return self.state.channel

    def set_channel(self, channel: int) -> None:
        self.state.channel = channel


class Radio(Device):
    """Radio class"""

    def toggle_power(self) -> None:
        self.state.enabled = not self.state.enabled
        if self.state.enabled:
            print('Radio enabled!')
            return
        print('Radio disabled!')


class TV(Device):
    """TV class"""

    def toggle_power(self) -> None:
        self.state.enabled = not self.state.enabled
        if self.state.enabled:
            print('TV enabled!')
            return
        print('TV disabled!')


class BridgeRemote:
    """Bridge Remote class"""

    def __init__(self,
                 device: Device,
                 volume_increment: int = 10) -> None:
        self.device = device
        self.volume_increment = volume_increment

    def toggle_power(self) -> None:
        self.device.toggle_power()

    def volume_up(self) -> None:
        volume = self.device.get_volume()
        new_volume = volume + self.volume_increment
        self.device.set_volume(new_volume)

    def volume_down(self) -> None:
        volume = self.device.get_volume()
        new_volume = volume - self.volume_increment
        self.device.set_volume(new_volume)

    def channel_up(self) -> None:
        channel = self.device.get_channel()
        self.device.set_channel(channel + 1)

    def channel_down(self) -> None:
        channel = self.device.get_channel()
        self.device.set_channel(channel - 1)
