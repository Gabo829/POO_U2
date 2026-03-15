import os
import tkinter as tk
from ui.app_tkinter import AppTkinter


DATA_FILE = os.path.join(os.path.dirname(__file__), "garaje.json")


def main():
    root = tk.Tk()
    app = AppTkinter(root)
    # Cargar datos si existen
    try:
        app.servicio.cargar_desde_json(DATA_FILE)
    except Exception:
        pass
    app.cargar_lista()

    def on_closing():
        try:
            app.servicio.guardar_en_json(DATA_FILE)
        except Exception:
            pass
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
