import numpy as np


class Transformation2D:
    '''
    3x3 2D Geometric Transformation
    '''

    def __init__(self, M=None):
        if M is None:
            self.M = np.eye(3)
        else:
            if type(M) is not np.ndarray:
                raise TypeError("Input a 3x3 numpy array")
            if M.shape != (3,3):
                raise ValueError("Input a 3x3 numpy array")
            M = M.copy()
            self.M = M / M[2, 2]

    def __repr__(self):
        return "Transformation2D(\n{})".format(self.M.round(3))

    @classmethod
    def from_elements(cls, A):
        '''
        Params:
        A - array of 9 numbers describing a general transform
        '''
        assert len(A) == 9, "A should have exactly 9 elements"
        M = np.array(A).reshape(3, 3)
        return cls(M)

    def copy(self):
        return self.__class__(self.M)

    def __mul__(self, x):
        if isinstance(x, np.ndarray):
            return self.apply(x)
        elif isinstance(x, Transformation2D):
            M = self.M @ x.M
            return self.__class__(M)
        else:
            raise NotImplementedError(
                "Send a PR at the github repo if necessary")

    def det(self):
        det = np.linalg.det(self.M)
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
        y = y / y[2:, :]
        return y[:2, :].T

    def reset(self):
        '''
        Resets to the identity transform
        '''
        self.M = np.eye(3)
        return self

    def translate(self, t_x=0, t_y=0):
        '''
        Params:
        t_x - translation in x
        t_y - translation in y
        '''
        M = np.eye(3)
        M[0, 2] = t_x
        M[1, 2] = t_y
        self.M = M @ self.M
        return self

    def scale(self, s_x=1, s_y=1):
        '''
        Scales with factors s_x and s_y.
        Params:
        s_x - scale factor in x
        s_y - scale factor in y
        '''
        assert s_x * s_y != 0, "Scale factors should be non zero"
        M = np.eye(3)
        M[0, 0] = s_x
        M[1, 1] = s_y
        self.M = M @ self.M
        return self

    def rotate(self, theta, degrees=True):
        '''
        Rotates clockwise by angle theta.
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


class Affine(Transformation2D):
    '''
    3x3 Affine
    '''

    def __init__(self, M=None):
        super().__init__(M)

    def __repr__(self):
        return "Affine(\n{})".format(self.M.round(3))

    def __mul__(self, x):
        if isinstance(x, np.ndarray):
            return self.apply(x)
        elif isinstance(x, Affine):
            M = self.M @ x.M
            return Affine(M)
        elif isinstance(x, Homography):
            M = self.M @ x.M
            return Homography(M)
        elif isinstance(x, Transformation2D):
            M = self.M @ x.M
            return Transformation2D(M)
        else:
            raise NotImplementedError(
                "Send a PR at the github repo if necessary")

    @classmethod
    def from_elements(cls, A):
        '''
        Params:
        A - array of 6 numbers describing an affine transform
        '''
        assert len(A) == 6, "A should have exactly 6 elements"
        M = np.array(A+[0, 0, 1]).reshape(3, 3)
        return cls(M)

    @classmethod
    def from_points(cls, src, dst):
        '''
        Params:
        src - source points. Nx2 array [x1, y1; x2, y2; ...]
        dst - destination points. same shape as src
        '''
        assert src.shape == dst.shape, "src and dst should have same shape"
        assert src.shape[1] == 2, "src and dst should be Nx2 arrays"
        n = src.shape[0]
        assert n >= 3, "need atleast 3 non collinear points to compute"
        x = np.ones((3, n))
        x[:2, :] = src.T
        X = np.zeros((2*n, 6))
        for i in range(n):
            X[2*i, :3] = x[:, i]
            X[2*i+1, 3:] = x[:, i]
        dst = dst.reshape(-1, 1)
        A = np.linalg.lstsq(X, dst, rcond=None)[0]
        return cls.from_elements(list(A.ravel()))


class Homography(Transformation2D):
    '''
    3x3 Homography
    '''

    def __init__(self, M=None):
        super().__init__(M)

    def __repr__(self):
        return "Homography(\n{})".format(self.M.round(3))

    @classmethod
    def from_elements(cls, H):
        '''
        Params:
        H - array of 8 numbers describing an affine transform
        '''
        assert len(H) == 8, "H should have exactly 8 elements"
        M = np.array(H+[1]).reshape(3, 3)
        return cls(M)

    @classmethod
    def from_points(cls, src, dst):
        '''
        Params:
        src - source points. Nx2 array [x1, y1; x2, y2; ...]
        dst - destination points. same shape as src
        '''
        assert src.shape == dst.shape, "src and dst should have same shape"
        assert src.shape[1] == 2, "src and dst should be Nx2 arrays"
        n = src.shape[0]
        assert n >= 4, "need atleast 4 points to compute"
        n = len(src)
        x1 = np.ones((n, 3))
        x1[:, :2] = src
        x2 = dst.reshape(2*n, 1)
        P = np.zeros((2*n, 9))
        for i in range(n):
            P[2*i, :3] = -x1[i, :]
            P[2*i, 6:] = x1[i, :]
            P[2*i+1, 3:6] = -x1[i, :]
            P[2*i+1, 6:] = x1[i, :]
        P[:, 6:] *= x2
        _, _, vh = np.linalg.svd(P)
        A = vh[-1, :].reshape(3, 3)
        A = A / A[2, 2]
        return cls.from_elements(list(A.ravel())[:8])
