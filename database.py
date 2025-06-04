import mysql.connector
from model import *
from config import base
from typing import List, Tuple, Any

class Database:
    __connection = None
    
    @classmethod
    def open(cls, host=base["host"], user=base["user"], password=base["password"], database=base["database"]):
        if cls.__connection is None:
            cls.__connection = mysql.connector.connect(
                user=user,
                password=password,
                host=host,
                database=database
            )

    @classmethod
    def close(cls):
        if cls.__connection:
            cls.__connection.close()
            cls.__connection = None
            
    @classmethod
    def query(cls, sql: str, values: Tuple[Any, ...] = None, fetch: bool = False) -> List[Tuple] | None:
        cursor = cls.__connection.cursor()
        try:
            cursor.execute(sql, values)
            if fetch:
                result = cursor.fetchall()
            else:
                result = None
            cls.__connection.commit()
            return result
        finally:
            cursor.close()

class ClientTable:
    @classmethod
    def get_by_id(cls, client_id: int) -> Client | None:
        sql = "SELECT id, name, address, number FROM Client WHERE id = %s;"
        result = Database.query(sql, (client_id,), fetch=True)
        if result:
            client = Client()
            client.id = result[0][0]
            client.name = result[0][1]
            client.address = result[0][2]
            client.number = result[0][3]
            return client
        return None

    @classmethod
    def add(cls, client: Client) -> int:
        sql = "INSERT INTO Client (name, address, number) VALUES (%s, %s, %s);"
        values = (client.name, client.address, client.number)
        Database.query(sql, values)
        return Database.query("SELECT LAST_INSERT_ID();", fetch=True)[0][0]

    @classmethod
    def get_by_phone(cls, phone: str) -> Client | None:
        sql = "SELECT id, name, address, number FROM Client WHERE number = %s;"
        result = Database.query(sql, (phone,), fetch=True)
        if result:
            client = Client()
            client.id = result[0][0]
            client.name = result[0][1]
            client.address = result[0][2]
            client.number = result[0][3]
            return client
        return None

class ProductTable:
    @classmethod
    def get_all_products(cls) -> List[Product]:
        sql = "SELECT id, name, quantity, price, guarantee FROM Product;"
        results = Database.query(sql, fetch=True)
        products = []
        for row in results:
            product = Product()
            product.id = row[0]
            product.name = row[1]
            product.quantity = row[2]
            product.price = row[3]
            product.guarantee = row[4]
            products.append(product)
        return products

    @classmethod
    def get_by_id(cls, product_id: int) -> Product | None:
        sql = "SELECT id, name, quantity, price, guarantee FROM Product WHERE id = %s;"
        result = Database.query(sql, (product_id,), fetch=True)
        if result:
            product = Product()
            product.id = result[0][0]
            product.name = result[0][1]
            product.quantity = result[0][2]
            product.price = result[0][3]
            product.guarantee = result[0][4]
            return product
        return None

class OrderTable:
    @classmethod
    def create_order(cls, client_id: int, products: List[Tuple[int, int]]) -> int:
        total_price = 0
        for product_id, quantity in products:
            product = ProductTable.get_by_id(product_id)
            if product:
                total_price += product.price * quantity

        sql = "INSERT INTO `Order` (id_client, total_price, status) VALUES (%s, %s, 'pending');"
        Database.query(sql, (client_id, total_price))
        order_id = Database.query("SELECT LAST_INSERT_ID();", fetch=True)[0][0]
        
        for product_id, quantity in products:
            sql = "INSERT INTO OrderItem (order_id, product_id, quantity) VALUES (%s, %s, %s);"
            Database.query(sql, (order_id, product_id, quantity))
            
            # Update product quantity
            sql = "UPDATE Product SET quantity = quantity - %s WHERE id = %s;"
            Database.query(sql, (quantity, product_id))
        
        return order_id

    @classmethod
    def get_client_orders(cls, client_id: int) -> List[Order]:
        sql = """
        SELECT o.id, o.id_client, o.date, o.total_price, o.status 
        FROM `Order` o 
        WHERE o.id_client = %s;
        """
        results = Database.query(sql, (client_id,), fetch=True)
        orders = []
        for row in results:
            order = Order()
            order.id = row[0]
            order.id_client = row[1]
            order.date = row[2]
            order.total_price = row[3]
            order.status = row[4]
            orders.append(order)
        return orders

    @classmethod
    def get_order_items(cls, order_id: int) -> List[Tuple[Product, int]]:
        sql = """
        SELECT p.id, p.name, oi.quantity, p.price 
        FROM OrderItem oi
        JOIN Product p ON oi.product_id = p.id
        WHERE oi.order_id = %s;
        """
        results = Database.query(sql, (order_id,), fetch=True)
        items = []
        for row in results:
            product = Product()
            product.id = row[0]
            product.name = row[1]
            product.price = row[3]
            items.append((product, row[2]))
        return items