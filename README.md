# petyr

Affine and Projective transformations for Python 3. Fast and chainable operations.

## Install
```bash
pip3 install petyr
```
```python
from petyr import Affine
```
## Applying Transformation
```python
p = np.array([[0,0],[1,0],[1,1],[0,1]]).T
rotate_45 = Affine().rotate(90).translate(2,1)
print(rotate_45)
```
```
3x3 Affine Transformation
[[ 0. -1.  2.]
 [ 1.  0.  1.]
 [ 0.  0.  1.]]
```

```python
q = rotate_45 * p
print(q)
```
```
[[2. 2. 1. 1.]
 [1. 2. 2. 1.]]
```
## Finding Transformation
```python
Affine().from_points(p,q)
```
```
3x3 Affine Transformation
[[-0. -1.  2.]
 [ 1.  0.  1.]
 [ 0.  0.  1.]]
```

## Basic Operations

### Translation
```python
at = Affine()
at.translate(tx=1, ty=3)
```
```
3x3 Affine Transformation
[[1. 0. 2.]
 [0. 1. 3.]
 [0. 0. 1.]]
```
### Scaling
```python
at = Affine()
at.scale(1.05, 2)
```
```
3x3 Affine Transformation
[[1.05 0.   0.  ]
 [0.   2.   0.  ]
 [0.   0.   1.  ]]
 ```
 ### Rotation
 ```python
at = Affine()
at.rotate(45)
```
```
3x3 Affine Transformation
[[ 0.707 -0.707  0.   ]
 [ 0.707  0.707  0.   ]
 [ 0.     0.     1.   ]]
```
### Shearing
```python
at = Affine()
at.shear(10, 45)
```
```
3x3 Affine Transformation
[[1.    0.176 0.   ]
 [1.    1.    0.   ]
 [0.    0.    1.   ]]
```
## Operation Chaining
Mutiple operations can be chained together.
```python
at = Affine()
at.scale(2,2).rotate(90)
at.shear(10, 0).translate(-3, 4)
```
```
3x3 Affine Transformation
[[ 0.353 -2.    -3.   ]
 [ 2.     0.     4.   ]
 [ 0.     0.     1.   ]]
```
Multiple transforms can be multiplied together.
```python
a = Affine()
a.translate(2,3)
b = Affine()
b.scale(4,5)
a * b
```
```
3x3 Affine Transformation
[[4. 0. 2.]
 [0. 5. 3.]
 [0. 0. 1.]]
```


