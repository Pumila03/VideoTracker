from pathlib import Path
from typing import List

from .point import Point


class FileRepo:
    """Provides methods to save acquired data in CSV files."""

    def transform_data_to_csv(
        self,
        time: List[float],
        points: List[Point],
        sep: str = ",",
    ) -> str:
        """
        Transforms data acquired by the user into a CSV-formatted string \
with 3 columns named time, x and y.

        Args:
            time (List[float]): A list of floats representing the time \
elapsed since the start of the video (in seconds)
            points (List[Point]): A list of points
            sep (str): The separator used ("," by default)

        Raises:
            ValueError: No points to transform
            ValueError: 'time' and 'points' have different lengths

        Returns:
            str: The CSV string representing the input data
        """
        nb_points = len(points)
        if nb_points == 0:
            raise ValueError("No points to transform")

        if len(time) != nb_points:
            raise ValueError("'time' and 'points' have different lengths")

        csv = f"temps{sep}x{sep}y"
        for instant, point in zip(time, points):
            csv += f"\n{instant}{sep}{point.x}{sep}{point.y}"

        return csv

    def export_to_csv(
        self,
        time: List[float],
        points: List[Point],
        filepath: str | Path,
        sep: str = ",",
    ) -> None:
        """
        Saves data acquired by the user in a CSV file with 3 columns \
named time, x and y.

        Args:
            time (List[float]): A list of floats representing the time \
elapsed since the start of the video (in seconds)
            points (List[Point]): A list of points
            filepath (str | Path): The path of the file
            sep (str, optional): The separator used ("," by default)

        Raises:
            ValueError: No points to transform
            ValueError: 'time' and 'points' have different lengths
        """
        csv = self.transform_data_to_csv(time, points, sep)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(csv)
