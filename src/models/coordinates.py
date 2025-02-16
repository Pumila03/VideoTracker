from math import sqrt

from .point import Point


class Coordinates:
    """Operations on coordinates."""

    @staticmethod
    def translated(point: Point, x_offset: float, y_offset: float) -> Point:
        """Translates a point by a certain amount.

        Args:
            point (Point): The initial point
            x_offset (float): The offset for the x coordinate
            y_offset (float): The offset for the y coordinate

        Returns:
            Point: The translated point
        """
        return Point(point.x + x_offset, point.y + y_offset)

    @staticmethod
    def scaled(point: Point, x_factor: float, y_factor: float) -> Point:
        """Scales a point's coordinates by a certain amount.

        Args:
            point (Point): The initial point
            y_factor (float): The factor for the x coordinate
            x_factor (float): The factor for the y coordinate

        Returns:
            Point: The scaled point
        """
        return Point(point.x * x_factor, point.y * y_factor)

    @staticmethod
    def horiz_vert(start: Point, point: Point) -> Point:
        """Returns the point closest to `point` that shares one coordinate with `start` \
and the other with `point`.

        Args:
            start (Point)
            point (Point)

        Returns:
            Point: The resulting point
        """
        x_distance = abs(start.x - point.x)
        y_distance = abs(start.y - point.y)
        if x_distance < y_distance:
            return Point(start.x, point.y)
        return Point(point.x, start.y)

    @staticmethod
    def distance(point1: Point, point2: Point) -> float:
        """Returns the distance between two points.

        Args:
            point1 (Point)
            point2 (Point)

        Returns:
            float
        """
        return sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

    @staticmethod
    def relative_to_origin(origin: Point, point: Point) -> Point:
        """Transforms a point using canvas coordinates to a point with \
coordinates relative to another point.

        NOTE: In a canvas (or a video) the y-axis is pointing down, \
where as the y-axis used for the resulting point is pointing up.

        Args:
            origin (Point): The origin
            point (Point): The initial point

        Returns:
            Point: The resulting point
        """
        return Point(point.x - origin.x, origin.y - point.y)
