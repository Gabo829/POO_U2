from modelos.tarea import Tarea
from typing import List, Optional
import json
from pathlib import Path
import sys


class TareaServicio:
    """Servicio que encapsula la lógica de negocio para gestionar tareas.

    Añade persistencia simple a `tareas.json` en la carpeta raíz del paquete.
    """

    def __init__(self):
        self._tareas: List[Tarea] = []
        self._next_id = 1
        # Determinar ruta de datos:
        # - Si la aplicación está 'frozen' (empaquetada por PyInstaller),
        #   escribir junto al ejecutable (`sys.executable`).
        # - Si no está empaquetada, escribir en la carpeta del paquete.
        if getattr(sys, "frozen", False):
            # En modo onefile PyInstaller el proceso extrae a un directorio
            # temporal; `sys.executable` puede apuntar a ese ejecutable temporal.
            # Para garantizar que los datos se guarden junto al .exe original,
            # usamos `sys.argv[0]` que contiene la ruta al ejecutable lanzado.
            base_dir = Path(sys.argv[0]).resolve().parent
        else:
            base_dir = Path(__file__).resolve().parent.parent
        self._data_file = base_dir / "tareas.json"
        self._load()

    def _load(self):
        if not self._data_file.exists():
            # Si no existe archivo de datos, inicializamos con ejemplos
            self._tareas = [
                Tarea(1, "Comprar leche", False),
                Tarea(2, "Entregar informe", True),
            ]
            self._next_id = 3
            # Guardar para que el .exe tenga el archivo externo en la carpeta del ejecutable
            self._save()
            return
        try:
            with open(self._data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._tareas = [Tarea(d["id"], d["descripcion"], d.get("completado", False)) for d in data]
            if self._tareas:
                self._next_id = max(t.id for t in self._tareas) + 1
        except Exception:
            # Si falla la carga, empezamos vacíos
            self._tareas = []
            self._next_id = 1

    def _save(self):
        try:
            data = [{"id": t.id, "descripcion": t.descripcion, "completado": t.completado} for t in self._tareas]
            with open(self._data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def agregar(self, descripcion: str) -> Tarea:
        tarea = Tarea(self._next_id, descripcion)
        self._tareas.append(tarea)
        self._next_id += 1
        self._save()
        return tarea

    def eliminar_por_id(self, tarea_id: int) -> bool:
        for i, t in enumerate(self._tareas):
            if t.id == tarea_id:
                del self._tareas[i]
                self._save()
                return True
        return False

    def marcar_completada(self, tarea_id: int) -> bool:
        tarea = self.obtener_por_id(tarea_id)
        if tarea:
            tarea.marcar_completada()
            self._save()
            return True
        return False

    def desmarcar(self, tarea_id: int) -> bool:
        tarea = self.obtener_por_id(tarea_id)
        if tarea:
            tarea.desmarcar()
            self._save()
            return True
        return False

    def obtener_por_id(self, tarea_id: int) -> Optional[Tarea]:
        for t in self._tareas:
            if t.id == tarea_id:
                return t
        return None

    def listar(self) -> List[Tarea]:
        return list(self._tareas)
