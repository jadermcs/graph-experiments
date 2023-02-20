from setuptools import setup
from Cython.Build import cythonize

setup(
    name = "shingles",
    ext_modules = cythonize("src/shingles.pyx",
                            language_level = "3"))
