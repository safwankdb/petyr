# -*- coding: utf-8 -*-

import numpy as np

class Affine():

    def __init__(self, M=None):
        if M is None:
            self.M = np.eye(3)
        else:
            self.M = M
        return
    
    def __repr__(self):
        return "3x3 Affine Transformation\n" + str(self.M.round(3))

    def __mul__(self, x):
        if isinstance(x, np.ndarray):
            return self.apply(x)
        elif isinstance(x, Affine):
            M = self.M @ x.M
            return self.__class__(M)
        else:
            raise NotImplementedError("Send a PR at the github repo if necessary")

    def get_det(self):
        self.det = np.linalg.det(self.M[:2,:2])
        return self.det

    def is_degenerate(self):
        self.get_det()
        return self.det > 0

    def apply(self, x):
        '''
        Apply the transform
        
        Params:
        x - 2xN array [x1, x2 ... ; y1, y2 ...]
        '''
        assert x.ndim==2 and x.shape[0]==2, "x should be 2xN array"
        X = np.ones((3,x.shape[1]))
        X[:2,:] = x
        y = self.M @ X
        return y[:2,:]

    def from_elements(self, A):
        """
        Params:
        A - array of 6 numbers describing an affine transform
        """
        assert len(A) == 6, "A should have exactly 6 elements"
        self.M = np.array(A+[0,0,1]).reshape(3,3)
        return self
    
    def from_points(self, src, dst):
        '''
        Params:
        src - source points. 2xN array [x1, x2 ... ; y1, y2 ...]
        dst - destination points. same shape as src
        '''
        assert src.shape == dst.shape, "src and dst should have same shape"
        assert src.shape[0] == 2, "src and dst should be 2*n arrays"
        n = src.shape[1]
        x = np.ones((3, n))
        x[:2,:] = src
        X = np.zeros((2*n, 6))
        for i in range(n):
            X[2*i,:3] = x[:,i]
            X[2*i+1,3:] = x[:,i]
        dst = dst.T.reshape(2*n,1)
        A = np.linalg.lstsq(X, dst, rcond=None)[0].reshape(2,3)
        self.M = np.vstack([A, [0,0,1]])
        return self


    
    def translate(self, tx=0, ty=0):
        """
        Params:
        t_x - translation in x
        t_y - translation in y
        """
        self.M[0,2] += tx
        self.M[1,2] += ty
        return self

    def scale(self, s_x=1, s_y=1):
        """
        Params:
        s_x - translation in x
        s_y - translation in y
        """
        self.M[0,:] *= s_x
        self.M[1,:] *= s_y
        return self

    def rotate(self, theta):
        '''
        Params:
        theta - angle to rotate anti-clockwise by in degrees
        '''
        theta *= np.pi / 180
        c = np.cos(theta)
        s = np.sin(theta)
        M = np.eye(3)
        M[0,0] = c
        M[0,1] = -s
        M[1,0] = s
        M[1,1] = c
        self.M = M @ self.M
        return self
    
    def shear(self, theta_x=0, theta_y=0):
        '''
        Params:
        theta - shearing angle with y axis in degrees
        '''
        theta_x *= np.pi / 180
        theta_y *= np.pi / 180
        M = np.eye(3)
        M[0,0] = 1
        M[0,1] = np.tan(theta_x)
        M[1,0] = np.tan(theta_y)
        M[1,1] = 1
        self.M = M @ self.M
        return self

    def invert(self):
        '''
        Inverses the transform
        '''
        if not self.is_degenerate():
            raise ValueError("Non Invertible Matrix")
        self.M = np.linalg.inv(self.M)
        return self

