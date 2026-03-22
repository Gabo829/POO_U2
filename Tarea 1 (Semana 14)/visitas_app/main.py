import os
import tkinter as tk
from servicios.visita_servicio import VisitaServicio
from ui.app_tkinter import AppTkinter

DATA_FILE = os.path.join(os.path.dirname(__file__), "visitas.json")

def main():
    servicio = VisitaServicio()
    app = AppTkinter(servicio)
    # Cargar datos si existen
    try:
        servicio.cargar_desde_json(DATA_FILE)
    except Exception:
        pass
    app.poblar_tabla()

    def on_closing():
        try:
            servicio.guardar_en_json(DATA_FILE)
        except Exception:
            pass
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()


if __name__ == "__main__":
    main()
