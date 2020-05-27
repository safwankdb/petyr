from petyr import Transformation2D as tf2d
import unittest
import numpy as np


class TestTransformation2D(unittest.TestCase):

    def test_init(self):
        A = [1, 0.1, 3, 0, 1, 4, 0.1, 0.2, 1.05]
        A = np.array(A).reshape(3, 3)
        A[2, 2] = 1
        M = tf2d(A).M
        np.testing.assert_array_almost_equal(M, A)

    def test_from_elements(self):
        A = [1, 2, 3, 1, 2, 3, 1, 2, 3]
        M = tf2d.from_elements(A).M
        A = np.array(A).reshape(3, 3)
        A = A / A[2, 2]
        np.testing.assert_array_almost_equal(M, A)

    def test_translate(self):
        tx, ty = 1.5, 2.5
        b = tf2d().translate(tx, ty)
        A = np.eye(3)
        A[0, 2] = tx
        A[1, 2] = ty
        np.testing.assert_array_almost_equal(b.M, A)

    def test_rotate(self):
        theta = 35 * np.pi/180
        b = tf2d().rotate(theta, degrees=False)
        M = b.M
        self.assertEqual(M[0, 0], M[1, 1])
        self.assertEqual(M[1, 0], -M[0, 1])
        self.assertEqual(np.arccos(M[0, 0]), theta)
        self.assertEqual(np.arcsin(M[1, 0]), theta)

    def test_scale(self):
        s_x, s_y = 1.5, 2.5
        b = tf2d().scale(s_x, s_y)
        self.assertEqual(b.M[0, 0], s_x)
        self.assertEqual(b.M[1, 1], s_y)

    def test_shear(self):
        theta_x, theta_y = 35 * np.pi/180, 65 * np.pi/180
        b = tf2d().shear(theta_x, theta_y, degrees=False)
        self.assertEqual(np.arctan(b.M[0, 1]), theta_x)
        self.assertEqual(np.arctan(b.M[1, 0]), theta_y)

    def test_mul(self):
        a = tf2d().rotate(30).translate(2, 2)
        b = tf2d().shear(10, 20).scale(1, 2)
        c = a * b
        np.testing.assert_array_almost_equal(c.M, a.M @ b.M)

    def test_apply(self):
        p = np.array([[0, 0], [0, 1], [1, 0]])
        a = tf2d().rotate(180).translate(1, 1).scale(2, 3)
        q = a * p
        r = np.array([[2., 3.], [2., 0.], [0., 3.]])
        np.testing.assert_array_almost_equal(r, q)

    def test_invert(self):
        a = tf2d().rotate(180).translate(1, 1).scale(2, 3)
        b = a * a.invert()
        np.testing.assert_array_almost_equal(b.M, np.eye(3))
        a = tf2d.from_elements([0]*8+[1])
        self.assertRaises(ValueError, tf2d.invert, a)

    def test_reset(self):
        a = tf2d().rotate(180).translate(1, 1).scale(2, 3)
        a.reset()
        np.testing.assert_array_almost_equal(a.M, np.eye(3))

    def test_copy(self):
        a = tf2d().rotate(180).translate(1, 1).scale(2, 3)
        b = a.copy()
        np.testing.assert_array_almost_equal(a.M, b.M)
