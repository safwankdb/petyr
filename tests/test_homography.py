from petyr import Homography, Affine, Transformation2D, Similarity
import numpy as np
import unittest


class TestHomography(unittest.TestCase):

    def test_from_elements(self):
        A = [1, 2, 3, 4, 5, 6, 7, 8]
        a = Homography.from_elements(A)
        A = np.array(A + [1]).reshape(3, 3)
        np.testing.assert_array_almost_equal(A, a.numpy())

    def test_from_points(self):
        p = np.random.rand(10, 2)
        a = Homography.from_elements([1, 0.1, 2, 0.1, 1, 3, 0.1, 0.2])
        q = a * p
        b = Homography.from_points(p, q)
        np.testing.assert_array_almost_equal(a.numpy(), b.numpy())
    
    def test_mul(self):
        a = Homography().rotate(30).translate(2, 2)

        b = Similarity().scale(1.5).rotate(10).translate(1,2)
        c = a * b
        self.assertIsInstance(c, Homography)
        np.testing.assert_array_almost_equal(c.numpy(), a.numpy() @ b.numpy())

        b = Affine().shear(10, 20).scale(1, 2)
        c = a * b
        self.assertIsInstance(c, Homography)
        np.testing.assert_array_almost_equal(c.numpy(), a.numpy() @ b.numpy())
        
        b = Transformation2D().shear(10, 20).scale(1, 2)
        c = a * b
        self.assertIsInstance(c, Transformation2D)
        np.testing.assert_array_almost_equal(c.numpy(), a.numpy() @ b.numpy())
        
        b = Homography().shear(10, 20).scale(1, 2)
        c = a * b
        self.assertIsInstance(c, Homography)
        np.testing.assert_array_almost_equal(c.numpy(), a.numpy() @ b.numpy())
