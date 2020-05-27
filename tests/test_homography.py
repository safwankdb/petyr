from petyr import Homography
import numpy as np
import unittest


class TestHomography(unittest.TestCase):

    def test_from_elements(self):
        A = [1, 2, 3, 4, 5, 6, 7, 8]
        a = Homography.from_elements(A)
        A = np.array(A + [1]).reshape(3, 3)
        np.testing.assert_array_almost_equal(A, a.M)

    def test_from_points(self):
        p = np.random.rand(10, 2)
        a = Homography.from_elements([1, 0.1, 2, 0.1, 1, 3, 0.1, 0.2])
        q = a * p
        b = Homography.from_points(p, q)
        np.testing.assert_array_almost_equal(a.M, b.M)
