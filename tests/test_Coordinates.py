import unittest

from src.models.point import Point
from src.models.coordinates import Coordinates


class testCoordinates(unittest.TestCase):
    def setUp(self):
        self.point = Point(3.0, 1.5)
        self.point_bis = Point(2.0, 3.5)

    def test_translated(self):
        result = Coordinates.translated(self.point, 0.5, 0.8)
        self.assertEqual(result.x, 3.5)
        self.assertEqual(result.y, 2.3)

    def test_scaled(self):
        result = Coordinates.scaled(self.point, 1.5, 2.0)
        self.assertEqual(result.x, 4.5)
        self.assertEqual(result.y, 3.0)

    def test_horiz_vert(self):
        start = Point(1.0, 1.0)

        result = Coordinates.horiz_vert(start, self.point)
        self.assertEqual(result.x, 3.0)
        self.assertEqual(result.y, 1.0)

        result_bis = Coordinates.horiz_vert(start, self.point_bis)
        self.assertEqual(result_bis.x, 1.0)
        self.assertEqual(result_bis.y, 3.5)

    def test_distance(self):
        result = Coordinates.distance(self.point, self.point_bis)
        self.assertEqual(result, 2.23606797749979)

    def test_relative_to_origine(self):
        origin = Point(2.0, 1.5)
        result = Coordinates.relative_to_origin(origin, self.point)
        self.assertEqual(result.x, 1.0)
        self.assertEqual(result.y, 0.0)
