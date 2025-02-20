"""Build the Srctools package."""
from setuptools import setup, Extension, find_packages
import sys
import os

WIN = sys.platform.startswith('win')
MAC = sys.platform.startswith('darwin')
root = os.path.dirname(__file__)

# Mandatory in CI!
optional_ext = os.environ.get('CIBUILDWHEEL', '0') != '1'

if WIN:
    openmp = ['/openmp']
elif MAC:
    openmp = []  # Not supported by system Clang.
else:
    openmp = ['-fopenmp']

setup(
    # Setuptools automatically runs Cython, if available.
    ext_modules=[
        Extension(
            "srctools._tokenizer",
            sources=["src/srctools/_tokenizer.pyx"],
            optional=optional_ext,
            extra_compile_args=[
                # '/FAs',  # MS ASM dump
            ],
        ),
        Extension(
            "srctools._cy_vtf_readwrite",
            include_dirs=[os.path.abspath(os.path.join(root, "src", "libsquish"))],
            language='c++',
            optional=optional_ext,
            sources=[
                "src/srctools/_cy_vtf_readwrite.pyx",
                "src/libsquish/alpha.cpp",
                "src/libsquish/clusterfit.cpp",
                "src/libsquish/colourblock.cpp",
                "src/libsquish/colourfit.cpp",
                "src/libsquish/colourset.cpp",
                "src/libsquish/maths.cpp",
                "src/libsquish/rangefit.cpp",
                "src/libsquish/singlecolourfit.cpp",
                "src/libsquish/squish.cpp",
            ],
            extra_compile_args=[
                # '/FAs',  # MS ASM dump
            ] + openmp,
            extra_link_args=openmp,
        ),
        Extension(
            "srctools._math",
            include_dirs=[os.path.abspath(os.path.join(root, "src", "quickhull/"))],
            language='c++',
            optional=optional_ext,
            sources=["src/srctools/_math.pyx", "src/quickhull/QuickHull.cpp"],
            extra_compile_args=[
                # '/FAs',  # MS ASM dump
            ] if WIN else [
                '-std=c++11',  # Needed for Mac to work
            ],
        ),
    ],
    # Here so Github can read it.
    install_requires=[
        "attrs >= 21.2.0",
        "typing_extensions >= 4.1.0"
	    # In stdlib after this.
	    "importlib_resources; python_version < '3.7'",
	    "contextvars; python_version < '3.7'",
	],
)
