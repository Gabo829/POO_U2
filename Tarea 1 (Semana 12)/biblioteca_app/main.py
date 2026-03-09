import sys
import os

# Asegurar que el directorio actual esté en el path para importar modelos y servicios
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from servicios.biblioteca_servicio import BibliotecaServicio

def mostrar_menu():
    title = "Sistema de Gestión de Biblioteca Digital"
    opciones = [
        "[1] Añadir libro",
        "[2] Quitar libro",
        "[3] Registrar usuario",
        "[4] Dar de baja usuario",
        "[5] Prestar libro",
        "[6] Devolver libro",
        "[7] Buscar libros",
        "[8] Listar libros prestados a un usuario",
        "[0] Guardar y Salir",
    ]

    max_content = max(len(title), max(len(o) for o in opciones))
    content_width = max_content + 4

    print()
    print('┌' + '─' * content_width + '┐')
    print('│' + title.center(content_width) + '│')
    print('├' + '─' * content_width + '┤')

    for opt in opciones:
        line = '  ' + opt.ljust(content_width - 2)
        print('│' + line + '│')

    print('└' + '─' * content_width + '┘')


def main():
    servicio = BibliotecaServicio()
    DATA_FILE = os.path.join(os.path.dirname(__file__), "biblioteca.json")

    ok, msg = servicio.load_from_file(DATA_FILE)
    while True:
        opcion = mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            titulo = input("Título: ")
            autor = input("Autor: ")
            categoria = input("Categoría: ")
            isbn = input("ISBN: ")
            exito, mensaje = servicio.añadir_libro(titulo, autor, categoria, isbn)
            print(mensaje)
            
        elif opcion == "2":
            isbn = input("ISBN del libro a quitar: ")
            exito, mensaje = servicio.quitar_libro(isbn)
            print(mensaje)
            
        elif opcion == "3":
            nombre = input("Nombre del usuario: ")
            id_usuario = input("ID de usuario: ")
            exito, mensaje = servicio.registrar_usuario(nombre, id_usuario)
            print(mensaje)
            
        elif opcion == "4":
            id_usuario = input("ID de usuario a dar de baja: ")
            exito, mensaje = servicio.dar_de_baja_usuario(id_usuario)
            print(mensaje)
            
        elif opcion == "5":
            isbn = input("ISBN del libro: ")
            id_usuario = input("ID del usuario: ")
            exito, mensaje = servicio.prestar_libro(isbn, id_usuario)
            print(mensaje)
            
        elif opcion == "6":
            isbn = input("ISBN del libro: ")
            id_usuario = input("ID del usuario: ")
            exito, mensaje = servicio.devolver_libro(isbn, id_usuario)
            print(mensaje)
            
        elif opcion == "7":
            print("Buscar por: 1. Título, 2. Autor, 3. Categoría")
            criterio_op = input("Opción: ")
            criterios = {"1": "titulo", "2": "autor", "3": "categoria"}
            criterio = criterios.get(criterio_op)
            
            if criterio:
                valor = input(f"Ingrese el {criterio} a buscar: ")
                resultados = servicio.buscar_libros(criterio, valor)
                if resultados:
                    print("\nResultados encontrados:")
                    for libro in resultados:
                        print(libro)
                else:
                    print("No se encontraron libros.")
            else:
                print("Opción no válida.")
                
        elif opcion == "8":
            id_usuario = input("ID del usuario: ")
            libros, mensaje = servicio.listar_libros_prestados(id_usuario)
            print(mensaje)
            if libros:
                for libro in libros:
                    print(f" - {libro}")
            elif libros == []:
                print(" - El usuario no tiene libros prestados.")
        elif opcion == "0":
            # Guardar antes de salir
            try:
                servicio.save_to_file(DATA_FILE)
                print("Guardando datos... Saliendo del sistema...")
            except Exception:
                print("No se pudieron guardar los datos; saliendo sin persistir.")
            break
        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    main()