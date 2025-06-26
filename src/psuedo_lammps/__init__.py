"""
psuedo-lammps

A lightweight, robust parser for Large Atomic/Molecularly Massive Parallel Simulator(LAMMPS) dump files.
"""

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

__author__ = "Andrew Trepagnier"
__email__ = "andrew.trepagnier@icloud.com"

# Import main functions/classes here
# from .core import main_function
# from .utils import utility_function

__all__ = [
    "__version__",
    # "main_function",
    # "utility_function",
] 