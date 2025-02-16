from typing import Optional, List, no_type_check

import tkinter as tk
from tkinter import ttk, simpledialog
from PIL import ImageTk
from PIL.Image import Image
import matplotlib.pyplot as plt

from models.point import Point
from models.editingmode import EditingMode
from models.axesdisplay import AxesDisplay
from views.widgets.menu import Menu
from views.widgets.videocontrols import VideoControls

OVERLAY_TAG = "overlay"
HELP_NO_VIDEO = "Importez une vidéo avec le menu Fichier > Charger une vidéo"
HELP_ORIGIN = "Cliquez sur l'image pour définir l'origine du repère"
HELP_SCALE = (
    "Avec le clic gauche, sélectionnez deux points sur la vidéo pour définir l'échelle"
)
HELP_ACQUIRING = """Cliquez sur la vidéo pour définir un point et passer à l'image suivante
Vous pouvez aussi quitter le mode acquisition avec Échap ou en utilisant le menu"""
HELP_VIEWING = "Commencez l'acquisition avec le menu Acquisition ou observez les valeurs avec le menu Affichage"


class View(ttk.Frame):
    """The application's main view"""

    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)

        self.frame_label = ttk.Label(self)
        self.help_label = ttk.Label(self)
        self.canvas = tk.Canvas(self)

        self.menu = Menu()
        parent.config(menu=self.menu)
        self.controls = VideoControls(self)

        # used for garbage collection and to redraw the same frame if needed
        self.cached_frame: Optional[ImageTk.PhotoImage] = None

    def pack_widgets(self, video_loaded: bool, current_mode: EditingMode) -> None:
        """Updates the view to show widgets matching the current app state.

        Args:
            video_loaded (bool): Whether the video is loaded
            current_mode (Mode): The current editing mode
        """
        self.frame_label.pack_forget()
        self.help_label.pack_forget()
        self.canvas.pack_forget()
        self.controls.pack_forget()

        if video_loaded:
            self.frame_label.pack(padx=48, pady=(16, 0), anchor=tk.NE)
            self.canvas.pack(padx=48, pady=(0, 16))
            if current_mode == EditingMode.DEFINING_ORIGIN:
                self.help_label.config(text=HELP_ORIGIN)
            elif current_mode == EditingMode.DEFINING_SCALE:
                self.help_label.config(text=HELP_SCALE)
            elif current_mode == EditingMode.ACQUIRING:
                self.help_label.config(text=HELP_ACQUIRING)
            elif current_mode == EditingMode.VIEWING:
                self.help_label.config(text=HELP_VIEWING)

            self.help_label.pack(padx=16)
            self.controls.pack(pady=16)
        else:
            self.help_label.config(text=HELP_NO_VIDEO)
            self.help_label.pack(expand=True)

    def set_canvas_size(self, width: int, height: int) -> None:
        """Updates the canvas's size.

        Args:
            width (int): The width of the canvas
            height (int): The height of the canvas
        """
        self.canvas.config(width=width, height=height)
        self.canvas.update()

    def draw_cached_frame(self) -> bool:
        """Draws the last cached frame in the canvas.

        Returns:
            bool: Whether the operation was successful
        """
        if self.cached_frame is None:
            return False

        self.canvas.create_image(  # pyright: ignore reportUnknownVariableType
            0,
            0,
            image=self.cached_frame,
            anchor=tk.NW,
        )

        return True

    def update_frame(self, frame: Image, index: int, total_frames: int) -> None:
        """Shows a new frame and updates the frame counter.

        Args:
            frame (Image): The frame to show
            index (int): The index of the current frame
            total_frames (int): The number of frames in the video
        """
        self.frame_label.config(text=f"Frame {index}/{total_frames}")

        self.cached_frame = ImageTk.PhotoImage(image=frame)
        self.draw_cached_frame()

    def ask_for_distance(self) -> Optional[float]:
        """Asks the user for the real distance between two points.

        Returns:
            Optional[float]: The distance, or None if the user canceled the operation
        """
        return simpledialog.askfloat(
            "Distance",
            "Veuillez indiquer la distance réelle entre ces deux points (en mètres)",
        )

    def show_point(self, point: Point) -> None:
        """Draws a point on the canvas.

        Args:
            point (Point): The point to draw
        """
        self.canvas.create_oval(
            point.x - 5,
            point.y - 5,
            point.x + 5,
            point.y + 5,
            fill="red",
            tags=[OVERLAY_TAG],
        )

    def show_line(self, start: Point, end: Point) -> None:
        """Draws a line on the canvas.

        Args:
            start (Point): Where the line starts
            end (Point): Where the line stops
        """
        self.canvas.create_line(
            start.x,
            start.y,
            end.x,
            end.y,
            width=5,
            fill="red",
            tags=[OVERLAY_TAG],
        )

    def clear_overlay(self) -> None:
        """Clears things previously drawn over the frame."""
        self.canvas.delete(OVERLAY_TAG)

    def display_values(self, points: List[Point], times: List[float]):
        """Opens a window showing the acquired values.

        Args:
            points (List[Point]): The defined points
            times (List[float]): The corresponding time in the video for each point
        """
        window = tk.Toplevel()
        window.title("Valeurs")
        table = ttk.Treeview(window, columns=("time", "x", "y"), show="headings")

        table.heading("time", text="Temps (en ms)")
        table.heading("x", text="x (en m)")
        table.heading("y", text="y (en m)")

        for point, time in zip(points, times):
            table.insert("", tk.END, values=(time, point.x, point.y))

        table.pack(expand=True, fill="both")

    @no_type_check
    def display_graph(self, mode: AxesDisplay, points: List[Point], times: List[float]):
        """Opens a window showing a graph.

        Args:
            mode (AxesDisplay): The type of graph to display
            points (List[Point]): The defined points
            times (List[float]): The corresponding time in the video for each point
        """
        x_values = [point.x for point in points]
        y_values = [point.y for point in points]
        if mode == AxesDisplay.Y_TO_TIME:
            plt.plot(times, y_values, marker="o")
            plt.xlabel("temps")
            plt.ylabel("axe Y")
            plt.title("y(t)")
            plt.show()
        elif mode == AxesDisplay.X_TO_TIME:
            plt.plot(times, x_values, marker="o")
            plt.xlabel("temps")
            plt.ylabel("axe X")
            plt.title("x(t)")
            plt.show()
        elif mode == AxesDisplay.Y_TO_X:
            plt.plot(x_values, y_values, marker="o")
            plt.xlabel("axe X")
            plt.ylabel("axe Y")
            plt.title("y(x)")
            plt.show()
