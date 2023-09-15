import sys

path = 'path/to/project/folder'
if path not in sys.path:
    sys.path.append(path)

from main import application
