# models.py
from database import Database

class Producto:
    def __init__(self, id, nombre, cantidad, precio, categoria=None, autor=None, isbn=None):
        self._id = id
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio
        self._categoria = categoria
        self._autor = autor
        self._isbn = isbn
        
    # Getters
    def get_id(self):
        return self._id
        
    def get_nombre(self):
        return self._nombre
        
    def get_cantidad(self):
        return self._cantidad
        
    def get_precio(self):
        return self._precio
        
    def get_categoria(self):
        return self._categoria
        
    def get_autor(self):
        return self._autor
        
    def get_isbn(self):
        return self._isbn
        
    # Setters
    def set_nombre(self, nombre):
        self._nombre = nombre
        
    def set_cantidad(self, cantidad):
        self._cantidad = cantidad
        
    def set_precio(self, precio):
        self._precio = precio
        
    def set_categoria(self, categoria):
        self._categoria = categoria
        
    def set_autor(self, autor):
        self._autor = autor
        
    def set_isbn(self, isbn):
        self._isbn = isbn
        
    def __str__(self):
        return (f"ID: {self._id}, Nombre: {self._nombre}, Cantidad: {self._cantidad}, "
                f"Precio: ${self._precio:.2f}, Categoría: {self._categoria}, "
                f"Autor: {self._autor}, ISBN: {self._isbn}")


class Inventario:
    def __init__(self):
        self._productos = {}  # Diccionario para acceso rápido por ID
        self._nombres_index = {}  # Diccionario para búsqueda por nombre
        self._db = Database()
        self._db.connect()
        self._db.create_table()
        self._cargar_desde_db()
        
    def _cargar_desde_db(self):
        """Carga todos los productos desde la base de datos"""
        query = "SELECT id, nombre, cantidad, precio, categoria, autor, isbn FROM productos"
        resultados = self._db.fetch_all(query)
        
        for row in resultados:
            id, nombre, cantidad, precio, categoria, autor, isbn = row
            producto = Producto(id, nombre, cantidad, precio, categoria, autor, isbn)
            self._productos[id] = producto
            
            # Indexar por nombre para búsquedas rápidas
            nombre_lower = nombre.lower()
            if nombre_lower not in self._nombres_index:
                self._nombres_index[nombre_lower] = set()
            self._nombres_index[nombre_lower].add(id)
            
    def añadir_producto(self, nombre, cantidad, precio, categoria=None, autor=None, isbn=None):
        """Añade un nuevo producto al inventario"""
        # Validar datos
        if not nombre or cantidad < 0 or precio <= 0:
            print("Error: Datos inválidos.")
            return False
            
        # Insertar en la base de datos
        query = """INSERT INTO productos (nombre, cantidad, precio, categoria, autor, isbn) 
                   VALUES (?, ?, ?, ?, ?, ?)"""
        params = (nombre, cantidad, precio, categoria, autor, isbn)
        
        if self._db.execute_query(query, params):
            # Obtener el ID del último registro insertado
            id = self._db.cursor.lastrowid
            
            # Crear el objeto Producto y añadirlo a las colecciones
            producto = Producto(id, nombre, cantidad, precio, categoria, autor, isbn)
            self._productos[id] = producto
            
            # Indexar por nombre para búsquedas rápidas
            nombre_lower = nombre.lower()
            if nombre_lower not in self._nombres_index:
                self._nombres_index[nombre_lower] = set()
            self._nombres_index[nombre_lower].add(id)
            
            print(f"Producto '{nombre}' añadido correctamente con ID {id}.")
            return True
        else:
            print("Error al añadir el producto a la base de datos.")
            return False
            
    def eliminar_producto(self, id):
        """Elimina un producto por ID"""
        if id not in self._productos:
            print(f"Error: No existe un producto con ID {id}.")
            return False
            
        # Eliminar de la base de datos
        query = "DELETE FROM productos WHERE id = ?"
        if self._db.execute_query(query, (id,)):
            # Eliminar de las colecciones en memoria
            producto = self._productos[id]
            nombre_lower = producto.get_nombre().lower()
            
            # Eliminar del índice de nombres
            if nombre_lower in self._nombres_index:
                self._nombres_index[nombre_lower].discard(id)
                if not self._nombres_index[nombre_lower]:  # Si está vacío, eliminar la entrada
                    del self._nombres_index[nombre_lower]
            
            # Eliminar del diccionario principal
            del self._productos[id]
            
            print(f"Producto con ID {id} eliminado correctamente.")
            return True
        else:
            print("Error al eliminar el producto de la base de datos.")
            return False
            
    def actualizar_producto(self, id, cantidad=None, precio=None, nombre=None, categoria=None, autor=None, isbn=None):
        """Actualiza los datos de un producto"""
        if id not in self._productos:
            print(f"Error: No existe un producto con ID {id}.")
            return False
            
        producto = self._productos[id]
        nombre_anterior = producto.get_nombre().lower()
        
        # Construir la consulta SQL dinámicamente
        campos = []
        params = []
        
        if nombre is not None and nombre != "":
            campos.append("nombre = ?")
            params.append(nombre)
            producto.set_nombre(nombre)
            
        if cantidad is not None and cantidad >= 0:
            campos.append("cantidad = ?")
            params.append(cantidad)
            producto.set_cantidad(cantidad)
            
        if precio is not None and precio > 0:
            campos.append("precio = ?")
            params.append(precio)
            producto.set_precio(precio)
            
        if categoria is not None:
            campos.append("categoria = ?")
            params.append(categoria)
            producto.set_categoria(categoria)
            
        if autor is not None:
            campos.append("autor = ?")
            params.append(autor)
            producto.set_autor(autor)
            
        if isbn is not None:
            campos.append("isbn = ?")
            params.append(isbn)
            producto.set_isbn(isbn)
            
        if not campos:
            print("No se proporcionaron campos para actualizar.")
            return False
            
        # Añadir el ID al final de los parámetros
        params.append(id)
        
        # Ejecutar la consulta
        query = f"UPDATE productos SET {', '.join(campos)} WHERE id = ?"
        if self._db.execute_query(query, params):
            # Actualizar el índice de nombres si cambió el nombre
            if nombre is not None and nombre != "":
                nombre_nuevo = nombre.lower()
                
                # Eliminar del índice antiguo
                if nombre_anterior in self._nombres_index:
                    self._nombres_index[nombre_anterior].discard(id)
                    if not self._nombres_index[nombre_anterior]:
                        del self._nombres_index[nombre_anterior]
                
                # Añadir al nuevo índice
                if nombre_nuevo not in self._nombres_index:
                    self._nombres_index[nombre_nuevo] = set()
                self._nombres_index[nombre_nuevo].add(id)
                
            print(f"Producto con ID {id} actualizado correctamente.")
            return True
        else:
            print("Error al actualizar el producto en la base de datos.")
            return False
            
    def buscar_por_nombre(self, nombre):
        """Busca productos por nombre (búsqueda parcial case-insensitive)"""
        nombre_lower = nombre.lower()
        resultados = []
        
        # Buscar en el índice de nombres
        for nombre_index, ids in self._nombres_index.items():
            if nombre_lower in nombre_index:
                for id in ids:
                    resultados.append(self._productos[id])
                    
        return resultados
        
    def obtener_por_id(self, id):
        """Obtiene un producto por su ID"""
        return self._productos.get(id)
        
    def mostrar_todos(self):
        """Devuelve todos los productos del inventario"""
        return list(self._productos.values())
        
    def __del__(self):
        """Destructor para cerrar la conexión a la base de datos"""
        if hasattr(self, '_db'):
            self._db.disconnect()