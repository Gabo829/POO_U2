class Producto:
    """
    Representa la entidad principal del sistema de inventarios.
    """

    def __init__(self, id_producto, nombre, cantidad, precio):
        """
        Constructor de la clase Producto.
        
        :param id_producto: Identificador único del producto (int o str).
        :param nombre: Nombre descriptivo del producto.
        :param cantidad: Cantidad disponible en stock (int).
        :param precio: Precio unitario del producto (float).
        """
        self.__id = id_producto
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio = precio

    # Getters
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

    # Setters
    @id.setter
    def id(self, nuevo_id):
        self.__id = nuevo_id

    @nombre.setter
    def nombre(self, nuevo_nombre):
        self.__nombre = nuevo_nombre

    @cantidad.setter
    def cantidad(self, nueva_cantidad):
        if nueva_cantidad >= 0:
            self.__cantidad = nueva_cantidad
        else:
            raise ValueError("La cantidad no puede ser negativa.")

    @precio.setter
    def precio(self, nuevo_precio):
        if nuevo_precio >= 0:
            self.__precio = nuevo_precio
        else:
            raise ValueError("El precio no puede ser negativo.")

    def __str__(self):
        """Representación en cadena del producto."""
        return f"ID: {self.__id} | Nombre: {self.__nombre} | Cantidad: {self.__cantidad} | Precio: ${self.__precio:.2f}"
