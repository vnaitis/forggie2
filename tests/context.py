import os
import sys

# Add forggie2/ directory to the search path.
cwd = os.path.abspath(os.path.join(os.path.dirname(__file__)))
path = os.path.join(cwd, '..', 'forggie2')
sys.path.insert(0, path)

import car
import frog
import logger
