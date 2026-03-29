class Tarea:
    """Modelo Tarea: mantiene id, descripcion y estado de completado."""

    def __init__(self, id: int, descripcion: str, completado: bool = False):
        self.id = id
        self.descripcion = descripcion
        self.completado = completado

    def marcar_completada(self):
        self.completado = True

    def desmarcar(self):
        self.completado = False

    def __repr__(self):
        return f"Tarea(id={self.id}, descripcion={self.descripcion!r}, completado={self.completado})"
