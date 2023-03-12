import pyodbc
import dotenv
from datetime import datetime

driver = dotenv.get_key('.env', 'driver')
server = dotenv.get_key('.env', 'server')
database = dotenv.get_key('.env', 'database')
username = dotenv.get_key('.env', 'username')
password = dotenv.get_key('.env', 'password')

class Client:
    def __init__(self):
        self.conn = None
        self.cursor = None
    
    def connect(self):
        self.conn = pyodbc.connect(f"DRIVER={driver};SERVER={server};DATABASE={database};ENCRYPT=yes;UID={username};PWD={password};TrustServerCertificate=yes")
        self.cursor = self.conn.cursor()

    def exec_fetchone(self, query):
        self.connect()
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        self.close()
        return row

    def exec_fetchall(self, query):
        self.connect()
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.close()
        return rows

    def exec_commit(self, query):
        self.connect()
        self.cursor.execute(query)
        self.conn.commit()
        self.close()
    
    def close(self):
        self.cursor.close()
        self.conn.close()

    def add(self, obj):
        tablename = getattr(obj, '__tablename__') if hasattr(obj, '__tablename__') else None

        @staticmethod
        def sql_format(value):
            return f"{value}," if str(value).isdigit() else f"'{value}',"

        if tablename is None: 
            raise Exception("Object missing tablename attribute")

        values = ""
        for att in obj.__dict__:
            val = getattr(obj, att)
            if val is not None:
                values += sql_format(val)

        sql = f"INSERT INTO {tablename} VALUES ({values.rstrip(',')})"

        # logger.info(f"{datetime.now()} - add() - Executing SQL line: {sql}")

        self.exec_commit(sql)

    def remove(self, obj):
        tablename = getattr(obj, '__tablename__') if hasattr(obj, '__tablename__') else None

        if tablename is None: 
            raise Exception("Object missing tablename attribute")

        atts = vars(obj)
        field = list(atts.keys())[0]
        value = list(atts.values())[0]

        sql = f"DELETE FROM {tablename} WHERE {field}={value}"
        
        # logger.info(f"{datetime.now()} - remove() - Executing SQL line: {sql}")

        self.exec_commit(sql)
    
    def update(self, obj):
        tablename = getattr(obj, '__tablename__') if hasattr(obj, '__tablename__') else None

        if tablename is None: 
            raise Exception("Object missing tablename attribute")

        @staticmethod
        def sql_format(value):
            return f"{value}," if str(value).isdigit() else f"'{value}',"
        
        atts = vars(obj)
        field = list(atts.keys())[0]
        value = list(atts.values())[0]

        row = self.exec_fetchone(f"SELECT * FROM {tablename} WHERE {field}={value}")

        for k, v in atts.items():
            if getattr(row, k) != v:
                sql = f"UPDATE {tablename} SET {k}={sql_format(v).rstrip(',')} WHERE {field}={value}"

                # logger.info(f"{datetime.now()} - update() - Executing SQL line: {sql}")

                self.exec_commit(sql)
