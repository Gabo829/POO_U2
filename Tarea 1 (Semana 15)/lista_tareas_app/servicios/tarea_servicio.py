from modelos.tarea import Tarea
from typing import List, Optional
import json
from pathlib import Path


class TareaServicio:
    """Servicio que encapsula la lógica de negocio para gestionar tareas.

    Añade persistencia simple a `tareas.json` en la carpeta raíz del paquete.
    """

    def __init__(self):
        self._tareas: List[Tarea] = []
        self._next_id = 1
        self._data_file = Path(__file__).resolve().parent.parent / "tareas.json"
        self._load()

    def _load(self):
        if not self._data_file.exists():
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
