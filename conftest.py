import sys
import os

# Add the src directory and the root directory to the Python path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
src_dir = os.path.join(root_dir, 'src')
sys.path.insert(0, root_dir)
sys.path.insert(0, src_dir)
