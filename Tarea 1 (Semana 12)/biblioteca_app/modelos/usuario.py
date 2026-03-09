class Usuario:
    """
    Representa a un usuario registrado en la biblioteca.
    """
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario
        # Requisito técnico: Utilizar lista para almacenar los libros prestados.
        self.libros_prestados = []

    def __str__(self):
        return f"Usuario: {self.nombre} (ID: {self.id_usuario}) | Libros prestados: {len(self.libros_prestados)}"