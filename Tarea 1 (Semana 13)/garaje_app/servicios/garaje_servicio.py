import json
from modelos.vehiculo import Vehiculo


class GarajeServicio:
    # Servicio que gestiona los vehículos del garaje.
    def __init__(self):
        self._vehiculos = []

    def agregar_vehiculo(self, vehiculo: Vehiculo):
        if not isinstance(vehiculo, Vehiculo):
            raise TypeError("Se esperaba una instancia de Vehiculo")
        self._vehiculos.append(vehiculo)

    def listar_vehiculos(self):
        return list(self._vehiculos)

    def limpiar(self):
        self._vehiculos.clear()

    def eliminar_vehiculo(self, index: int):
        # Elimina un vehículo por su índice en la lista interna.
        # Lanza IndexError si el índice no existe.
        try:
            del self._vehiculos[index]
        except IndexError:
            raise IndexError("Índice de vehículo fuera de rango")

    def actualizar_vehiculo(self, index: int, vehiculo: Vehiculo):
        # Actualiza el vehículo en la posición `index` con la nueva instancia.
        if not isinstance(vehiculo, Vehiculo):
            raise TypeError("Se esperaba una instancia de Vehiculo")
        try:
            self._vehiculos[index] = vehiculo
        except IndexError:
            raise IndexError("Índice de vehículo fuera de rango")

    def guardar_en_json(self, path: str):
        # Guarda la lista de vehículos en un archivo JSON.
        data = [v.to_dict() for v in self._vehiculos]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def cargar_desde_json(self, path: str):
        # Carga vehículos desde un archivo JSON. Si el archivo no existe, no hace nada.
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return
        except json.JSONDecodeError:
            # Archivo corrupto o vacío — ignorar carga
            return

        self._vehiculos = []
        for item in data:
            try:
                v = Vehiculo.from_dict(item)
            except Exception:
                continue
            self._vehiculos.append(v)
