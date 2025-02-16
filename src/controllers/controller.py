from tkinter import Event, messagebox, filedialog
from typing import Any, Callable, Optional, Tuple, List
from time import perf_counter
from pathlib import Path

from views.view import View
from models.editingmode import EditingMode
from models.axesdisplay import AxesDisplay
from models.point import Point
from models.video import Video
from models.filerepo import FileRepo
from models.coordinates import Coordinates

SHOWN_POINTS = 5


class Controller:
    """The application's main controller."""

    def __init__(self, view: View, on_quit: Callable[[], Any]) -> None:
        self.__view = view
        self.__quit = on_quit

        self.__paused = True
        self.__current_mode = EditingMode.DEFINING_ORIGIN
        self.__filerepo = FileRepo()

        self.__points: List[Point | None] = []
        self.__video: Optional[Video] = None
        self.__origin: Optional[Point] = None
        self.__scale: Optional[float] = None

        # used to store the first point when defining the scale
        self.__scale_start: Optional[Point] = None

        self.reconfigure_view()
        self.config_events()

    def clean_quit(self) -> None:
        """Asks user for confirmation if needed, then quits."""
        message = "Si vous quittez l'application, vous perdrez les modifications non enregistrées. Êtes vous sûr de vouloir quitter ?"
        if self.__video is None or messagebox.askokcancel("Quitter", message):  # type: ignore
            self.__quit()

    def open_video_file(self) -> None:
        """Asks for confirmation if a video is already loaded, then opens \
a file explorer to ask the user for a video file, then loads the video and updates \
the application's state."""
        message = "Si vous chargez une nouvelle vidéo, vous perdrez les modifications non enregistrées. Êtes vous sûr de vouloir charger une nouvelle vidéo ?"
        if self.__video is None or messagebox.askokcancel("Ouvrir une vidéo", message):  # type: ignore
            filename = filedialog.askopenfilename()
            if Path(str(filename)).is_file():
                try:
                    self.__video = Video(filename)
                    self.__points = [None] * self.__video.frame_count
                    self.__paused = True
                    self.reconfigure_view()
                    self.__view.set_canvas_size(self.__video.width, self.__video.height)
                    self.__view.winfo_toplevel().geometry("")
                    self.next_frame()
                except ValueError as e:
                    messagebox.showerror(  # pyright: ignore reportUnknownVariableType
                        title="Erreur", message=str(e)
                    )

    def save_to_file(self) -> None:
        """Saves points to a file chosen by the user."""
        filename = filedialog.asksaveasfilename(
            confirmoverwrite=True,
            defaultextension=".csv",
        )

        if filename:
            try:
                point_list, time_list = self.transformed_values()
                self.__filerepo.export_to_csv(time_list, point_list, filename)
            except ValueError as error:
                messagebox.showerror("Erreur", str(error))  # type: ignore

    def next_frame(self) -> bool:
        """Shows the next frame.

        Returns:
            bool: True if the operation was a success
        """
        if self.__video is None:
            return False

        frame = self.__video.get_frame()
        if frame is None:
            self.__paused = True
            return False

        self.__view.update_frame(
            frame,
            self.__video.current_frame,
            self.__video.frame_count,
        )

        self.__view.controls.reconfigure(
            self.__paused,
            self.__video.current_frame == self.__video.frame_count,
            self.__video.current_frame != 1,
        )

        show_points = self.__current_mode in (
            EditingMode.VIEWING,
            EditingMode.ACQUIRING,
        )

        if show_points:
            for point_index in range(
                max(self.__video.current_frame - SHOWN_POINTS - 1, 0),
                self.__video.current_frame,
            ):
                point = self.__points[point_index]
                if point is not None:
                    self.__view.show_point(point)

        return True

    def first_frame(self) -> bool:
        """Shows the first frame.

        Returns:
            bool: True if the operation was a success
        """
        if self.__video is None:
            return False

        self.__video.go_to(0)
        return self.next_frame()

    def previous_frame(self) -> bool:
        """Shows the previous frame.

        Returns:
            bool: True if the operation was a success
        """
        if self.__video is None:
            return False

        self.__video.go_back()
        self.__video.go_back()
        return self.next_frame()

    def last_frame(self) -> bool:
        """Shows the previous frame.

        Returns:
            bool: True if the operation was a success
        """
        if self.__video is None:
            return False

        self.__video.go_to(self.__video.frame_count - 1)
        return self.next_frame()

    def play_video(self) -> None:
        """Plays the video normally."""
        if self.__paused or self.__video is None:
            return

        before = int(perf_counter() * 1000)
        self.next_frame()
        after = int(perf_counter() * 1000)

        elapsed = after - before
        delay = max(self.__video.frame_duration_ms - elapsed, 0)
        self.__view.after(int(delay), self.play_video)

    def toggle_playback(self) -> None:
        """Toggles playback of the video."""
        if self.__video is not None:
            self.__paused = not self.__paused
            if not self.__paused:
                self.play_video()

            self.__view.controls.reconfigure(
                self.__paused,
                self.__video.current_frame == self.__video.frame_count,
                self.__video.current_frame != 1,
            )

    def reconfigure_view(self) -> None:
        """Reconfigures the view entirely to match the current state by \
repacking the widgets, reconfiguring the menu, and updating the canvas's size"""
        self.__view.pack_widgets(self.__video is not None, self.__current_mode)
        self.__view.menu.reconfigure(self.__video is not None, self.__current_mode)

    def config_events(self) -> None:
        """Binds controller methods to widget events to make the view interactive."""
        self.__view.menu.file_menu.entryconfigure(0, command=self.open_video_file)
        self.__view.menu.file_menu.entryconfigure(1, command=self.toggle_playback)
        self.__view.menu.file_menu.entryconfigure(2, command=self.save_to_file)
        self.__view.menu.file_menu.entryconfigure(4, command=self.clean_quit)

        self.__view.menu.acquisition_menu.entryconfigure(
            0,
            command=self.on_toggle_acquisition,
        )
        self.__view.menu.acquisition_menu.entryconfigure(
            1,
            command=lambda: self.set_mode(EditingMode.DEFINING_ORIGIN),
        )
        self.__view.menu.acquisition_menu.entryconfigure(
            2,
            command=lambda: self.set_mode(EditingMode.DEFINING_SCALE),
        )

        self.__view.menu.show_menu.entryconfigure(
            0,
            command=lambda: self.__view.display_graph(  # type: ignore
                AxesDisplay.Y_TO_TIME, *self.transformed_values()
            ),
        )
        self.__view.menu.show_menu.entryconfigure(
            1,
            command=lambda: self.__view.display_graph(  # type: ignore
                AxesDisplay.X_TO_TIME, *self.transformed_values()
            ),
        )
        self.__view.menu.show_menu.entryconfigure(
            2,
            command=lambda: self.__view.display_graph(  # type: ignore
                AxesDisplay.Y_TO_X, *self.transformed_values()
            ),
        )
        self.__view.menu.show_menu.entryconfigure(
            3,
            command=lambda: self.__view.display_values(*self.transformed_values()),
        )

        self.__view.controls.start_button.config(command=self.first_frame)
        self.__view.controls.previous_button.config(command=self.previous_frame)
        self.__view.controls.play_button.config(command=self.toggle_playback)
        self.__view.controls.next_button.config(command=self.next_frame)
        self.__view.controls.end_button.config(command=self.last_frame)

        # NOTE: the handlers have to be added in this order
        # if not, canvas_click_scale can be triggered after canvas_click_origin for the same click
        self.__view.canvas.bind("<Button-1>", self.canvas_click_acquiring, "+")  # type: ignore
        self.__view.canvas.bind("<Button-1>", self.canvas_click_scale, "+")  # type: ignore
        self.__view.canvas.bind("<Button-1>", self.canvas_click_origin, "+")  # type: ignore
        self.__view.canvas.bind("<Motion>", self.canvas_move_scale)  # type: ignore

        self.__view.winfo_toplevel().bind(
            "<Escape>",
            lambda _: self.stop_acquisition(),
        )
        self.__view.winfo_toplevel().bind(
            "<Control-o>",
            lambda _: self.open_video_file(),
        )
        self.__view.winfo_toplevel().bind(
            "<Control-q>",
            lambda _: self.clean_quit(),
        )

    def set_mode(self, mode: EditingMode) -> None:
        """Changes the current mode, reconfigures the view and clears the overlay.

        Args:
            mode (EditingMode): The new editing mode
        """
        self.__current_mode = mode
        self.reconfigure_view()
        self.__view.clear_overlay()

    def stop_acquisition(self) -> None:
        """Goes back to viewing mode if the app is in acquisition mode."""
        if self.__current_mode == EditingMode.ACQUIRING:
            self.set_mode(EditingMode.VIEWING)

    def on_toggle_acquisition(self) -> None:
        """Switches between viewing and acquisition mode."""
        if self.__current_mode == EditingMode.VIEWING:
            self.set_mode(EditingMode.ACQUIRING)
        elif self.__current_mode == EditingMode.ACQUIRING:
            self.set_mode(EditingMode.VIEWING)

    def canvas_click_origin(self, event: Event) -> None:  # type: ignore
        """Handles clicks on the canvas when defining the origin.

        Args:
            event (Event): The click event
        """
        if self.__current_mode == EditingMode.DEFINING_ORIGIN:
            self.__origin = Point(event.x, event.y)
            if self.__scale is None:
                self.set_mode(EditingMode.DEFINING_SCALE)
            else:
                self.set_mode(EditingMode.VIEWING)

    def canvas_click_scale(self, event: Event) -> None:  # type: ignore
        """Handles clicks in the canvas when defining the scale.

        Args:
            event (Event): The click event
        """
        if self.__current_mode == EditingMode.DEFINING_SCALE:
            clicked_point = Point(event.x, event.y)
            if self.__scale_start is None:
                self.__scale_start = clicked_point
            else:
                new_point = Coordinates.horiz_vert(self.__scale_start, clicked_point)
                distance = Coordinates.distance(self.__scale_start, new_point)
                real_distance = self.__view.ask_for_distance()
                if real_distance is not None:
                    self.__scale = distance / real_distance
                    self.__scale_start = None
                    self.set_mode(EditingMode.VIEWING)

    def canvas_click_acquiring(self, event: Event) -> None:  # type: ignore
        """Handles clicks in the canvas when acquiring.

        Args:
            event (Event): The click event
        """
        if self.__current_mode == EditingMode.ACQUIRING and self.__video is not None:
            self.__points[self.__video.current_frame - 1] = Point(event.x, event.y)
            if not self.next_frame():
                self.stop_acquisition()

    def canvas_move_scale(self, event: Event) -> None:  # type: ignore
        """Handles motion events in the canvas when defining scale.

        Args:
            event (Event): The motion event
        """
        show_scale = self.__current_mode == EditingMode.DEFINING_SCALE
        if show_scale and self.__scale_start is not None:
            self.__view.clear_overlay()
            self.__view.show_point(self.__scale_start)
            mouse_position = Point(event.x, event.y)
            self.__view.show_line(
                self.__scale_start,
                Coordinates.horiz_vert(self.__scale_start, mouse_position),
            )

    def transformed_values(self) -> Tuple[List[Point], List[float]]:
        """Returns the transformed points and their corresponding time in the video.

        Returns:
            Tuple[List[Point], List[float]]: A list of transformed points and a list \
of times in milliseconds. The lists are empty if there is no video, origin or scale.
        """
        if self.__video is None or self.__origin is None or self.__scale is None:
            return [], []  # allows us to unpack safely

        time = [
            i * self.__video.frame_duration_ms
            for i, point in enumerate(self.__points)
            if point is not None
        ]

        points = [
            Coordinates.scaled(
                Coordinates.relative_to_origin(self.__origin, point),
                1 / self.__scale,
                1 / self.__scale,
            )
            for point in self.__points
            if point is not None
        ]

        return points, time
