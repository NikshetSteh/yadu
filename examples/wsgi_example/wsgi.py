import sys

path = '/path/to/application'
if path not in sys.path:
    sys.path.append(path)

# noinspection PyUnresolvedReferences
from main import application
