import sys
import os

if getattr(sys, "frozen", False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from ui.app_tkinter import App


def main() -> None:
    app = App()
    app.run()


if __name__ == "__main__":
    main()
