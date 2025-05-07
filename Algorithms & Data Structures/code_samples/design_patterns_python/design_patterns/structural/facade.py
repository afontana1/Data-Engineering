
from design_patterns.structural.composite import (Check, CompositeOrder,
                                                  Device, ProductPackage)


class Facade:
    """Facade class"""

    def __init__(self) -> None:
        self.order = CompositeOrder()
        self.device = Device(
            name='Special Device',
            weight=175,
            price=10000)
        self.package = ProductPackage()

    def do(self) -> Check:
        self.package.add(self.device)
        self.check=self.order.checkout()
        return self.check
