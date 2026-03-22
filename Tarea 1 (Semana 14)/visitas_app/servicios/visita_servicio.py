import json
from typing import List
from modelos.visitante import Visitante


class VisitaServicio:
    # Servicio que gestiona la lista de visitantes en memoria.
    def __init__(self):
        self._visitantes: List[Visitante] = []
        # path por defecto (puede ser proporcionado por main)
        self._path = None

    def agregar(self, visitante: Visitante):
        if any(v.cedula == visitante.cedula for v in self._visitantes):
            raise ValueError("Cédula ya registrada")
        self._visitantes.append(visitante)

    def listar(self) -> List[Visitante]:
        return list(self._visitantes)

    def guardar_en_json(self, path: str = None):
        if path is None:
            path = self._path
        data = [v.to_dict() for v in self._visitantes]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def cargar_desde_json(self, path: str = None):
        if path is None:
            path = self._path
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return
        except json.JSONDecodeError:
            return

        self._visitantes = []
        for item in data:
            try:
                v = Visitante.from_dict(item)
            except Exception:
                continue
            self._visitantes.append(v)

    def eliminar_por_cedula(self, cedula: str):
        for i, v in enumerate(self._visitantes):
            if v.cedula == cedula:
                del self._visitantes[i]
                return
        raise ValueError("Cédula no encontrada")

    def actualizar_por_cedula(self, cedula_antigua: str, visitante_nuevo: Visitante):
        # Verificar existencia de la cédula antigua
        index = None
        for i, v in enumerate(self._visitantes):
            if v.cedula == cedula_antigua:
                index = i
                break
        if index is None:
            raise ValueError("Cédula a actualizar no encontrada")

        # Si la cédula cambia, asegurar que la nueva no esté repetida
        if visitante_nuevo.cedula != cedula_antigua:
            if any(v.cedula == visitante_nuevo.cedula for v in self._visitantes):
                raise ValueError("La nueva cédula ya está registrada")

        self._visitantes[index] = visitante_nuevo
