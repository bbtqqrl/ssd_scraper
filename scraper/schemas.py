from dataclasses import dataclass

@dataclass
class Product:
    id: int
    brand: str
    title: str
    price: float
    href: str