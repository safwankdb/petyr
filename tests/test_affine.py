from petyr import Affine
import numpy as np
import unittest

class TestAffine(unittest.TestCase):

    def test_from_points(self):
        p = np.random.rand(10,2)
        a = Affine().translate(2,3).rotate(45)
        q = a * p
        b = Affine.from_points(p, q)
        np.testing.assert_array_almost_equal(a.M, b.M)

    def test_from_elements(self):
        A = [1,2,3,4,5,6]
        a = Affine.from_elements(A)
        A = np.array(A + [0,0,1]).reshape(3,3)
        np.testing.assert_array_almost_equal(A,a.M)
