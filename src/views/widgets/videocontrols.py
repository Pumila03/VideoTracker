import os
from tkinter import PhotoImage, ttk, LEFT

ASSETS_DIRECTORY = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
        "assets",
    )
)

START_ICON_PATH = os.path.join(ASSETS_DIRECTORY, "backward-step-solid.png")
PREVIOUS_ICON_PATH = os.path.join(ASSETS_DIRECTORY, "backward-fast-solid.png")
PLAY_ICON_PATH = os.path.join(ASSETS_DIRECTORY, "play-solid.png")
PAUSE_ICON_PATH = os.path.join(ASSETS_DIRECTORY, "pause-solid.png")
NEXT_ICON_PATH = os.path.join(ASSETS_DIRECTORY, "forward-fast-solid.png")
END_ICON_PATH = os.path.join(ASSETS_DIRECTORY, "forward-step-solid.png")


class VideoControls(ttk.Frame):
    """A group of buttons representing video controls."""

    def __init__(self, parent: ttk.Frame):
        super().__init__(parent)

        # Created here because the root window needs to exist before creating a PhotoImage
        self.__start_icon = PhotoImage(file=START_ICON_PATH)
        self.__previous_icon = PhotoImage(file=PREVIOUS_ICON_PATH)
        self.__play_icon = PhotoImage(file=PLAY_ICON_PATH)
        self.__pause_icon = PhotoImage(file=PAUSE_ICON_PATH)
        self.__next_icon = PhotoImage(file=NEXT_ICON_PATH)
        self.__end_icon = PhotoImage(file=END_ICON_PATH)

        self.start_button = ttk.Button(self, image=self.__start_icon)
        self.previous_button = ttk.Button(self, image=self.__previous_icon)
        self.play_button = ttk.Button(self, image=self.__play_icon)
        self.next_button = ttk.Button(self, image=self.__next_icon)
        self.end_button = ttk.Button(self, image=self.__end_icon)

        self.start_button.pack(side=LEFT)
        self.previous_button.pack(side=LEFT)
        self.play_button.pack(side=LEFT)
        self.next_button.pack(side=LEFT)
        self.end_button.pack(side=LEFT)

    def reconfigure(
        self,
        paused: bool,
        reached_end: bool = False,
        can_go_back: bool = False,
    ) -> None:
        """Reconfigures buttons to match the current app state.

        Args:
            paused (bool): Whether the video is paused
            reached_end (bool, optional): Whether the end of the \
video is reached. Defaults to False.
            can_go_back (bool, optional): Whether the video is not \
currently on the first frame. Defaults to False.
        """
        play_button_icon = self.__play_icon if paused else self.__pause_icon
        left_buttons_state = "normal" if can_go_back else "disabled"
        right_buttons_state = "disabled" if reached_end else "normal"

        self.start_button.config(state=left_buttons_state)
        self.previous_button.config(state=left_buttons_state)
        self.play_button.config(
            image=play_button_icon,
            state=right_buttons_state,
        )
        self.next_button.config(state=right_buttons_state)
        self.end_button.config(state=right_buttons_state)
