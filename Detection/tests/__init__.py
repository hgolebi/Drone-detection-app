import os, sys
current = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current)
sys.path.append(os.path.dirname(current))
sys.path.append(os.path.dirname(os.path.dirname(current)))
test_files_dir = os.path.join(os.path.dirname(__file__), 'files')