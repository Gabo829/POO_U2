# Lista de Tareas

Aplicación de escritorio (Tkinter) para gestionar una lista de tareas.

Esta entrega respeta la arquitectura modular vista en clase (`modelos`, `servicios`, `ui`) y añade persistencia en `tareas.json`.

## Objetivos
- Practicar separación de capas (modelo/servicio/ui).
- Implementar eventos de teclado y ratón en Tkinter (Enter y doble clic).
- Empaquetar la aplicación con PyInstaller.

## Estructura del proyecto
- `main.py` - Punto de entrada y orquestador.
- `modelos/tarea.py` - Clase `Tarea` (id, descripcion, completado).
- `servicios/tarea_servicio.py` - Lógica (agregar, listar, marcar, eliminar) + persistencia JSON.
- `ui/app_tkinter.py` - Interfaz gráfica y manejadores de eventos.
- `tareas.json` - Archivo de datos (se crea/actualiza automáticamente).

Árbol resumido:

```
Tarea 1 (Semana 15)
└── lista_tareas_app/
		├── main.py
		├── modelos/
		│   └── tarea.py
		├── servicios/
		│   └── tarea_servicio.py
		├── ui/
		│   └── app_tkinter.py
		├── tareas.json
		└── README.md
```

## Funcionamiento
- Añadir tarea: escribir la descripción y pulsar `Añadir Tarea` o `Enter` en el campo.
- Marcar completada: seleccionar y pulsar `Marcar Completada`, o hacer doble clic sobre la tarea.
- Eliminar: seleccionar y pulsar `Eliminar`.

Feedback visual: las tareas completadas muestran el emoji `✔️` y las pendientes `❌` al inicio de la línea.

## Persistencia
- Archivo: `tareas.json` (ubicado junto a `main.py`).
- Al iniciar, la aplicación carga `tareas.json` si existe.
- Al agregar/eliminar/marcar una tarea, se guarda automáticamente.

## Ejecución
1. Abrir una terminal en la carpeta `lista_tareas_app`.
2. Instalar dependencias (opcional si ya están instaladas):

```bash
pip install -r requirements.txt
```

3. Ejecutar la app:

```bash
python main.py
```

Al abrir la aplicación las tareas guardadas en `tareas.json` aparecerán automáticamente.

## Empaquetado con PyInstaller
1. Instalar PyInstaller: `pip install pyinstaller` o usar `requirements.txt`.
2. Generar ejecutable (sin consola) desde la carpeta `lista_tareas_app`:

```bash
python -m PyInstaller --noconsole --onefile --name ListaTareas main.py
```

Resultado: `dist/ListaTareas.exe`.

## Ejemplo de `tareas.json`
Al inicio este proyecto incluye dos tareas de ejemplo para que se muestren al abrir la app:

```json
[
	{
		"id": 1,
		"descripcion": "Comprar leche",
		"completado": false
	},
	{
		"id": 2,
		"descripcion": "Entregar informe",
		"completado": true
	}
]
```

## Autor
Proyecto realizado por Gabo.
