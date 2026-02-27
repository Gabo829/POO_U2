import json
from pathlib import Path
from typing import Dict, List

from modelos.producto import Producto


class Inventario:
    """Gestiona una colección de productos usando un diccionario para acceso rápido por ID."""

    def __init__(self):
        self._productos: Dict[str, Producto] = {}

    def add_product(self, producto: Producto):
        pid = producto.get_id()
        if pid in self._productos:
            raise ValueError(f"El producto con ID {pid} ya existe.")
        self._productos[pid] = producto

    def remove_product(self, product_id: str):
        return self._productos.pop(str(product_id), None)

    def update_quantity(self, product_id: str, cantidad: int):
        pid = str(product_id)
        if pid not in self._productos:
            raise KeyError(f"Producto {pid} no encontrado")
        cantidad_i = int(cantidad)
        if cantidad_i < 0:
            raise ValueError("La cantidad no puede ser negativa")
        self._productos[pid].set_cantidad(cantidad_i)

    def update_price(self, product_id: str, precio: float):
        pid = str(product_id)
        if pid not in self._productos:
            raise KeyError(f"Producto {pid} no encontrado")
        precio_f = float(precio)
        if precio_f < 0:
            raise ValueError("El precio no puede ser negativo")
        self._productos[pid].set_precio(precio_f)

    def search_by_name(self, nombre: str) -> List[Producto]:
        q = nombre.strip().lower()
        return [p for p in self._productos.values() if q in p.get_nombre().lower()]

    def list_all(self) -> List[Producto]:
        return list(self._productos.values())

    def get_product(self, product_id: str) -> Producto:
        return self._productos.get(str(product_id))

    # Almacenamiento en archivo (JSON)
    def save_to_file(self, path: str):
        p = Path(path)
        data = [prod.to_dict() for prod in self._productos.values()]
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def load_from_file(self, path: str):
        p = Path(path)
        if not p.exists():
            return
        raw = p.read_text(encoding="utf-8")
        data = json.loads(raw)
        self._productos = {str(d["id"]): Producto.from_dict(d) for d in data}
