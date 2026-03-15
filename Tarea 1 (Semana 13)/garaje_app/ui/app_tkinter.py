import tkinter as tk
from tkinter import ttk, messagebox

from modelos.vehiculo import Vehiculo
from servicios.garaje_servicio import GarajeServicio


class AppTkinter:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sistema de Gestión de Garaje")
        self.servicio = GarajeServicio()
        self.editing_index = None
        self._build_ui()

    def _build_ui(self):
        frm = ttk.Frame(self.root, padding=10)
        frm.grid(sticky="nsew")

        # Entradas
        ttk.Label(frm, text="Placa:").grid(column=0, row=0, sticky="w")
        self.placa_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.placa_var).grid(column=1, row=0, sticky="ew")

        ttk.Label(frm, text="Marca:").grid(column=0, row=1, sticky="w")
        self.marca_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.marca_var).grid(column=1, row=1, sticky="ew")

        # Nuevo campo: Cilindraje
        ttk.Label(frm, text="Cilindraje:").grid(column=0, row=2, sticky="w")
        self.cilindraje_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.cilindraje_var).grid(column=1, row=2, sticky="ew")

        ttk.Label(frm, text="Propietario:").grid(column=0, row=3, sticky="w")
        self.prop_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.prop_var).grid(column=1, row=3, sticky="ew")

        # Botones
        btn_frame = ttk.Frame(frm)
        btn_frame.grid(column=0, row=4, columnspan=2, pady=8)

        self.add_button = ttk.Button(btn_frame, text="Agregar vehículo", command=self.agregar_vehiculo)
        self.add_button.grid(column=0, row=0, padx=4)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_campos).grid(column=1, row=0, padx=4)
        ttk.Button(btn_frame, text="Editar", command=self.editar_vehiculo).grid(column=2, row=0, padx=4)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_vehiculo).grid(column=3, row=0, padx=4)

        # Tabla (agregar columna Cilindraje)
        cols = ("placa", "marca", "cilindraje", "propietario")
        self.tree = ttk.Treeview(frm, columns=cols, show="headings", height=8)
        self.tree.grid(column=0, row=5, columnspan=2, sticky="nsew")
        for c, title in zip(cols, ("Placa", "Marca", "Cilindraje", "Propietario")):
            self.tree.heading(c, text=title)
            # Ajustar ancho para que la columna de cilindraje sea más estrecha
            col_width = 100 if c == "cilindraje" else 140
            self.tree.column(c, width=col_width, anchor="center")

        # Configurar expansión
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        frm.columnconfigure(1, weight=1)

    def agregar_vehiculo(self):
        placa = self.placa_var.get().strip()
        marca = self.marca_var.get().strip()
        cilindraje = self.cilindraje_var.get().strip()
        propietario = self.prop_var.get().strip()
        if not placa or not marca or not cilindraje or not propietario:
            messagebox.showwarning("Datos incompletos", "Por favor complete todos los campos.")
            return

        v = Vehiculo(placa, marca, propietario, cilindraje)
        try:
            if self.editing_index is None:
                self.servicio.agregar_vehiculo(v)
                self.tree.insert("", "end", values=v.to_tuple())
            else:
                # Guardar cambios en un vehículo existente
                try:
                    self.servicio.actualizar_vehiculo(self.editing_index, v)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                    return
                items = self.tree.get_children()
                if 0 <= self.editing_index < len(items):
                    item_id = items[self.editing_index]
                    self.tree.item(item_id, values=v.to_tuple())
                self.editing_index = None
                self.add_button.config(text="Agregar vehículo")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.limpiar_campos()

    def editar_vehiculo(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selección requerida", "Seleccione un vehículo para editar.")
            return
        item_id = sel[0]
        index = self.tree.index(item_id)
        vehiculos = self.servicio.listar_vehiculos()
        if index < 0 or index >= len(vehiculos):
            messagebox.showerror("Error", "Índice inválido para editar.")
            return
        v = vehiculos[index]
        self.placa_var.set(v.placa)
        self.marca_var.set(v.marca)
        self.cilindraje_var.set(getattr(v, "cilindraje", ""))
        self.prop_var.set(v.propietario)
        self.editing_index = index
        self.add_button.config(text="Guardar cambios")

    def eliminar_vehiculo(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selección requerida", "Seleccione un vehículo para eliminar.")
            return
        item_id = sel[0]
        index = self.tree.index(item_id)
        confirm = messagebox.askyesno("Confirmar eliminación", "¿Eliminar el vehículo seleccionado?")
        if not confirm:
            return
        try:
            self.servicio.eliminar_vehiculo(index)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        self.tree.delete(item_id)
        # Si estábamos editando ese índice, cancelar edición
        if self.editing_index is not None:
            if self.editing_index == index:
                self.editing_index = None
                self.add_button.config(text="Agregar vehículo")
            elif self.editing_index > index:
                # ajustar índice si se borró un item anterior
                self.editing_index -= 1

    def limpiar_campos(self):
        self.placa_var.set("")
        self.marca_var.set("")
        self.cilindraje_var.set("")
        self.prop_var.set("")
        # Si se estaba editando, cancelar el modo edición y restaurar el botón
        self.editing_index = None
        self.add_button.config(text="Agregar vehículo")
        # Quitar selección de la tabla si existe
        try:
            sel = self.tree.selection()
            if sel:
                self.tree.selection_remove(sel)
        except Exception:
            pass

    def cargar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for v in self.servicio.listar_vehiculos():
            self.tree.insert("", "end", values=v.to_tuple())
