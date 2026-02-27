# Sistema Avanzado de Gestión de Inventario
Este proyecto implementa un sistema de gestión de inventarios en consola usando Programación Orientada a Objetos (POO). Modela los productos con la clase `Producto` y gestiona la colección de productos con la clase `Inventario`.

## Objetivos
- Aplicar conceptos de POO para organizar la lógica del inventario.
- Usar colecciones de Python (diccionarios, listas) para operaciones eficientes.
- Persistir el inventario en disco (archivo JSON) para almacenamiento entre ejecuciones.

## Estructura del proyecto
- `main.py`: Interfaz de consola y punto de inicio.
- `modelos/producto.py`: Clase `Producto` con getters/setters y serialización (`to_dict` / `from_dict`).
- `servicios/inventario.py`: Clase `Inventario` que mantiene `dict[id -> Producto]`, operaciones CRUD y persistencia en `inventario.json`.

## Colecciones y razones de diseño
- Diccionario (`dict`): `Inventario._productos` mapea `id -> Producto`. Permite accesos, inserciones y eliminaciones promedio O(1) por ID.
- Lista (`list`): Se usa temporalmente para producir una representación serializable (lista de diccionarios) al guardar en JSON y para iteraciones ordenadas al mostrar todos los productos.

## Persistencia (almacenamiento en archivos)
- Archivo: `inventario.json` (formato JSON, UTF-8).
- Métodos: `Inventario.save_to_file(path)` y `Inventario.load_from_file(path)` realizan la serialización/deserialización.
- Formato de almacenamiento: una lista de objetos JSON con las claves `id`, `nombre`, `cantidad` y `precio`.

Ejemplo de contenido de `inventario.json`:

```
[
  {
    "id": "1",
    "nombre": "Pera",
    "cantidad": 1,
    "precio": 0.5
  },
  {
    "id": "2",
    "nombre": "Manzana",
    "cantidad": 1,
    "precio": 0.5
  }
]
```

## Instrucciones de Uso
1.  Coloque el archivo `main.py` en la carpeta raíz de sus proyectos.
2.  Ejecute el programa:
    ```bash
    python main.py
    ```
3.  Navegue por el menú usando los números indicados.

## Buenas prácticas y notas de robustez
- Los IDs deben ser únicos; `Inventario.add_product` lanza `ValueError` si el `id` ya existe.
- Al actualizar o eliminar por `id` se lanza `KeyError` si el `id` no existe (capturado en `main.py`).
- La persistencia usa JSON para legibilidad y compatibilidad; puede adaptarse a CSV o texto plano si se necesita.

## Validaciones implementadas (entrada y errores)
- ID y Nombre: no pueden quedar vacíos. El constructor y los setters en `Producto` validan esto y lanzan `ValueError` si se viola.
- Cantidad: debe ser un entero; no se permiten valores negativos. Validado en `main.py`, en `Producto` y en los métodos de `Inventario`.
- Precio: admite separador decimal con coma o punto (ej. `0,5` o `0.5`); no se permiten valores negativos. Las conversiones inválidas generan `ValueError`.
- Mensajes de error: todos los mensajes visibles al usuario están en español y amigables (por ejemplo: "Precio inválido: use punto o coma como separador decimal").

## Detalles de la interfaz y usabilidad
- Menú decorado en consola con bordes Unicode para mejorar la presentación.
- Al actualizar cantidad o precio puede dejarse el campo vacío para mantener el valor actual.
- Se limpian la pantalla entre interacciones para una experiencia más limpia en la terminal.

## Pruebas sugeridas
- Añadir varios productos y verificar que aparecen en `inventario.json`.
- Reiniciar la aplicación y comprobar que los productos se cargan correctamente.
- Probar búsquedas por fragmento de `nombre` (ej. "lap") y verificar resultados.
- Intentar añadir un producto con `id` existente y confirmar que se muestra el error.

## Autor
Proyecto elaborado por Gabo.