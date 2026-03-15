# Sistema Básico de Gestión de Garaje

Esta aplicación es una pequeña herramienta de escritorio (Tkinter) para registrar y gestionar vehículos que ingresan a un garaje. Sigue una arquitectura modular con `modelos`, `servicios`, `ui` y `main.py`.

## Objetivos
- Practicar POO y separación de responsabilidades.
- Implementar una interfaz gráfica básica con Tkinter.
- Persistir datos de vehículos en formato JSON.

## Estructura del proyecto
- `main.py`: Punto de entrada; carga/guarda datos y arranca la UI.
-- `modelos/vehiculo.py`: Clase `Vehiculo` (placa, marca, cilindraje, propietario).
- `servicios/garaje_servicio.py`: Lógica de negocio (añadir, listar, editar, eliminar, persistencia JSON).
- `ui/app_tkinter.py`: Interfaz gráfica construida con Tkinter (formulario y tabla).

Arquitectura en árbol:

```
Tarea 1 (Semana 13)
├──garaje_app/
│
├── modelos/
│   ├──__init__.py
│   └── vehiculo.py
├── servicios/
│   ├──__init__.py
│   └── garaje_servicio.py
├── ui/
│   ├──__init__.py
│   └── app_tkinter.py
├── main.py
└── garaje.json   # archivo de datos (se crea al guardar)
└── README.md
```

- ## Funcionalidades
- Agregar vehículo: llenar placa, marca, cilindraje y propietario.
- Editar un vehículo existente (seleccionar en la tabla y pulsar "Editar").
- Eliminar vehículo seleccionado.
- Limpiar formulario.
- Persistencia: carga desde `garaje.json` al iniciar y guarda al cerrar (archivo en la carpeta de la app).

## Validaciones y comportamiento
- Todos los campos del formulario son obligatorios; se mostrará una advertencia si están incompletos.
- La interfaz permite seleccionar filas en la tabla para editar o eliminar.
- Si se está en modo edición y se pulsa "Limpiar", la edición se cancela y el botón vuelve a "Agregar vehículo".

## Persistencia
- Archivo: `garaje.json` (ubicado junto a `main.py`).
- Al iniciar, la aplicación intenta cargar los datos existentes.
- Al cerrar la ventana, los datos se guardan automáticamente en `garaje.json`.

## Ejecución
1. Abrir una terminal en la carpeta `Tarea 1 (Semana 13)/garaje_app`.
2. Ejecutar:

```bash
python main.py
```

La ventana mostrará el formulario (Placa, Marca, Cilindraje, Propietario), los botones `Agregar vehículo`, `Limpiar`, `Editar`, `Eliminar` y una tabla con los vehículos registrados.

## Ejemplo de `garaje.json`
Al iniciar la carpeta `garaje_app` puede contener un archivo `garaje.json` con un arreglo de vehículos. Ejemplo:

```json
[
	{
		"placa": "ABC-123",
		"marca": "Toyota",
		"cilindraje": "1500",
		"propietario": "María Pérez"
	},
	{
		"placa": "XYZ-987",
		"marca": "Honda",
		"cilindraje": "1100",
		"propietario": "Juan Gómez"
	}
]
```

## Autor
Proyecto realizado por Gabo.

