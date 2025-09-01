# database.py
import sqlite3
import os

class Database:
    def __init__(self, db_name="inventario.db"):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Establece conexión con la base de datos"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            return True
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            return False
            
    def disconnect(self):
        """Cierra la conexión con la base de datos"""
        if self.connection:
            self.connection.close()
            
    def create_table(self):
        """Crea la tabla de productos si no existe"""
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    cantidad INTEGER NOT NULL,
                    precio REAL NOT NULL,
                    categoria TEXT,
                    autor TEXT,
                    isbn TEXT UNIQUE
                )
            ''')
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {e}")
            return False
            
    def execute_query(self, query, params=None):
        """Ejecuta una consulta SQL"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return False
            
    def fetch_all(self, query, params=None):
        """Ejecuta una consulta y devuelve todos los resultados"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener datos: {e}")
            return []