# sistema-inventario-libreria
## Evidencia de funcionamiento

El sistema incluye:
- [x] Clase Producto con todos los atributos requeridos
- [x] Clase Inventario con diccionarios para gestión eficiente
- [x] Operaciones CRUD completas
- [x] Base de datos SQLite con tabla productos
- [x] Interfaz de usuario en consola
- [x] Uso de colecciones para optimización

## Colecciones utilizadas

- **Diccionario principal**: Para acceso rápido por ID (O(1))
- **Índice de nombres**: Diccionario con sets para búsquedas eficientes
- **Listas**: Para devolver resultados de búsquedas

## Conexión a SQLite

Se implementó una clase Database que gestiona:
- Conexiones automáticas
- Creación de tablas
- Consultas parametrizadas
- Gestión de errores
