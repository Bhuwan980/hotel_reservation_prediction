import os
import yaml
from src.logger import get_logger

# Create logger instance
logger = get_logger(__name__)

def get_config(file_path):
    """
    Reads a YAML config file and returns its content.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Config file '{file_path}' doesn't exist")

        with open(file_path, 'r') as conf_file:
            config = yaml.safe_load(conf_file)
            logger.info('Successfully loaded the YAML file')
            return config

    except Exception as e:
        logger.error(f"Error reading config file: {e}")
        # Optionally raise the error again or return None
        raise