from dataclasses import dataclass

@dataclass
class Visitante:
    cedula: str
    nombre: str
    motivo: str

    def to_dict(self) -> dict:
        return {
            "cedula": self.cedula,
            "nombre": self.nombre,
            "motivo": self.motivo,
        }

    @staticmethod
    def from_dict(data: dict):
        return Visitante(
            cedula=str(data.get("cedula", "")),
            nombre=str(data.get("nombre", "")),
            motivo=str(data.get("motivo", "")),
        )
