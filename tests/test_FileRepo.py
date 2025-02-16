import unittest
import tempfile
from pathlib import Path

from src.models.filerepo import FileRepo
from src.models.point import Point

TMP = tempfile.gettempdir()

CONTENT_FILEPATH = Path(TMP).joinpath("test_present.csv")
PRESENT_FILEPATH = Path(TMP).joinpath("test_content.csv")


class testFileRepo(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FileRepo()
        self.point_list = [Point(5, 9), Point(7, 2), Point(1, 0)]
        self.time_list = [0.243, 0.267, 0.301]

    def tearDown(self) -> None:
        """Remove created files after each test."""
        CONTENT_FILEPATH.unlink(True)
        PRESENT_FILEPATH.unlink(True)

    def test_transform(self) -> None:
        """Checks that the CSV data returned by FileRepo.transform_data_to_csv \
is correct."""
        csv = self.repo.transform_data_to_csv(self.time_list, self.point_list)
        self.assertEqual(
            csv.splitlines(),
            [
                "temps,x,y",
                "0.243,5,9",
                "0.267,7,2",
                "0.301,1,0",
            ],
        )

        csv = self.repo.transform_data_to_csv(self.time_list, self.point_list, ";")
        self.assertEqual(
            csv.splitlines(),
            [
                "temps;x;y",
                "0.243;5;9",
                "0.267;7;2",
                "0.301;1;0",
            ],
        )

    def test_no_points(self) -> None:
        """Checks that the correct error is raised when there are no points."""
        with self.assertRaises(ValueError) as context:
            self.repo.transform_data_to_csv([], [])

        self.assertEqual(str(context.exception), "No points to transform")

    def test_different_len(self) -> None:
        """Checks that the correct error is raised when the lists have different lengths."""
        with self.assertRaises(ValueError) as context:
            self.repo.transform_data_to_csv([0.5], [Point(1, 0), Point(1, 2)])

        self.assertEqual(
            str(context.exception), "'time' and 'points' have different lengths"
        )

    def test_file_present(self) -> None:
        """Checks that the file exists after calling FileRepo.export_to_csv."""
        self.repo.export_to_csv(
            self.time_list,
            self.point_list,
            PRESENT_FILEPATH,
        )

        self.assertTrue(PRESENT_FILEPATH.is_file())

    def test_file_content(self) -> None:
        """Checks that the file created by calling FileRepo.export_to_csv \
contains the correct data."""
        self.repo.export_to_csv(
            self.time_list,
            self.point_list,
            CONTENT_FILEPATH,
        )

        with open(CONTENT_FILEPATH) as csv:
            content = csv.read()
            self.assertEqual(
                content.splitlines(),
                [
                    "temps,x,y",
                    "0.243,5,9",
                    "0.267,7,2",
                    "0.301,1,0",
                ],
            )
