# Sistema Avanzado de Gestión de Biblioteca

Este proyecto implementa un sistema de gestión de biblioteca en consola usando Programación Orientada a Objetos (POO). Modela los libros con la clase `Libro` y gestiona usuarios y préstamos con `BibliotecaServicio`.

## Objetivos
- Aplicar conceptos de POO para organizar la lógica de la biblioteca.
- Usar colecciones de Python (`dict`, `set`, `list`) para operaciones eficientes.
- Mantener la aplicación simple y enfocada en lógica (persistencia en memoria por defecto).

## Estructura del proyecto
- `main.py`: Interfaz de consola y punto de inicio (menú con recuadro, pausa y limpieza de pantalla).
- `modelos/libro.py`: Clase `Libro` (título, autor en tupla, categoría, ISBN).
- `modelos/usuario.py`: Clase `Usuario` (nombre, id_usuario, lista de `libros_prestados`).
- `servicios/biblioteca_servicio.py`: Clase `BibliotecaServicio` con la lógica de negocio (añadir/quitar libros, registrar/dar de baja usuarios, prestar/devolver libros, búsquedas).

## Arquitectura del Proyecto
El proyecto está organizado en una estructura de directorios que refleja la arquitectura por capas, garantizando una separación de responsabilidades clara y mantenible:

```
biblioteca_app/
│
├── modelos/
│   ├── libro.py
│   └── usuario.py
│
├── servicios/
│   └── biblioteca_servicio.py
│
└── main.py
```

- `modelos/`: Contiene las clases que representan las entidades del dominio (`Libro` y `Usuario`).
- `servicios/`: Aloja la lógica de negocio principal del sistema, encapsulada en la clase `BibliotecaServicio`.
- `main.py`: Es el punto de inicio de la aplicación, encargado de la interacción con el usuario a través de un menú en consola y de coordinar las operaciones con el servicio.

## Diseño y colecciones
- `dict` para mapear ISBN -> `Libro` (acceso eficiente por ISBN).
- `set` para almacenar IDs de usuario registrados y validar unicidad.
- `list` para la colección de `libros_prestados` en cada `Usuario`.

## Persistencia
La aplicación soporta persistencia sencilla mediante un archivo JSON llamado `biblioteca.json` ubicado en la misma carpeta de la aplicación.

- Al iniciar, la aplicación intentará cargar los datos desde `biblioteca.json` (libros y usuarios).
- Al salir (opción `[0] Guardar y Salir`), los datos actuales se guardan automáticamente en `biblioteca.json`.

## Uso (instrucciones)
1. Abra una terminal en la carpeta `biblioteca_app`.
2. Ejecute:

```bash
python main.py
```

3. Navegue con las opciones del menú (números entre corchetes). La opción para salir es `[0] Guardar y Salir`.

## Validaciones y comportamiento
- Al añadir un libro se verifica que el `ISBN` no exista ya en el catálogo.
- No se puede eliminar un libro que esté prestado.
- No se puede dar de baja a un usuario que tenga libros pendientes.
- Búsquedas: por `titulo`, `autor` o `categoria` (búsqueda case-insensitive y por substring).

## Interfaz y usabilidad
- Menú enmarcado con caracteres Unicode (`┌ ─ ┐ │ └ ┘`) para una mejor visualización.
- Opciones mostradas con formato: `[1] Añadir libro`.
- Tras cada acción se muestra `Presione Enter para continuar...` y se limpia la pantalla para reimprimir el menú.

## Pruebas sugeridas
- Registrar usuarios y prestar libros; verificar que no se puedan prestar libros ya prestados.
- Intentar eliminar un libro prestado y confirmar que se impide.
- Buscar libros por fragmento de título o autor.

## Autor
Proyecto elaborado por Gabo.