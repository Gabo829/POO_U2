class Vehiculo:
    # Clase que representa un vehículo del garaje.
    def __init__(self, placa: str, marca: str, propietario: str, cilindraje: str = ""):
        self.placa = placa.strip()
        self.marca = marca.strip()
        self.propietario = propietario.strip()
        self.cilindraje = str(cilindraje).strip()

    def to_tuple(self):
        return (self.placa, self.marca, self.cilindraje, self.propietario)

    def __repr__(self):
        return (
            f"Vehiculo(placa={self.placa!r}, marca={self.marca!r}, cilindraje={self.cilindraje!r}, "
            f"propietario={self.propietario!r})"
        )

    def to_dict(self):
        return {
            "placa": self.placa,
            "marca": self.marca,
            "cilindraje": self.cilindraje,
            "propietario": self.propietario,
        }

    @classmethod
    def from_dict(cls, data: dict):
        placa = data.get("placa", "")
        marca = data.get("marca", "")
        cilindraje = data.get("cilindraje", "")
        propietario = data.get("propietario", "")
        return cls(placa, marca, propietario, cilindraje)
