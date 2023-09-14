import sys

path = 'path/to/project'
if path not in sys.path:
    sys.path.append(path)

from main import application
