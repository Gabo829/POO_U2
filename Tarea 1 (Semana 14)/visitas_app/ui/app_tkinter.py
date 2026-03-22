import tkinter as tk
from tkinter import ttk, messagebox
import re
from modelos.visitante import Visitante


class AppTkinter(tk.Tk):
    def __init__(self, servicio):
        super().__init__()
        self.servicio = servicio
        self.title("Registro de Visitantes")
        self.resizable(False, False)
        self._editing_cedula = None
        self._crear_widgets()
        self.poblar_tabla()

    def _crear_widgets(self):
        frame_form = ttk.Frame(self, padding=4)
        frame_form.pack(fill='x')

        lbl_ced = ttk.Label(frame_form, text="Cédula:")
        lbl_ced.grid(row=0, column=0, sticky='w')
        self.ent_cedula = ttk.Entry(frame_form)
        self.ent_cedula.grid(row=0, column=1, sticky='ew', padx=5)

        lbl_nombre = ttk.Label(frame_form, text="Nombre completo:")
        lbl_nombre.grid(row=1, column=0, sticky='w')
        self.ent_nombre = ttk.Entry(frame_form)
        self.ent_nombre.grid(row=1, column=1, sticky='ew', padx=5)

        lbl_motivo = ttk.Label(frame_form, text="Motivo:")
        lbl_motivo.grid(row=2, column=0, sticky='w')
        self.ent_motivo = ttk.Entry(frame_form)
        self.ent_motivo.grid(row=2, column=1, sticky='ew', padx=5)

        frame_form.columnconfigure(1, weight=1)

        frame_actions = ttk.Frame(self, padding=2)
        frame_actions.pack(fill='x')

        # Marco interno para centrar los botones
        actions_inner = ttk.Frame(frame_actions)
        actions_inner.pack(anchor='center', pady=0)

        # Botones: Registrar, Limpiar, Editar, Eliminar
        self.btn_registrar = ttk.Button(actions_inner, text="Registrar", command=self.registrar)
        self.btn_registrar.pack(side='left', padx=6)
        btn_limpiar = ttk.Button(actions_inner, text="Limpiar", command=self.limpiar_campos)
        btn_limpiar.pack(side='left', padx=6)
        btn_editar = ttk.Button(actions_inner, text="Editar", command=self.editar)
        btn_editar.pack(side='left', padx=6)
        btn_eliminar = ttk.Button(actions_inner, text="Eliminar", command=self.eliminar)
        btn_eliminar.pack(side='left', padx=6)

        frame_table = ttk.Frame(self, padding=4)
        # reducir espacio superior entre botones y tabla
        frame_table.pack(fill='both', expand=True, pady=(2,0))

        columns = ("cedula", "nombre", "motivo")
        self.tree = ttk.Treeview(frame_table, columns=columns, show='headings', selectmode='browse')
        for col, text in zip(columns, ("Cédula", "Nombre", "Motivo")):
            self.tree.heading(col, text=text, anchor='center')
            # Anchos más compactos para evitar ventana demasiado grande
            self.tree.column(col, width=180, anchor='center', stretch=True)
        self.tree.pack(fill='both', expand=True)

    def registrar(self):
        ced = self.ent_cedula.get().strip()
        nombre = self.ent_nombre.get().strip()
        motivo = self.ent_motivo.get().strip()
        # Validación: cédula debe ser numérica y tener entre 7 y 18 dígitos
        if not ced.isdigit() or not (7 <= len(ced) <= 18):
            messagebox.showwarning("Cédula inválida", "La cédula debe contener entre 7 y 18 dígitos numéricos.")
            return
        if not ced or not nombre or not motivo:
            messagebox.showwarning("Campos incompletos", "Por favor complete todos los campos.")
            return
        # Validación: nombre y motivo solo letras y espacios
        letras_pattern = re.compile(r'^[A-Za-zÀ-ÖØ-öø-ÿÑñ\s]+$')
        if not letras_pattern.match(nombre):
            messagebox.showwarning("Nombre inválido", "El nombre solo debe contener letras y espacios.")
            return
        if not letras_pattern.match(motivo):
            messagebox.showwarning("Motivo inválido", "El motivo solo debe contener letras y espacios.")
            return
        visitante = Visitante(ced, nombre, motivo)
        # Si estamos en modo edición, actualizar en lugar de agregar
        if self._editing_cedula:
            try:
                self.servicio.actualizar_por_cedula(self._editing_cedula, visitante)
            except ValueError as e:
                messagebox.showwarning("Error", str(e))
                return
            self._editing_cedula = None
            self.btn_registrar.config(text="Registrar")
            messagebox.showinfo("Éxito", "Registro actualizado correctamente.")
        else:
            try:
                self.servicio.agregar(visitante)
            except ValueError as e:
                messagebox.showwarning("Error", str(e))
                return
            messagebox.showinfo("Éxito", "Visitante registrado correctamente.")

        self.poblar_tabla()
        self.limpiar_campos()

    def eliminar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Seleccionar", "Seleccione un registro para eliminar.")
            return
        valores = self.tree.item(sel[0], 'values')
        cedula = valores[0]
        confirmar = messagebox.askyesno("Confirmar eliminación", f"¿Eliminar visitante con cédula {cedula}?")
        if not confirmar:
            return
        try:
            self.servicio.eliminar_por_cedula(cedula)
        except ValueError as e:
            messagebox.showwarning("Error", str(e))
            return
        # Si se estaba editando ese registro, cancelar edición
        if self._editing_cedula == cedula:
            self._editing_cedula = None
            self.btn_registrar.config(text="Registrar")

        self.poblar_tabla()
        messagebox.showinfo("Éxito", "Registro eliminado.")

    def editar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selección requerida", "Seleccione un registro para editar.")
            return
        valores = self.tree.item(sel[0], 'values')
        cedula = valores[0]
        nombre = valores[1]
        motivo = valores[2]
        # Poner los valores en los campos y activar modo edición
        self.ent_cedula.delete(0, tk.END)
        self.ent_cedula.insert(0, cedula)
        self.ent_nombre.delete(0, tk.END)
        self.ent_nombre.insert(0, nombre)
        self.ent_motivo.delete(0, tk.END)
        self.ent_motivo.insert(0, motivo)
        self._editing_cedula = cedula
        self.btn_registrar.config(text="Guardar cambios")

    def limpiar_campos(self):
        self.ent_cedula.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)
        self.ent_motivo.delete(0, tk.END)
        # Si estaba en modo edición, cancelar y restaurar botón
        try:
            if getattr(self, "_editing_cedula", None):
                self._editing_cedula = None
                if hasattr(self, 'btn_registrar'):
                    self.btn_registrar.config(text="Registrar")
        except Exception:
            pass

    def poblar_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for v in self.servicio.listar():
            self.tree.insert('', tk.END, values=(v.cedula, v.nombre, v.motivo))
