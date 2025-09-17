# app/__main__.py
import sys
from pathlib import Path

# Directories
REPO_ROOT = Path(__file__).resolve().parent.parent      # Main Repo Directory
sys.path.insert(0, str(REPO_ROOT))                      # Assign REPO ROOT as Directory 0 for Import searches

# Launch app
from app.app import main
main()