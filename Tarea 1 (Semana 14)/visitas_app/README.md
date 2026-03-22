# Sistema de Registro de Visitantes

Aplicación de escritorio (Tkinter) para gestionar el flujo de visitantes en una oficina. Sigue la arquitectura modular con `modelos`, `servicios`, `ui` y `main.py`.

## Objetivos
- Practicar POO y separación de responsabilidades.
- Implementar una interfaz gráfica básica con Tkinter.
- Persistir datos de visitantes en formato JSON.

## Estructura del proyecto
- `main.py`: Punto de entrada; carga/guarda datos y arranca la UI.
- `modelos/visitante.py`: Clase `Visitante` (cédula, nombre, motivo).
- `servicios/visita_servicio.py`: Lógica de negocio (agregar, listar, editar, eliminar, persistencia JSON).
- `ui/app_tkinter.py`: Interfaz gráfica construida con Tkinter (formulario y tabla).

Arquitectura en árbol:

```
Tarea 1 (Semana 14)
├──visitas_app/
│
├── modelos/
│   ├──__init__.py
│   └── visitante.py
├── servicios/
│   ├──__init__.py
│   └── visita_servicio.py
├── ui/
│   ├──__init__.py
│   └── app_tkinter.py
├── main.py
└── README.md
└── visitas.json   # archivo de datos (se crea al guardar)
```

## Funcionalidades
- Registrar un visitante: cédula, nombre completo y motivo.
- Editar un visitante existente (seleccionar en la tabla y pulsar "Editar").
- Eliminar visitante seleccionado.
- Limpiar formulario (cancela edición si estaba activa).
- Visualizar visitantes en una tabla (ttk.Treeview).

## Validaciones y comportamiento
- La cédula debe ser numérica y contener entre 7 y 18 dígitos (Esta configurada para ser global).
- `Nombre` y `Motivo` solo aceptan letras y espacios (no números ni signos).
- Todos los campos son obligatorios; se mostrará una advertencia si están incompletos.
- Si se está en modo edición y se pulsa "Limpiar", la edición se cancela y el botón vuelve a "Registrar".

## Persistencia
- Archivo: `visitas.json` (ubicado junto a `main.py`).
- Al iniciar, la aplicación intenta cargar los datos existentes.
- Al cerrar la ventana, los datos se guardan automáticamente en `visitas.json`.

## Ejecución
1. Abrir una terminal en la carpeta `Tarea 1 (Semana 14)/visitas_app`.
2. Ejecutar:

```bash
python main.py
```

La ventana mostrará el formulario (Cédula, Nombre completo, Motivo), los botones `Registrar`, `Limpiar`, `Editar`, `Eliminar` y una tabla con los visitantes registrados.

## Ejemplo de `visitas.json`
Ejemplo de contenido que esta en `visitas.json`:

```json
[
	{
		"cedula": "1234567890",
		"nombre": "María Pérez",
		"motivo": "Reunión"
	},
	{
		"cedula": "0987654321",
		"nombre": "Juan Gómez",
		"motivo": "Entrega"
	}
]
```

## Autor
Proyecto realizado por Gabo.
