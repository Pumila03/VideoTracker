import tkinter as tk

from models.editingmode import EditingMode


class Menu(tk.Menu):
    """The application's menu."""

    def __init__(self):
        super().__init__()

        self.file_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Fichier", menu=self.file_menu)

        self.file_menu.add_command(
            label="Charger un fichier vidéo", accelerator="Ctrl+O"
        )
        self.file_menu.add_command(label="Lire une vidéo")
        self.file_menu.add_command(label="Enregistrer sous")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quitter", accelerator="Ctrl+Q")

        self.show_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Affichage", menu=self.show_menu)

        self.show_menu.add_command(label="Afficher y(t)")
        self.show_menu.add_command(label="Afficher x(t)")
        self.show_menu.add_command(label="Afficher y(x)")
        self.show_menu.add_command(label="Afficher les valeurs")

        self.acquisition_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Acquisition", menu=self.acquisition_menu)

        self.acquisition_menu.add_command(label="Commencer/Arrêter l'acquisition")
        self.acquisition_menu.add_command(label="Redefinir l'origine")
        self.acquisition_menu.add_command(label="Redefinir l'echelle")

    def reconfigure(
        self,
        video_loaded: bool = False,
        current_mode: EditingMode = EditingMode.DEFINING_ORIGIN,
    ) -> None:
        """Reconfigures the menu to match the current app state.

        Args:
            video_loaded (bool, optional): Whether a video is loaded. Defaults to False.
            current_mode (EditingMode, optional): The current editing mode. Defaults to EditingMode.DEFINING_ORIGIN.
        """
        needs_video = "normal" if video_loaded else "disabled"
        needs_video_and_viewing = (
            "normal"
            if video_loaded and current_mode == EditingMode.VIEWING
            else "disabled"
        )
        needs_video_and_not_defining = (
            "normal"
            if video_loaded
            and current_mode in (EditingMode.VIEWING, EditingMode.ACQUIRING)
            else "disabled"
        )

        self.file_menu.entryconfigure(1, state=needs_video)
        self.file_menu.entryconfigure(2, state=needs_video_and_viewing)

        self.show_menu.entryconfigure(0, state=needs_video_and_viewing)
        self.show_menu.entryconfigure(1, state=needs_video_and_viewing)
        self.show_menu.entryconfigure(2, state=needs_video_and_viewing)
        self.show_menu.entryconfigure(3, state=needs_video_and_viewing)

        self.acquisition_menu.entryconfigure(0, state=needs_video_and_not_defining)
        self.acquisition_menu.entryconfigure(1, state=needs_video_and_viewing)
        self.acquisition_menu.entryconfigure(2, state=needs_video_and_viewing)
