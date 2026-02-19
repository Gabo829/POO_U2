# Sistema de Gestión de Inventarios V2
Proyecto de ejemplo para la asignatura de Programación Orientada a Objetos que implementa un sistema de gestión de inventarios en consola. Esta versión mejora la entrega previa añadiendo persistencia en archivos y manejo robusto de excepciones.

Objetivo
- Guardar y recuperar productos desde un archivo (`inventario.txt`) y notificar al usuario sobre fallos o éxitos en operaciones de E/S.

## Estructura del proyecto
- `main.py`: Interfaz de consola (entrada/salida) y punto de arranque.
- `modelos/producto.py`: Clase `Producto` con validaciones y métodos de serialización (`to_line` / `from_line`).
- `servicios/inventario.py`: Clase `Inventario` que carga/guarda el inventario en `inventario.txt`, con manejo de excepciones (`PermissionError`, `FileNotFoundError`, parseo inválido) y guardado atómico.
- `inventario.txt`: Archivo creado automáticamente en la carpeta del proyecto para persistir los productos.

## Comportamiento de persistencia
- Al iniciar, `Inventario` intentará cargar `inventario.txt`. Si el archivo no existe lo crea.
- Cada operación que modifica el inventario (`añadir_producto`, `eliminar_producto`, `actualizar_producto`) intenta persistir los cambios en disco. El guardado se hace en un archivo temporal y luego se reemplaza el original para reducir el riesgo de corrupción.
- Mensajes sobre el resultado de las operaciones de archivo están disponibles y se muestran en la interfaz.

## Manejo de excepciones y casos especiales
- Se manejan `PermissionError` y errores generales de E/S con mensajes claros.
- Si alguna línea en `inventario.txt` no respeta el formato esperado, se ignora y se aumenta el contador de líneas ignoradas; el usuario recibe un resumen al cargar.

## Formato del archivo
- Cada producto se almacena en una línea con el formato: `id|nombre|cantidad|precio`.

## Instrucciones de Uso
1.  Coloque el archivo `main.py` en la carpeta raíz de sus proyectos.
2.  Ejecute el programa:
    ```bash
    python main.py
    ```
3.  Navegue por el menú usando los números indicados.

## Pruebas sugeridas
- Probar agregar/editar/eliminar productos y verificar que `inventario.txt` se actualice.
- Simular falta de permisos cambiando permisos del archivo para verificar los mensajes de error.
- Introducir líneas corruptas manualmente en `inventario.txt` y reiniciar el programa para verificar que se informen líneas ignoradas.

## Autor
Proyecto elaborado por Gabo.