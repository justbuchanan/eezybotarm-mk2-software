from __future__ import print_function
import unittest
from circ2_intersect import *
import numpy as np
import sys

class TestCirc2Intersect(unittest.TestCase):

    def test_two_intersections(self):
        intersections = circ2_intersect(
            np.array([0, 0]), 0.7,
            np.array([0, 1]), 0.7,
        )

        self.assertEqual(2, len(intersections))


    def test_zero_intersections(self):
        intersections = circ2_intersect(
            np.array([0, 0]), .1,
            np.array([10, 10]), .1,
        )

        self.assertEqual(None, intersections)

    def test_one_intersection(self):
        intersections = circ2_intersect(
            np.array([0, 0]), 1,
            np.array([0, 2]), 1,
        )

        self.assertEqual(2, len(intersections))
        self.assertItemsEqual(intersections[0], intersections[1])
