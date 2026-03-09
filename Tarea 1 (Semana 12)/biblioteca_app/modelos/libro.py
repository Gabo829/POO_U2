class Libro:
    """
    Representa un libro dentro del sistema de biblioteca.
    """
    def __init__(self, titulo, autor, categoria, isbn):
        # Requisito técnico: Título y autor almacenados como una tupla (inmutables).
        self.info = (titulo, autor)
        self.categoria = categoria
        self.isbn = isbn

    @property
    def titulo(self):
        return self.info[0]

    @property
    def autor(self):
        return self.info[1]

    def __str__(self):
        return f"Libro: {self.titulo} | Autor: {self.autor} | Categoría: {self.categoria} | ISBN: {self.isbn}"