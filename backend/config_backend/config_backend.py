from pathlib import Path
import sys
import logging
import logging.config
from rich.logging import RichHandler
import argparse

# Directories
BASE_DIR = Path(__file__).parent.parent.absolute()
CONFIG_DIR = Path(BASE_DIR, "config_backend")
#DATA_DIR = Path(BASE_DIR, "data")

# Create dirs
#DATA_DIR.mkdir(parents=True, exist_ok=True)

#Logging
LOGS_DIR = Path(BASE_DIR, "logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Use config file to initialize logger
logging.config.fileConfig(Path(CONFIG_DIR, "logging.config"))
logger = logging.getLogger()
logger.handlers[0] = RichHandler(markup=True)  # set rich handler
