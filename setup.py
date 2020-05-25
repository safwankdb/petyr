import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="petyr", # Replace with your own username
    version="0.0.1",
    author="Mohd Safwam",
    author_email="kdbeatbox@gmail.com",
    description="2D Geometric Transforms",
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