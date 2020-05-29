from petyr import Affine, Transformation2D, Homography, Similarity
import numpy as np
import unittest


class TestAffine(unittest.TestCase):

    def test_from_points(self):
        p = np.random.rand(10, 2)
        a = Affine().translate(2, 3).rotate(45)
        q = a * p
        b = Affine.from_points(p, q)
        np.testing.assert_array_almost_equal(a.numpy(), b.numpy())

    def test_from_elements(self):
        A = [1, 2, 3, 4, 5, 6]
        a = Affine.from_elements(A)
        A = np.array(A + [0, 0, 1]).reshape(3, 3)
        np.testing.assert_array_almost_equal(A, a.numpy())

    def test_mul(self):
        a = Affine().rotate(30).translate(2, 2)

        b = Similarity().scale(1.5).rotate(10).translate(1,2)
        c = a * b
        self.assertIsInstance(c, Affine)
        np.testing.assert_array_almost_equal(c.numpy(), a.numpy() @ b.numpy())
        
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
