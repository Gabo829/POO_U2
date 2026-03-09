import json
from modelos.libro import Libro
from modelos.usuario import Usuario

class BibliotecaServicio:
    """
    Gestiona la lógica del sistema de biblioteca digital.
    """
    def __init__(self):
        # Requisito técnico: Utilizar diccionario para almacenar los libros disponibles.
        # Clave: ISBN, Valor: Objeto Libro
        self.libros_disponibles = {}
        
        # Requisito técnico: Utilizar conjunto (set) para gestionar IDs únicos de usuarios.
        self.ids_usuarios = set()
        
        # Diccionario para almacenar objetos Usuario (Clave: ID, Valor: Objeto Usuario)
        self.usuarios_registrados = {}

    def añadir_libro(self, titulo, autor, categoria, isbn):
        """Añade un nuevo libro al catálogo."""
        if isbn in self.libros_disponibles:
            return False, f"El libro con ISBN {isbn} ya existe."
        
        nuevo_libro = Libro(titulo, autor, categoria, isbn)
        self.libros_disponibles[isbn] = nuevo_libro
        return True, f"Libro '{titulo}' añadido correctamente."

    def quitar_libro(self, isbn):
        """Elimina un libro del catálogo si no está prestado."""
        if isbn not in self.libros_disponibles:
            return False, "El libro no se encuentra en el catálogo."
        
        # Verificar si el libro está prestado a algún usuario
        for usuario in self.usuarios_registrados.values():
            if any(libro.isbn == isbn for libro in usuario.libros_prestados):
                return False, "No se puede eliminar un libro que está actualmente prestado."
        
        del self.libros_disponibles[isbn]
        return True, "Libro eliminado correctamente."

    def registrar_usuario(self, nombre, id_usuario):
        """Registra un nuevo usuario en el sistema."""
        if id_usuario in self.ids_usuarios:
            return False, f"El ID de usuario {id_usuario} ya está registrado."
        
        nuevo_usuario = Usuario(nombre, id_usuario)
        self.usuarios_registrados[id_usuario] = nuevo_usuario
        self.ids_usuarios.add(id_usuario)
        return True, f"Usuario '{nombre}' registrado correctamente."

    def dar_de_baja_usuario(self, id_usuario):
        """Elimina un usuario si no tiene libros pendientes."""
        if id_usuario not in self.usuarios_registrados:
            return False, "El usuario no existe."
        
        usuario = self.usuarios_registrados[id_usuario]
        if usuario.libros_prestados:
            return False, "No se puede dar de baja a un usuario con libros pendientes de devolución."
        
        del self.usuarios_registrados[id_usuario]
        self.ids_usuarios.remove(id_usuario)
        return True, "Usuario dado de baja correctamente."

    def prestar_libro(self, isbn, id_usuario):
        """Asigna un libro a un usuario."""
        if isbn not in self.libros_disponibles:
            return False, "El libro no está disponible en el catálogo."
        
        if id_usuario not in self.usuarios_registrados:
            return False, "El usuario no está registrado."
        
        # Verificar si el libro ya está prestado a alguien
        for u in self.usuarios_registrados.values():
            if any(libro.isbn == isbn for libro in u.libros_prestados):
                return False, "El libro ya se encuentra prestado a otro usuario."
        
        libro = self.libros_disponibles[isbn]
        usuario = self.usuarios_registrados[id_usuario]
        usuario.libros_prestados.append(libro)
        return True, f"Libro '{libro.titulo}' prestado a {usuario.nombre}."

    def devolver_libro(self, isbn, id_usuario):
        """Registra la devolución de un libro por parte de un usuario."""
        if id_usuario not in self.usuarios_registrados:
            return False, "El usuario no está registrado."
        
        usuario = self.usuarios_registrados[id_usuario]
        libro_encontrado = None
        for libro in usuario.libros_prestados:
            if libro.isbn == isbn:
                libro_encontrado = libro
                break
        
        if not libro_encontrado:
            return False, "El usuario no tiene este libro en préstamo."
        
        usuario.libros_prestados.remove(libro_encontrado)
        return True, f"Libro '{libro_encontrado.titulo}' devuelto correctamente."

    def buscar_libros(self, criterio, valor):
        """Busca libros por título, autor o categoría."""
        resultados = []
        valor = valor.lower()
        
        for libro in self.libros_disponibles.values():
            if criterio == "titulo" and valor in libro.titulo.lower():
                resultados.append(libro)
            elif criterio == "autor" and valor in libro.autor.lower():
                resultados.append(libro)
            elif criterio == "categoria" and valor in libro.categoria.lower():
                resultados.append(libro)
        
        return resultados

    def listar_libros_prestados(self, id_usuario):
        """Retorna la lista de libros prestados a un usuario específico."""
        if id_usuario not in self.usuarios_registrados:
            return None, "El usuario no existe."
        
        usuario = self.usuarios_registrados[id_usuario]
        return usuario.libros_prestados, f"Libros prestados a {usuario.nombre}:"

    def save_to_file(self, path: str):
        """Guarda el estado actual (libros y usuarios) a un archivo JSON.

        Formato:
        {
          "libros": [{"titulo":..., "autor": [titulo, autor], "categoria":..., "isbn":...}, ...],
          "usuarios": [{"nombre":..., "id_usuario":..., "libros_prestados": [isbn1, isbn2]}, ...]
        }
        """
        data = {
            "libros": [],
            "usuarios": []
        }

        for libro in self.libros_disponibles.values():
            data["libros"].append({
                "titulo": libro.titulo,
                "autor": [libro.autor],
                "categoria": libro.categoria,
                "isbn": libro.isbn,
            })

        for usuario in self.usuarios_registrados.values():
            prestamos = [lib.isbn for lib in usuario.libros_prestados]
            data["usuarios"].append({
                "nombre": usuario.nombre,
                "id_usuario": usuario.id_usuario,
                "libros_prestados": prestamos,
            })

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_from_file(self, path: str):
        """Carga libros y usuarios desde un archivo JSON si existe.

        Si faltan campos o el archivo no existe, no lanza excepción — deja el estado por defecto.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return False, "Archivo no encontrado; iniciando con datos vacíos."
        except Exception as e:
            return False, f"Error leyendo archivo: {e}"

        # Limpiar estructuras actuales
        self.libros_disponibles = {}
        self.usuarios_registrados = {}
        self.ids_usuarios = set()

        libros = data.get("libros", [])
        for lb in libros:
            titulo = lb.get("titulo")
            autor = lb.get("autor")
            # autor puede estar guardado como lista o string
            autor_str = autor[0] if isinstance(autor, list) and autor else (autor or "")
            categoria = lb.get("categoria", "")
            isbn = lb.get("isbn")
            if isbn:
                nuevo = Libro(titulo or "", autor_str, categoria, isbn)
                self.libros_disponibles[isbn] = nuevo

        usuarios = data.get("usuarios", [])
        for us in usuarios:
            nombre = us.get("nombre", "")
            id_usuario = us.get("id_usuario")
            prestamos = us.get("libros_prestados", [])
            if id_usuario:
                nuevo_usuario = Usuario(nombre, id_usuario)
                # Asociar objetos Libro por ISBN cuando exista
                for isbn in prestamos:
                    libro_obj = self.libros_disponibles.get(isbn)
                    if libro_obj:
                        nuevo_usuario.libros_prestados.append(libro_obj)
                self.usuarios_registrados[id_usuario] = nuevo_usuario
                self.ids_usuarios.add(id_usuario)

        return True, "Datos cargados correctamente."