import os
import sys

# Asegura importaciones relativas si se ejecuta desde la carpeta
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from servicios.inventario import Inventario
from modelos.producto import Producto
from pathlib import Path

# Archivo de datos situado siempre junto a este script (evita crear archivos fuera)
DATA_FILE = str(Path(__file__).resolve().parent / "inventario.json")


def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


def solicitar_entero(mensaje: str) -> int:
    while True:
        try:
            s = input(mensaje).strip()
            val = int(s)
            return val
        except ValueError:
            print("Error: Por favor ingrese un número entero válido.")


def solicitar_float(mensaje: str) -> float:
    """Acepta coma o punto como separador decimal y valida la entrada."""
    while True:
        s = input(mensaje).strip()
        s = s.replace(',', '.')
        try:
            return float(s)
        except ValueError:
            print("Error: Por favor ingrese un número decimal válido (use punto o coma). Ejemplo: 0.5 o 0,5")


def solicitar_texto_no_vacio(mensaje: str) -> str:
    while True:
        s = input(mensaje).strip()
        if s:
            return s
        print("Error: Este campo no puede quedar vacío.")


def input_product_data():
    id_ = solicitar_texto_no_vacio("ID: ")
    nombre = solicitar_texto_no_vacio("Nombre: ")
    cantidad = solicitar_entero("Cantidad: ")
    while cantidad < 0:
        print("Error: La cantidad no puede ser negativa.")
        cantidad = solicitar_entero("Cantidad: ")
    precio = solicitar_float("Precio: ")
    while precio < 0:
        print("Error: El precio no puede ser negativo.")
        precio = solicitar_float("Precio: ")
    return Producto(id_, nombre, cantidad, precio)


def mostrar_producto(prod: Producto):
    if not prod:
        print("No existe el producto.")
        return
    print(f"ID: {prod.get_id()} | Nombre: {prod.get_nombre()} | Cantidad: {prod.get_cantidad()} | Precio: {prod.get_precio()}")


def mostrar_menu():
    title = "Sistema Avanzado de Gestión de Inventario"
    options = [
        "[1] Añadir producto",
        "[2] Eliminar producto por ID",
        "[3] Actualizar cantidad",
        "[4] Actualizar precio",
        "[5] Buscar producto",
        "[6] Mostrar inventario",
        "[7] Guardar y salir",
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
    inv = Inventario()
    inv.load_from_file(DATA_FILE)

    while True:
        mostrar_menu()
        opc = input("Seleccione una opción: ").strip()

        try:
            if opc == "1":
                prod = input_product_data()
                inv.add_product(prod)
                print("Producto añadido.")
            elif opc == "2":
                pid = input("ID a eliminar: ").strip()
                removed = inv.remove_product(pid)
                print("Eliminado." if removed else "ID no encontrado.")
            elif opc == "3":
                pid = input("ID: ").strip()
                cant_str = input("Nueva cantidad (dejar vacío para no cambiar): ").strip()
                if cant_str == "":
                    print("No se modificó la cantidad.")
                else:
                    # validar y aplicar
                    try:
                        cantidad = int(cant_str)
                    except ValueError:
                        print("Error: ingrese un número entero válido para la cantidad.")
                    else:
                        if cantidad < 0:
                            print("Error: La cantidad no puede ser negativa.")
                        else:
                            inv.update_quantity(pid, cantidad)
                            print("Cantidad actualizada.")
            elif opc == "4":
                pid = input("ID: ").strip()
                prec_str = input("Nuevo precio (dejar vacío para no cambiar): ").strip()
                if prec_str == "":
                    print("No se modificó el precio.")
                else:
                    try:
                        prec = float(prec_str.replace(',', '.'))
                    except ValueError:
                        print("Error: ingrese un número válido para el precio.")
                    else:
                        if prec < 0:
                            print("Error: El precio no puede ser negativo.")
                        else:
                            inv.update_price(pid, prec)
                            print("Precio actualizado.")
            elif opc == "5":
                q = input("Nombre o parte del nombre: ").strip()
                res = inv.search_by_name(q)
                if not res:
                    print("No se encontraron coincidencias.")
                else:
                    for p in res:
                        mostrar_producto(p)
            elif opc == "6":
                todos = inv.list_all()
                if not todos:
                    print("Inventario vacío.")
                else:
                    for p in todos:
                        mostrar_producto(p)
            elif opc == "7":
                inv.save_to_file(DATA_FILE)
                print("Inventario guardado. Saliendo...")
                break
            else:
                print("Opción no válida.")
        except Exception as e:
            # Mensaje de error en español, sin exponer trace completo al usuario
            print(f"Error: {e}")

        input("\nPresione Enter para continuar...")
        limpiar_pantalla()


if __name__ == "__main__":
    main()
