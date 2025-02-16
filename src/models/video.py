import cv2
from PIL import Image


class Video:
    """Represents a video."""

    def __init__(self, filename: str):
        self.__capture = cv2.VideoCapture(filename)
        if not self.__capture.isOpened():
            raise ValueError("Impossible de charger la vidéo")

        self.__width = int(self.__capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.__height = int(self.__capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.__frame_duration = 1000 / self.__capture.get(cv2.CAP_PROP_FPS)
        self.__frame_count = int(self.__capture.get(cv2.CAP_PROP_FRAME_COUNT))

        if self.frame_count <= 1:
            raise ValueError("Nombre d'images invalide")

    @property
    def width(self) -> int:
        """The width of the video (in pixels)."""
        return self.__width

    @property
    def height(self) -> int:
        """The height of the video (in pixels)."""
        return self.__height

    @property
    def frame_duration_ms(self) -> float:
        """The duration of a frame (in milliseconds)."""
        return self.__frame_duration

    @property
    def frame_count(self) -> int:
        """The amount of frames in the video."""
        return self.__frame_count

    @property
    def current_frame(self) -> int:
        """The index of the current frame (starting at 1)."""
        return int(self.__capture.get(cv2.CAP_PROP_POS_FRAMES))

    def go_to(self, frame_index: int) -> bool:
        """Goes to a specific frame.

        Args:
            frame_index (int): The index (starting at 1) of the frame

        Returns:
            bool: True if the operation was a success
        """
        if 0 <= frame_index <= self.frame_count:
            self.__capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            return True

        return False

    def go_back(self) -> bool:
        """Goes back one frame.

        Returns:
            bool: True if the operation was a success
        """
        return self.go_to(self.current_frame - 1)

    def get_frame(self) -> Image.Image | None:
        """Reads and returns the current frame from the video.

        Returns:
            Image | None: The current frame, or None if the operation \
failed (end of video was reached or there was an error)
        """
        try:
            ret, frame = self.__capture.read()
            if ret:
                return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            return None
        except:
            return None

    def __del__(self) -> None:
        """Releases the video source when an instance is destroyed."""
        self.__capture.release()
