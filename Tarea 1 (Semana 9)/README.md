# Sistema de Gestión de Inventarios

Este proyecto es una aplicación sencilla en Python para gestionar el inventario de una tienda. Permite agregar, actualizar, eliminar y buscar productos utilizando conceptos de Programación Orientada a Objetos y una estructura modular para facilitar su mantenimiento y expansión.

## Requisitos principales

- Clase `Producto` con ID único, nombre, cantidad y precio; usa validaciones y propiedades para acceder a los atributos.
- Clase `Inventario` que administra una colección de `Producto` y ofrece operaciones para añadir (verificando la unicidad del ID), eliminar por ID, actualizar cantidad o precio, buscar por nombre (coincidencias parciales) y listar todos los productos.
- Interfaz de consola (`main.py`) con un menú interactivo que valida entradas y coordina las acciones sobre el inventario.
- Organización en módulos (`modelos/`, `servicios/`) para separar entidades y lógica de negocio.

## Estructura del Sistema
La arquitectura del proyecto se basa en una estructura modular, dividiendo las responsabilidades en tres componentes principales:

```
sistema_inventario/
├── modelos/
│   ├── __init__.py
│   └── producto.py
├── servicios/
│   ├── __init__.py
│   └── inventario.py
└── main.py
```

- `modelos/`: define la entidad `Producto`.
- `servicios/`: contiene la lógica de negocio en la clase `Inventario`.
- `main.py`: punto de entrada que gestiona la interacción con el usuario.

## Diseño y consideraciones

- `Producto` usa atributos privados y propiedades; valida que cantidad y precio no sean negativos y proporciona una representación legible.
- `Inventario` mantiene una lista interna de productos y devuelve resultados claros (éxito/mensaje) en sus operaciones.
- Se añadieron validaciones de entrada y comentarios en el código para mejorar la robustez y la comprensión.
- La modularidad y la legibilidad facilitan futuras mejoras, como persistencia de datos o una interfaz gráfica.

## Conclusión

El sistema cumple su objetivo como una base sencilla y bien estructurada para la gestión de inventarios, adecuada para ampliaciones posteriores.
