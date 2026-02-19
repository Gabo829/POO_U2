class Producto:
    """
    Representa la entidad Producto y provee helpers para serializar
    y deserializar a una línea de archivo.
    """

    def __init__(self, id_producto, nombre, cantidad, precio):
        self.__id = id_producto
        self.__nombre = nombre
        self.__cantidad = int(cantidad)
        self.__precio = float(precio)

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @property
    def cantidad(self):
        return self.__cantidad

    @property
    def precio(self):
        return self.__precio

    @id.setter
    def id(self, nuevo_id):
        self.__id = nuevo_id

    @nombre.setter
    def nombre(self, nuevo_nombre):
        self.__nombre = nuevo_nombre

    @cantidad.setter
    def cantidad(self, nueva_cantidad):
        nueva = int(nueva_cantidad)
        if nueva >= 0:
            self.__cantidad = nueva
        else:
            raise ValueError("La cantidad no puede ser negativa.")

    @precio.setter
    def precio(self, nuevo_precio):
        nuevo = float(nuevo_precio)
        if nuevo >= 0:
            self.__precio = nuevo
        else:
            raise ValueError("El precio no puede ser negativo.")

    def __str__(self):
        return f"ID: {self.__id} | Nombre: {self.__nombre} | Cantidad: {self.__cantidad} | Precio: ${self.__precio:.2f}"

    def to_line(self):
        """Serializa el producto a una línea para almacenar en archivo.

        Formato: id|nombre|cantidad|precio\n

        """
        safe_nombre = str(self.__nombre).replace('|', '/')
        return f"{self.__id}|{safe_nombre}|{self.__cantidad}|{self.__precio}\n"

    @classmethod
    def from_line(cls, line):
        """Crea un Producto a partir de una línea serializada.

        Lanza ValueError si la línea no tiene el formato esperado.
        """
        parts = line.strip().split('|')
        if len(parts) != 4:
            raise ValueError("Línea de producto con formato inválido")
        id_p, nombre, cantidad, precio = parts
        return cls(id_p, nombre, int(cantidad), float(precio))
