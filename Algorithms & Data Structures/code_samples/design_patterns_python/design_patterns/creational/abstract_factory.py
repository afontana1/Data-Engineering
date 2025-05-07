from abc import ABC
from enum import Enum


class Style(Enum):
    """Style Enum Class
    This can be an ABC-based class, but for sake of simplicity, this is an Enum.
    """
    victorian = "victorian"
    modern = "modern"
    art_deco = "art_deco"


class Furniture(ABC):
    """Abstract Furniture class"""

    def __init__(self, style: Style) -> None:
        self.style = style


class Chair(Furniture):
    """Chair Class"""
    pass


class Table(Furniture):
    """Table Class"""
    pass


class Sofa(Furniture):
    """Sofa Class"""
    pass


class AbstractFurnitureFactory(ABC):
    """Abstract Furniture Factory class"""

    def __init__(self, style: Style) -> None:
        self.style = style

    def make_chair(self) -> Chair:
        """Chair creation method """
        print(f'{self.style} style Chair created')
        return Chair(self.style)

    def make_table(self) -> Table:
        """Table creation method """
        print(f'{self.style} style Table created')
        return Table(self.style)

    def make_sofa(self) -> Sofa:
        """Sofa creation method """
        print(f'{self.style} style Sofa created')
        return Sofa(self.style)


class VictorianFurnitureFactory(AbstractFurnitureFactory):
    """Victorian Furniture Factory class"""

    def __init__(self) -> None:
        super().__init__(Style.victorian)


class ModernFurnitureFactory(AbstractFurnitureFactory):
    """Modern Furniture Factory class"""

    def __init__(self) -> None:
        super().__init__(Style.modern)


class ArtDecoFurnitureFactory(AbstractFurnitureFactory):
    """ArtDeco Furniture Factory class"""

    def __init__(self) -> None:
        super().__init__(Style.art_deco)


class AbstractFactory:
    """Abstract factory"""

    @staticmethod
    def new(style: str) -> AbstractFurnitureFactory:
        match style:
            case Style.victorian.value:
                return VictorianFurnitureFactory()
            case Style.modern.value:
                return ModernFurnitureFactory()
            case Style.art_deco.value:
                return ArtDecoFurnitureFactory()
            case _:
                raise Exception(
                    f'No factory that produces furniture in the {style} style')
