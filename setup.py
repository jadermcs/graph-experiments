from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("src/shingles.pyx",
                            language_level = "3")
)

from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext


ext_modules = [
        Extension("shingles",
            ["shingles.pyx"],
            extra_compile_args = ["-O3", "-march=native" ],
            language="c++")
        ]
setup(name="agg_cyth_pure",cmdclass = {'build_ext': build_ext}, ext_modules=ext_modules,)
