from pathlib import Path
import sys


SIMULATION_SRC = Path(__file__).resolve().parents[1] / "src"

if str(SIMULATION_SRC) not in sys.path:
    sys.path.insert(0, str(SIMULATION_SRC))
