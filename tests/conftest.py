import sys
import os

# Get the path of the parent directory (NOTE-API)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Insert the parent directory into sys.path
sys.path.insert(0, parent_dir)