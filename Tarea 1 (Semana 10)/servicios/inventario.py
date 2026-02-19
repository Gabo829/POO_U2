import os
from modelos.producto import Producto


class Inventario:
    """
    Gestión de inventario con persistencia en archivo `inventario.txt`.
    Todas las modificaciones (añadir/actualizar/eliminar) intentan guardarse
    inmediatamente en el archivo y se devuelve información sobre el éxito
    o fracaso de la operación.
    """

    def __init__(self, archivo=None):
        # Ubicación por defecto: archivo en la carpeta raíz de la tarea
        base_dir = os.path.dirname(os.path.abspath(__file__))
        proyecto_dir = os.path.normpath(os.path.join(base_dir, '..'))
        self.archivo = archivo or os.path.join(proyecto_dir, 'inventario.txt')
        self.__productos = []
        self.last_file_message = ''
        self._cargar_desde_archivo()

    def _cargar_desde_archivo(self):
        """Carga productos desde `self.archivo`. Crea el archivo si no existe.

        Guarda en `self.last_file_message` el resultado de la operación para
        que la interfaz pueda notificar al usuario.
        """
        try:
            # Asegurar la existencia del directorio
            os.makedirs(os.path.dirname(self.archivo), exist_ok=True)
            if not os.path.exists(self.archivo):
                # Crear archivo vacío
                with open(self.archivo, 'w', encoding='utf-8'):
                    pass
                self.last_file_message = f"Archivo de inventario creado en: {self.archivo}"
                return

            with open(self.archivo, 'r', encoding='utf-8') as f:
                lineas = f.readlines()

            cargados = 0
            errores = 0
            for i, linea in enumerate(lineas, start=1):
                if not linea.strip():
                    continue
                try:
                    p = Producto.from_line(linea)
                    self.__productos.append(p)
                    cargados += 1
                except Exception:
                    errores += 1
            self.last_file_message = f"Carga completa: {cargados} productos cargados. {errores} líneas ignoradas."

        except PermissionError:
            self.last_file_message = f"Error: Sin permiso para leer/crear el archivo {self.archivo}."
        except FileNotFoundError:
            # En teoría no debe ocurrir por la creación previa, pero lo manejamos
            try:
                with open(self.archivo, 'w', encoding='utf-8'):
                    pass
                self.last_file_message = f"Archivo de inventario creado en: {self.archivo}"
            except Exception:
                self.last_file_message = f"Error crítico al crear el archivo {self.archivo}."
        except Exception as e:
            self.last_file_message = f"Error al cargar inventario: {e}"

    def _guardar_en_archivo(self):
        """Guarda el estado completo del inventario en el archivo.

        Lanza PermissionError o excepciones de E/S en caso de fallo.
        """
        # Escribir en un archivo temporal y luego renombrarlo para evitar corrupciones
        tmp = self.archivo + '.tmp'
        try:
            with open(tmp, 'w', encoding='utf-8') as f:
                for p in self.__productos:
                    f.write(p.to_line())
            os.replace(tmp, self.archivo)
            return True, f"Cambios guardados en {self.archivo}."
        except PermissionError:
            return False, f"Error: Sin permiso para escribir en {self.archivo}."
        except Exception as e:
            # Intenta limpiar archivo temporal si existe
            try:
                if os.path.exists(tmp):
                    os.remove(tmp)
            except Exception:
                pass
            return False, f"Error al guardar inventario: {e}"

    def añadir_producto(self, producto):
        if any(p.id == producto.id for p in self.__productos):
            return False, f"Error: Ya existe un producto con el ID {producto.id}."

        self.__productos.append(producto)
        ok, msg = self._guardar_en_archivo()
        if ok:
            return True, f"Producto añadido y {msg}"
        else:
            return False, f"Producto añadido en memoria, pero {msg}"

    def eliminar_producto(self, id_producto):
        for i, producto in enumerate(self.__productos):
            if producto.id == id_producto:
                del self.__productos[i]
                ok, msg = self._guardar_en_archivo()
                if ok:
                    return True, f"Producto con ID {id_producto} eliminado. {msg}"
                else:
                    return False, f"Producto eliminado en memoria, pero {msg}"
        return False, f"Error: No se encontró el producto con ID {id_producto}."

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        for producto in self.__productos:
            if producto.id == id_producto:
                try:
                    if cantidad is not None:
                        producto.cantidad = cantidad
                    if precio is not None:
                        producto.precio = precio
                except ValueError as e:
                    return False, f"Error en datos: {e}"

                ok, msg = self._guardar_en_archivo()
                if ok:
                    return True, f"Producto con ID {id_producto} actualizado. {msg}"
                else:
                    return False, f"Producto actualizado en memoria, pero {msg}"
        return False, f"Error: No se encontró el producto con ID {id_producto}."

    def buscar_por_nombre(self, nombre_parcial):
        return [p for p in self.__productos if nombre_parcial.lower() in p.nombre.lower()]

    def obtener_todos(self):
        return self.__productos
