from typing import Dict, List, Tuple, Any

class Client:
    def __init__(self):
        self.id: int = 0
        self.name: str = ""
        self.address: str = ""
        self.number: str = ""

class Product:
    def __init__(self):
        self.id: int = 0
        self.name: str = ""
        self.quantity: int = 0
        self.price: float = 0.0
        self.guarantee: int = 0

class Order:
    def __init__(self):
        self.id: int = 0
        self.id_client: int = 0
        self.date: str = ""
        self.total_price: float = 0.0
        self.status: str = ""