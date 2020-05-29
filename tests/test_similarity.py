from petyr import Similarity, Affine, Transformation2D, Homography
import numpy as np
import unittest


class TestSimilarity(unittest.TestCase):

    def test_from_points(self):
        p = np.random.rand(10, 2)
        a = Similarity().translate(2, 3).rotate(45).scale(2)
        q = a * p
        b = Similarity.from_points(p, q)
        np.testing.assert_array_almost_equal(a.numpy(), b.numpy())

    def test_from_elements(self):
        A = [1, 2, 3, 4]
        a = Similarity.from_elements(A)
        A = np.array([1,-2,3,2,1,4,0,0,1]).reshape(3, 3)
        np.testing.assert_array_almost_equal(A, a.numpy())

    def test_mul(self):
        a = Similarity().rotate(30).translate(2, 2)
        b = Affine().shear(10, 20).scale(1, 2)
        c = a * b
        self.assertIsInstance(c, Affine)
        np.testing.assert_array_almost_equal(c.numpy(), a.numpy() @ b.numpy())
        b = Transformation2D().shear(10, 20).scale(1, 2)
        c = a * b
        self.assertEqual(type(c), Transformation2D)
        np.testing.assert_array_almost_equal(c.numpy(), a.numpy() @ b.numpy())
        b = Homography().shear(10, 20).scale(1, 2)
        c = a * b
        self.assertIsInstance(c, Homography)
        np.testing.assert_array_almost_equal(c.numpy(), a.numpy() @ b.numpy())
    
    def test_shear(self):
        self.assertRaises(AttributeError, Similarity.shear, 4)
