import os
import sys

import tkinter as tk
from views.view import View

from controllers.controller import Controller

src_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(src_path)


class Application(tk.Tk):
    """The application's main window"""

    def __init__(self):
        super().__init__()
        self.title("Video Tracker")
        self.geometry("960x540")

        self.view = View(self)
        self.view.pack(fill=tk.BOTH, expand=True)

        self.controller = Controller(self.view, self.quit)
        self.protocol("WM_DELETE_WINDOW", self.controller.clean_quit)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
