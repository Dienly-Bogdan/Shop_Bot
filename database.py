import mysql.connector
from model import *


class Database:
    __connection = None
    @classmethod
    def open(cls,):
        if cls.__connection is None:
            cls.__connection = mysql.connector.connect(user=user,
                                                       password=password,
                                                       host=host,
                                                       database=database)

    @classmethod
    def close(cls):
        cls.__connection.close()
    @classmethod
    def query(cls, sql, values):
        cls.__connection.cursor().execute(sql, values)
        result = cls.__connection.cursor().fetchall()
        cls.__connection.commit()
        return result

class ClientTable:
    def get_by_id(cls, client: Client):
        sql = "SELECT "

    @classmethod
    def add(cls, client: Client):
        sql = "INSERT INTO Client (`name`, `address`, `number`) VALUE (%s, %s, %s);"
        values = [client.name, client.address, client.number]
        Database.query(sql, values)
