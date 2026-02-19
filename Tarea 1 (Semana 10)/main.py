import os
import sys

# Asegura que el directorio actual esté en el path para las importaciones modulares
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modelos.producto import Producto
from servicios.inventario import Inventario


def limpiar_pantalla():
    """Limpia la consola según el sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')


def solicitar_entero(mensaje):
    """Solicita un entero y valida la entrada."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: Por favor, ingrese un número entero válido.")


def solicitar_float(mensaje):
    """Solicita un float y valida la entrada."""
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: Por favor, ingrese un número decimal válido.")


def mostrar_menu():
    title = "Sistema de Gestión de Inventario (Mejorado)"
    options = [
        "[1] Añadir producto",
        "[2] Eliminar producto",
        "[3] Actualizar producto",
        "[4] Buscar producto",
        "[5] Listar inventario",
        "[6] Salir"
    ]

    max_content = max(len(title), max(len(o) for o in options))
    content_width = max_content + 4

    print()
    print('┌' + '─' * content_width + '┐')
    print('│' + title.center(content_width) + '│')
    print('├' + '─' * content_width + '┤')

    for opt in options:
        line = '  ' + opt.ljust(content_width - 2)
        print('│' + line + '│')

    print('└' + '─' * content_width + '┘')


def main():
    inventario = Inventario()
    # Muestra el resultado de la carga/creación del archivo al iniciar
    if inventario.last_file_message:
        print(inventario.last_file_message)

    while True:
        mostrar_menu()
        opcion = input(">> Seleccione una opcion (1-6): ")

        if opcion == '1':
            print("\n--- Añadir Nuevo Producto ---")
            id_p = input("ID único: ")
            nombre = input("Nombre: ")
            cantidad = solicitar_entero("Cantidad: ")
            precio = solicitar_float("Precio: ")

            nuevo_p = Producto(id_p, nombre, cantidad, precio)
            exito, mensaje = inventario.añadir_producto(nuevo_p)
            print(mensaje)

        elif opcion == '2':
            print("\n--- Eliminar Producto ---")
            id_p = input("Ingrese el ID del producto a eliminar: ")
            exito, mensaje = inventario.eliminar_producto(id_p)
            print(mensaje)

        elif opcion == '3':
            print("\n--- Actualizar Producto ---")
            id_p = input("Ingrese el ID del producto: ")
            print("Deje en blanco si no desea cambiar el valor.")

            cant_str = input("Nueva cantidad: ")
            prec_str = input("Nuevo precio: ")

            cantidad = int(cant_str) if cant_str.strip() else None
            precio = float(prec_str) if prec_str.strip() else None

            exito, mensaje = inventario.actualizar_producto(id_p, cantidad, precio)
            print(mensaje)

        elif opcion == '4':
            print("\n--- Buscar Producto ---")
            nombre = input("Ingrese el nombre o parte del nombre: ")
            resultados = inventario.buscar_por_nombre(nombre)

            if resultados:
                print(f"\nSe encontraron {len(resultados)} coincidencias:")
                for p in resultados:
                    print(p)
            else:
                print("No se encontraron productos con ese nombre.")

        elif opcion == '5':
            print("\n--- Listado de Inventario ---")
            productos = inventario.obtener_todos()
            if productos:
                for p in productos:
                    print(p)
            else:
                print("El inventario está vacío.")

        elif opcion == '6':
            print("Saliendo del sistema... ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

        input("\nPresione Enter para continuar...")
        limpiar_pantalla()


if __name__ == "__main__":
    main()
