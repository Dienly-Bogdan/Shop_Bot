class Client:
    id: int
    name: str
    address: dict
    number: str

class Product:
    id: int
    name: str
    quantity: int
    price: float
    guarantee: int

class Order:
    id: int
    id_product: int
    id_client: int
    data: str
