import os
from .receip_types import *
import importlib
import sys

# import all parsers
parsers = os.path.join(os.path.dirname(os.path.abspath(__file__)), "parsers")
for name in os.listdir(parsers):
    if name.endswith(".py"):
        sys.path.append(parsers)
        out = importlib.import_module(name[:-3], package=parsers)
