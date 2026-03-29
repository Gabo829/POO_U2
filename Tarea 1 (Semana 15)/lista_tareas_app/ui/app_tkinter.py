import tkinter as tk
from tkinter import ttk, messagebox
from servicios.tarea_servicio import TareaServicio

class App:
    """Interfaz gráfica de la aplicación "Lista de Tareas".

    Implementa eventos con `.bind()` y comandos con `command=`.
    - Enter en Entry añade la tarea.
    - Doble clic en la lista alterna completado/descompletado.
    """

    def __init__(self):
        self.servicio = TareaServicio()

        self.root = tk.Tk()
        self.root.title("Lista de Tareas")
        self.root.geometry("480x400")

        frm = ttk.Frame(self.root, padding=12)
        frm.pack(fill=tk.BOTH, expand=True)

        # Campo de entrada
        self.entry = ttk.Entry(frm)
        self.entry.pack(fill=tk.X, side=tk.TOP, padx=2, pady=4)
        self.entry.focus()
        # Evento de teclado: agregar con Enter
        self.entry.bind('<Return>', lambda e: self.agregar_tarea())

        # Botones
        btn_frame = ttk.Frame(frm)
        btn_frame.pack(fill=tk.X, pady=4)

        btn_add = ttk.Button(btn_frame, text="Añadir Tarea", command=self.agregar_tarea)
        btn_add.pack(side=tk.LEFT, padx=4)

        btn_mark = ttk.Button(btn_frame, text="Marcar Completada", command=self.marcar_seleccionada)
        btn_mark.pack(side=tk.LEFT, padx=4)

        btn_del = ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_seleccionada)
        btn_del.pack(side=tk.LEFT, padx=4)

        # Lista con scrollbar
        list_frame = ttk.Frame(frm)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(list_frame, yscrollcommand=self.scrollbar.set, activestyle='none')
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        # Evento de ratón: doble clic para alternar completado
        self.listbox.bind('<Double-1>', lambda e: self.toggle_completado())

        # Estado visual: colores
        self._fg_default = 'black'
        self._fg_completed = 'gray'

        self.refresh()

    def agregar_tarea(self):
        texto = self.entry.get().strip()
        if not texto:
            messagebox.showwarning("Aviso", "La descripción no puede estar vacía")
            return
        # Lógica via servicio
        self.servicio.agregar(texto)
        self.entry.delete(0, tk.END)
        self.refresh()

    def marcar_seleccionada(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "Seleccione una tarea")
            return
        index = sel[0]
        tarea = self.servicio.listar()[index]
        self.servicio.marcar_completada(tarea.id)
        self.refresh()

    def eliminar_seleccionada(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "Seleccione una tarea")
            return
        index = sel[0]
        tarea = self.servicio.listar()[index]
        self.servicio.eliminar_por_id(tarea.id)
        self.refresh()

    def toggle_completado(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        index = sel[0]
        tarea = self.servicio.listar()[index]
        if tarea.completado:
            self.servicio.desmarcar(tarea.id)
        else:
            self.servicio.marcar_completada(tarea.id)
        self.refresh()

    def refresh(self):
        # Renderiza la lista desde el servicio y aplica feedback visual
        self.listbox.delete(0, tk.END)
        tareas = self.servicio.listar()
        for i, t in enumerate(tareas):
            status = "✔️" if t.completado else "❌"
            texto = f"{status} {t.descripcion}"
            self.listbox.insert(tk.END, texto)
            # Apply color for completed tasks
            try:
                if t.completado:
                    self.listbox.itemconfig(i, fg=self._fg_completed)
                else:
                    self.listbox.itemconfig(i, fg=self._fg_default)
            except Exception:
                # Algunas versiones/tk no soportan itemconfig; en ese caso usamos prefijo sólo
                pass

    def run(self):
        self.root.mainloop()
