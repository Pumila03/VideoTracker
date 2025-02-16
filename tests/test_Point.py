import unittest

from src.models.point import Point


class TestPoint(unittest.TestCase):
    def test_getters(self) -> None:
        """Checks that the returned coordinates are correct."""
        point = Point(2.12024, 672.2342)
        self.assertEqual(2.12024, point.x)
        self.assertEqual(672.2342, point.y)

        point = Point(242.28, 2874.2449)
        self.assertEqual(242.28, point.x)
        self.assertEqual(2874.2449, point.y)

        point = Point(835.1, 24)
        self.assertEqual(835.1, point.x)
        self.assertEqual(24, point.y)

    def test_repr(self) -> None:
        """Checks that the string representation is correct."""
        self.assertEqual("(0, 0)", str(Point(0, 0)))
        self.assertEqual("(2432, 24)", str(Point(2432, 24)))
        self.assertEqual("(-134.0, 234)", str(Point(-134.0, 234)))
