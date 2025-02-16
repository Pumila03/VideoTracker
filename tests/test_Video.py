from src.models.video import Video
import unittest
import os

RESSOURCES_DIRECTORY = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "ressources")
)

VALID_FILE_PATH = os.path.join(RESSOURCES_DIRECTORY, "sample.mp4")
IMAGE_PATH = os.path.join(RESSOURCES_DIRECTORY, "image.jpeg")


class testVideo(unittest.TestCase):
    def test_open_valid_file(self):
        """Checks that a Video instance can be created from a valid video file."""
        video = Video(filename=VALID_FILE_PATH)
        self.assertIsInstance(video, Video)

    def test_open_invalid_file(self):
        """Checks that a Video instance cannot be created from an invalid file."""
        with self.assertRaises(ValueError) as context:
            Video(filename="./ressources/invalidfile.mp4")

        self.assertEqual(str(context.exception), "Impossible de charger la vidéo")

    def test_image(self):
        """Checks that a Video instance cannot be created from an image."""
        with self.assertRaises(ValueError) as context:
            Video(filename=IMAGE_PATH)

        self.assertEqual(str(context.exception), "Nombre d'images invalide")

    def test_properties(self):
        """Checks that the properties of the instance match the properties of the video."""
        video = Video(filename=VALID_FILE_PATH)
        self.assertEqual(video.width, 640)
        self.assertEqual(video.height, 480)
        self.assertEqual(video.frame_duration_ms, 40)
        self.assertEqual(video.frame_count, 774)

    def test_go_to_valid(self):
        """Checks that Video.go_to works as expected with a valid index."""
        video = Video(filename=VALID_FILE_PATH)
        self.assertTrue(video.go_to(50))
        self.assertEqual(video.current_frame, 50)

    def test_go_to_invalid(self):
        """Checks that Video.go_to works as expected with an invalid index."""
        video = Video(filename=VALID_FILE_PATH)
        self.assertFalse(video.go_to(-5))
        self.assertEqual(video.current_frame, 0)

    def test_go_back_valid(self):
        """Checks that Video.go_back works as expected with a valid index."""
        video = Video(filename=VALID_FILE_PATH)
        video.go_to(50)
        self.assertTrue(video.go_back())
        self.assertEqual(video.current_frame, 49)

    def test_go_back_invalid(self):
        """Checks that Video.go_back works as expected with an invalid index."""
        video = Video(filename=VALID_FILE_PATH)
        self.assertFalse(video.go_back())
        self.assertEqual(video.current_frame, 0)

    def test_get_frame(self):
        """Checks that Video.get_frame can return the first frame."""
        video = Video(filename=VALID_FILE_PATH)
        frame = video.get_frame()
        self.assertNotEqual(frame, None)
