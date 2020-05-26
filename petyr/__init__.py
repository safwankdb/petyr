# -*- coding: utf-8 -*-

import numpy as np


class Affine:

    def __init__(self, M=None):
        if M is None:
            self.M = np.eye(3)
        else:
            self.M = M
        return

    @classmethod
    def from_elements(cls, A):
        """
        Params:
        A - array of 6 numbers describing an affine transform
        """
        assert len(A) == 6, "A should have exactly 6 elements"
        M = np.array(A+[0, 0, 1]).reshape(3, 3)
        return cls(M)

    @classmethod
    def from_points(cls, src, dst):
        '''
        Params:
        src - source points. 2xN array [x1, y1; x2, y2; ...]
        dst - destination points. same shape as src
        '''
        assert src.shape == dst.shape, "src and dst should have same shape"
        assert src.shape[1] == 2, "src and dst should be Nx2 arrays"
        n = src.shape[0]
        x = np.ones((3, n))
        x[:2, :] = src.T
        X = np.zeros((2*n, 6))
        for i in range(n):
            X[2*i, :3] = x[:, i]
            X[2*i+1, 3:] = x[:, i]
        dst = dst.reshape(-1, 1)
        A = np.linalg.lstsq(X, dst, rcond=None)[0]
        return cls.from_elements(list(A.ravel()))

    def __repr__(self):
        return "Affine(\n" + str(self.M.round(3)) + ')'

    def __mul__(self, x):
        if isinstance(x, np.ndarray):
            return self.apply(x)
        elif isinstance(x, Affine):
            M = self.M @ x.M
            return self.__class__(M)
        else:
            raise NotImplementedError(
                "Send a PR at the github repo if necessary")

    def det(self):
        det = np.linalg.det(self.M[:2, :2])
        return det

    def is_degenerate(self):
        det = self.det()
        return det == 0

    def apply(self, x):
        '''
        Apply the transform

        Params:
        x - Nx2 array [x1, y1; x2, y2; ...]

        Returns:
        y - Nx2 array [x1', y1'; x2', y2'; ...]
        '''
        assert x.ndim == 2 and x.shape[1] == 2, "x should be an Nx2 array"
        X = np.ones((3, x.shape[0]))
        X[:2, :] = x.T
        y = self.M @ X
        return y[:2, :].T

    def translate(self, tx=0, ty=0):
        """
        Params:
        t_x - translation in x
        t_y - translation in y
        """
        self.M[0, 2] += tx
        self.M[1, 2] += ty
        return self

    def scale(self, s_x=1, s_y=1):
        """
        Params:
        s_x - scale factor in x
        s_y - scale factor in y
        """
        assert s_x * s_y != 0, "Scale factors should be non zero"
        self.M[0, :] *= s_x
        self.M[1, :] *= s_y
        return self

    def rotate(self, theta, degrees=True):
        '''
        Params:
        theta - angle to rotate anti-clockwise by in degrees
        '''
        if degrees:
            theta = np.radians(theta)
        c = np.cos(theta)
        s = np.sin(theta)
        M = np.eye(3)
        M[0, 0] = c
        M[0, 1] = -s
        M[1, 0] = s
        M[1, 1] = c
        self.M = M @ self.M
        return self

    def shear(self, theta_x=0, theta_y=0, degrees=True):
        '''
        Params:
        theta_x - shearing angle with y axis
        theta_y - shearing angle with x axis
        '''
        if degrees:
            theta_x, theta_y = np.radians((theta_x, theta_y))
        M = np.eye(3)
        M[0, 0] = 1
        M[0, 1] = np.tan(theta_x)
        M[1, 0] = np.tan(theta_y)
        M[1, 1] = 1
        self.M = M @ self.M
        return self

    def invert(self):
        '''
        Return the inverse transform
        '''
        if self.is_degenerate():
            raise ValueError("Non Invertible Matrix")
        M = np.linalg.inv(self.M)
        return self.__class__(M)
