
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from itertools import count

DATE_FORMAT = '%d/%m/%Y, %H:%M'


@dataclass
class Product:
    "General product class"
    name: str
    weight: float = 0.0
    price: float = 0.0
    id: int = field(default_factory=count(start=1).__next__)


@dataclass
class Device(Product):
    "Device product class"
    camera: bool = False
    battery: bool = False
    wi_fi: bool = False
    bluetooth: bool = False


@dataclass
class Check:
    "Check class"
    order_id: int
    price: float
    weight: float = 0.0
    date: str = datetime.now().strftime(DATE_FORMAT)


class AbstractPackage(ABC):
    "Abstract Package"

    weight: float = 0.0
    id_iter = count(start=1)

    def __init__(self) -> None:
        self.id = next(AbstractPackage.id_iter)

    @abstractmethod
    def remove(self, id: int) -> None:
        ...


class ProductPackage(AbstractPackage):
    "Product Package"

    def __init__(self) -> None:
        super().__init__()
        self.products: dict[int, Product] = {}

    def __len__(self) -> int:
        return len(self.products)

    def add(self, product: Product) -> None:
        self.products[product.id] = product

    def remove(self, id: int) -> None:
        if not self.products.get(id, None):
            raise KeyError(f'No product with id {id}')
        removed = self.products.pop(id)
        print(removed)

    @property
    def price_total(self) -> float:
        total = sum(p.price for p in self.products.values())
        return total

    @property
    def weight_total(self) -> float:
        total = sum(p.weight for p in self.products.values())
        return total


class CompositeOrder(AbstractPackage):
    """Composite Order Class"""

    check: Check | None

    def __init__(self) -> None:
        super().__init__()
        self.packages: dict[int, ProductPackage] = {}

    def __len__(self) -> int:
        return len(self.packages)

    def add(self, item: ProductPackage) -> None:
        self.packages[item.id] = item

    def remove(self, id: int) -> None:
        if not self.packages.get(id, None):
            raise KeyError(f'No package with id {id}')
        removed = self.packages.pop(id)
        print(removed)

    def checkout(self) -> Check:
        price_total = sum(p.price_total for p in self.packages.values())
        weight_total = sum(p.weight_total for p in self.packages.values())
        check = Check(order_id=self.id, price=price_total, weight=weight_total)
        print(f'Order total: ${price_total}')
        print(f'Items: {len(self)}')
        print(f'Date: {check.date}')
        return check
