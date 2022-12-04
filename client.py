import pyodbc
import dotenv

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

    def execute(self, query):
        self.cursor.execute(query)
    
    def close(self):
        self.cursor.close()
        self.conn.close()
