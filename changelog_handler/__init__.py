import importlib.metadata

__version__ = importlib.metadata.version(__package__)
__all__ = []

from .version import *
__all__ += version.__all__

from .changelog import *
__all__ += changelog.__all__
