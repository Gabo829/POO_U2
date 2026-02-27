class Producto:
    """Representa un producto en el inventario.

    Atributos:
        id: identificador único (str)
        nombre: nombre del producto (str)
        cantidad: stock disponible (int)
        precio: precio unitario (float)
    """

    def __init__(self, id_, nombre, cantidad, precio):
        id_s = str(id_).strip()
        nombre_s = str(nombre).strip()
        if not id_s:
            raise ValueError("ID no puede estar vacío")
        if not nombre_s:
            raise ValueError("Nombre no puede estar vacío")
        try:
            cantidad_i = int(cantidad)
        except Exception:
            raise ValueError("Cantidad inválida: ingrese un número entero")
        try:
            precio_f = float(str(precio).replace(',', '.'))
        except Exception:
            raise ValueError("Precio inválido: use punto o coma como separador decimal")
        if cantidad_i < 0:
            raise ValueError("La cantidad no puede ser negativa")
        if precio_f < 0:
            raise ValueError("El precio no puede ser negativo")

        self._id = id_s
        self._nombre = nombre_s
        self._cantidad = cantidad_i
        self._precio = precio_f

    # Getters
    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def get_cantidad(self):
        return self._cantidad

    def get_precio(self):
        return self._precio

    # Setters
    def set_nombre(self, nombre):
        nombre_s = str(nombre).strip()
        if not nombre_s:
            raise ValueError("Nombre no puede estar vacío")
        self._nombre = nombre_s

    def set_cantidad(self, cantidad):
        try:
            cantidad_i = int(cantidad)
        except Exception:
            raise ValueError("Cantidad inválida: ingrese un número entero")
        if cantidad_i < 0:
            raise ValueError("La cantidad no puede ser negativa")
        self._cantidad = cantidad_i

    def set_precio(self, precio):
        try:
            precio_f = float(str(precio).replace(',', '.'))
        except Exception:
            raise ValueError("Precio inválido: use punto o coma como separador decimal")
        if precio_f < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = precio_f

    def to_dict(self):
        return {
            "id": self._id,
            "nombre": self._nombre,
            "cantidad": self._cantidad,
            "precio": self._precio,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["id"], d["nombre"], d["cantidad"], d["precio"])

    def __repr__(self):
        return f"Producto(id={self._id!r}, nombre={self._nombre!r}, cantidad={self._cantidad}, precio={self._precio})"
