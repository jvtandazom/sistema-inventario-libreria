# main.py
from models import Inventario

def mostrar_menu():
    """Muestra el menú principal"""
    print("\n=== SISTEMA DE GESTIÓN DE INVENTARIO - LIBRERÍA ===")
    print("1. Añadir nuevo producto")
    print("2. Eliminar producto")
    print("3. Actualizar producto")
    print("4. Buscar producto por nombre")
    print("5. Mostrar todos los productos")
    print("6. Salir")

def añadir_producto(inventario):
    """Interfaz para añadir un nuevo producto"""
    print("\n--- Añadir nuevo producto ---")
    
    nombre = input("Nombre del libro: ").strip()
    if not nombre:
        print("Error: El nombre no puede estar vacío.")
        return
        
    try:
        cantidad = int(input("Cantidad: "))
        if cantidad < 0:
            print("Error: La cantidad no puede ser negativa.")
            return
    except ValueError:
        print("Error: La cantidad debe ser un número entero.")
        return
        
    try:
        precio = float(input("Precio: "))
        if precio <= 0:
            print("Error: El precio debe ser mayor a cero.")
            return
    except ValueError:
        print("Error: El precio debe ser un número.")
        return
        
    categoria = input("Categoría (opcional): ").strip() or None
    autor = input("Autor (opcional): ").strip() or None
    isbn = input("ISBN (opcional): ").strip() or None
    
    inventario.añadir_producto(nombre, cantidad, precio, categoria, autor, isbn)

def eliminar_producto(inventario):
    """Interfaz para eliminar un producto"""
    print("\n--- Eliminar producto ---")
    
    try:
        id = int(input("ID del producto a eliminar: "))
    except ValueError:
        print("Error: El ID debe ser un número entero.")
        return
        
    inventario.eliminar_producto(id)

def actualizar_producto(inventario):
    """Interfaz para actualizar un producto"""
    print("\n--- Actualizar producto ---")
    
    try:
        id = int(input("ID del producto a actualizar: "))
    except ValueError:
        print("Error: El ID debe ser un número entero.")
        return
        
    # Verificar si el producto existe
    producto = inventario.obtener_por_id(id)
    if not producto:
        print(f"Error: No existe un producto con ID {id}.")
        return
        
    print("Deja en blanco los campos que no quieras modificar.")
    
    nombre = input(f"Nuevo nombre [{producto.get_nombre()}]: ").strip()
    nombre = nombre if nombre != "" else None
    
    try:
        cantidad_str = input(f"Nueva cantidad [{producto.get_cantidad()}]: ").strip()
        cantidad = int(cantidad_str) if cantidad_str != "" else None
        if cantidad is not None and cantidad < 0:
            print("Error: La cantidad no puede ser negativa.")
            return
    except ValueError:
        print("Error: La cantidad debe ser un número entero.")
        return
        
    try:
        precio_str = input(f"Nuevo precio [{producto.get_precio()}]: ").strip()
        precio = float(precio_str) if precio_str != "" else None
        if precio is not None and precio <= 0:
            print("Error: El precio debe ser mayor a cero.")
            return
    except ValueError:
        print("Error: El precio debe ser un número.")
        return
        
    categoria = input(f"Nueva categoría [{producto.get_categoria()}]: ").strip()
    categoria = categoria if categoria != "" else None
    
    autor = input(f"Nuevo autor [{producto.get_autor()}]: ").strip()
    autor = autor if autor != "" else None
    
    isbn = input(f"Nuevo ISBN [{producto.get_isbn()}]: ").strip()
    isbn = isbn if isbn != "" else None
    
    inventario.actualizar_producto(id, cantidad, precio, nombre, categoria, autor, isbn)

def buscar_producto(inventario):
    """Interfaz para buscar productos por nombre"""
    print("\n--- Buscar producto por nombre ---")
    
    nombre = input("Nombre a buscar: ").strip()
    if not nombre:
        print("Error: Debes introducir un nombre para buscar.")
        return
        
    resultados = inventario.buscar_por_nombre(nombre)
    
    if resultados:
        print(f"\nSe encontraron {len(resultados)} resultado(s):")
        for producto in resultados:
            print(producto)
    else:
        print("No se encontraron productos con ese nombre.")

def mostrar_todos_productos(inventario):
    """Interfaz para mostrar todos los productos"""
    print("\n--- Todos los productos en el inventario ---")
    
    productos = inventario.mostrar_todos()
    
    if productos:
        for producto in productos:
            print(producto)
        print(f"\nTotal: {len(productos)} producto(s)")
    else:
        print("El inventario está vacío.")

def main():
    """Función principal del programa"""
    inventario = Inventario()
    
    while True:
        mostrar_menu()
        opcion = input("\nSelecciona una opción (1-6): ").strip()
        
        if opcion == "1":
            añadir_producto(inventario)
        elif opcion == "2":
            eliminar_producto(inventario)
        elif opcion == "3":
            actualizar_producto(inventario)
        elif opcion == "4":
            buscar_producto(inventario)
        elif opcion == "5":
            mostrar_todos_productos(inventario)
        elif opcion == "6":
            print("¡Gracias por usar el sistema de gestión de inventario!")
            break
        else:
            print("Opción no válida. Por favor, selecciona una opción del 1 al 6.")
            
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()