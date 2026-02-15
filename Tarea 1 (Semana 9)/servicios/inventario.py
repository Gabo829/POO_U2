from modelos.producto import Producto

class Inventario:
    """
    Clase encargada de la gestión de los productos en el sistema.
    """

    def __init__(self):
        """
        Inicializa el inventario con una lista vacía de productos.
        """
        self.__productos = []

    def añadir_producto(self, producto):
        """
        Añade un nuevo producto al inventario validando que el ID no esté repetido.
        """
        if any(p.id == producto.id for p in self.__productos):
            return False, f"Error: Ya existe un producto con el ID {producto.id}."
        
        self.__productos.append(producto)
        return True, "Producto añadido exitosamente."

    def eliminar_producto(self, id_producto):
        """
        Elimina un producto del inventario por su ID.
        """
        for i, producto in enumerate(self.__productos):
            if producto.id == id_producto:
                del self.__productos[i]
                return True, f"Producto con ID {id_producto} eliminado."
        return False, f"Error: No se encontró el producto con ID {id_producto}."

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        """
        Actualiza la cantidad o el precio de un producto por su ID.
        """
        for producto in self.__productos:
            if producto.id == id_producto:
                if cantidad is not None:
                    producto.cantidad = cantidad
                if precio is not None:
                    producto.precio = precio
                return True, f"Producto con ID {id_producto} actualizado."
        return False, f"Error: No se encontró el producto con ID {id_producto}."

    def buscar_por_nombre(self, nombre_parcial):
        """
        Busca productos por nombre permitiendo coincidencias parciales.
        """
        coincidencias = [p for p in self.__productos if nombre_parcial.lower() in p.nombre.lower()]
        return coincidencias

    def obtener_todos(self):
        """
        Retorna la lista de todos los productos registrados.
        """
        return self.__productos
