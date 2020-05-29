import numpy as np


class Transformation2D:
    '''
    3x3 2D Geometric Transformation
    '''

    def __init__(self, M=None):
        if M is None:
            self._M = np.eye(3)
        else:
            if type(M) is not np.ndarray:
                raise TypeError("Input a 3x3 numpy array")
            if M.shape != (3, 3):
                raise ValueError("Input a 3x3 numpy array")
            M = M.copy()
            self._M = M / M[2, 2]

    def __repr__(self):
        return "{}(\n{})".format(type(self).__name__, self._M.round(3))

    @classmethod
    def from_elements(cls, *args):
        '''
        Params:
        A - array of 9 numbers describing a general transform
        '''
        A = np.asarray(args[0]) if len(args) == 1 else np.asarray(args)
        assert len(A) == 9, "A should have exactly 9 elements"
        M = np.array(A).reshape(3, 3)
        return cls(M)

    def copy(self):
        return self.__class__(self._M)

    def __mul__(self, x):
        if isinstance(x, np.ndarray):
            return self.apply(x)
        elif isinstance(x, Transformation2D):
            M = self._M @ x._M
            return self.__class__(M)
        else:
            raise NotImplementedError(
                "Send a PR at the github repo if necessary")

    def __invert__(self):
        return self.invert()

    def det(self):
        det = np.linalg.det(self._M)
        return det

    def is_degenerate(self):
        det = self.det()
        return det == 0

    def numpy(self):
        return self._M.copy()

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
        y = self._M @ X
        y = y / y[2:, :]
        return y[:2, :].T

    def reset(self):
        '''
        Resets to the identity transform
        '''
        self._M = np.eye(3)
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
        self._M = M @ self._M
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
        self._M = M @ self._M
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
        self._M = M @ self._M
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
        self._M = M @ self._M
        return self

    def invert(self):
        '''
        Return the inverse transform
        '''
        if self.is_degenerate():
            raise ValueError("Non Invertible Matrix")
        M = np.linalg.inv(self._M)
        return self.__class__(M)


class Similarity(Transformation2D):
    '''
    3x3 Similarity Transform
    '''

    def __mul__(self, x):
        if isinstance(x, np.ndarray):
            return self.apply(x)
        elif isinstance(x, Transformation2D):
            M = self._M @ x._M
            return type(x)(M)
        else:
            raise NotImplementedError(
                "Send a PR at the github repo if necessary")

    @classmethod
    def from_elements(cls, *args):
        '''
        Params:
        A - array of 4 numbers describing a similarity transform
        '''
        A = np.asarray(args[0]) if len(args) == 1 else np.asarray(args)
        assert len(A) == 4, "*args should have exactly 4 elements"
        a, b, c, d = A
        M = np.array([a, -b, c, b, a, d, 0, 0, 1]).reshape(3, 3)
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
        assert n >= 2, "need atleast 2 points to compute"
        x1 = np.hstack([src[:, :1], -src[:, 1:], np.ones((n, 1))])
        x2 = np.hstack([src, np.ones((n, 1))])
        X = np.zeros((2*n, 4))
        r = np.arange(n)
        X[2*r, 1:] = x1
        X[2*r+1, :3] = x2[:, ::-1]
        dst = dst.reshape(-1, 1)
        A = np.linalg.lstsq(X, dst, rcond=None)[0].ravel()
        d, a, b, c = A
        return cls.from_elements(a, b, c, d)

    def scale(self, s):
        '''
        Uniform Scaling
        Scales with factors s in both x and y.
        Params:
        s - scale factor
        '''
        return super().scale(s, s)

    def shear(self, *args):
        '''
        Raises Error
        '''
        raise AttributeError(
            "Similarity Transform does not involve shearing, Use petyr.Affine instead")


class Affine(Transformation2D):
    '''
    3x3 Affine Transform
    '''

    def __mul__(self, x):
        if isinstance(x, np.ndarray):
            return self.apply(x)
        elif isinstance(x, Similarity):
            M = self._M @ x._M
            return self.__class__(M)
        elif isinstance(x, Transformation2D):
            M = self._M @ x._M
            return type(x)(M)
        else:
            raise NotImplementedError(
                "Send a PR at the github repo if necessary")

    @classmethod
    def from_elements(cls, *args):
        '''
        Params:
        A - array of 6 numbers describing an affine transform
        '''
        A = np.asarray(args[0]) if len(args) == 1 else np.asarray(args)
        assert len(A) == 6, "A should have exactly 6 elements"
        M = np.concatenate([A, [0, 0, 1]]).reshape(3, 3)
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
        x = np.hstack([src, np.ones((n, 1))])
        X = np.zeros((2*n, 6))
        r = np.arange(n)
        X[2*r, :3] = x
        X[2*r+1, 3:] = x
        dst = dst.reshape(-1, 1)
        A = np.linalg.lstsq(X, dst, rcond=None)[0]
        return cls.from_elements(list(A.ravel()))


class Homography(Transformation2D):
    '''
    3x3 Homography
    '''

    def __mul__(self, x):
        if isinstance(x, np.ndarray):
            return self.apply(x)
        elif isinstance(x, (Similarity, Affine)):
            M = self._M @ x._M
            return self.__class__(M)
        elif isinstance(x, Transformation2D):
            M = self._M @ x._M
            return type(x)(M)
        else:
            raise NotImplementedError(
                "Send a PR at the github repo if necessary")

    @classmethod
    def from_elements(cls, *args):
        '''
        Params:
        H - array of 8 numbers describing an affine transform
        '''
        H = np.asarray(args[0]) if len(args) == 1 else np.asarray(args)
        assert len(H) == 8, "H should have exactly 8 elements"
        M = np.concatenate([H, [1]]).reshape(3, 3)
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
        r = np.arange(n)
        P[2*r, :3] = -x1
        P[2*r, 6:] = x1
        P[2*r+1, 3:6] = -x1
        P[2*r+1, 6:] = x1
        P[:, 6:] *= x2
        _, _, vh = np.linalg.svd(P)
        A = vh[-1, :].reshape(3, 3)
        A = A / A[2, 2]
        return cls.from_elements(list(A.ravel())[:8])
