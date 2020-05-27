import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="petyr",
    version="0.0.7",
    author="Mohd Safwan",
    author_email="kdbeatbox@gmail.com",
    description="2D Homography and Affine Transformations for Python",
    install_requires=[
        'numpy',
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/safwankdb/petyr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
