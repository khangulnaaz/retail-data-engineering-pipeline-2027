import logging
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Logs directory
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Log file path
LOG_FILE = LOG_DIR / "pipeline.log"

# Logging configuration
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Create logger
logger = logging.getLogger("RetailPipeline")