"""
Utility functions for healthcare fraud detection project.
Includes logging, configuration, and helper functions.
"""

import logging
import os
from pathlib import Path
from typing import Optional


def setup_logging(log_level=logging.INFO, log_file: Optional[str] = None):
    """
    Configure logging for the project.
    
    Args:
        log_level: Logging level (default INFO)
        log_file: Optional log file path
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(),
        ]
    )
    
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(log_format))
        logging.getLogger().addHandler(file_handler)


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def ensure_directory_exists(directory: str):
    """Create directory if it doesn't exist."""
    Path(directory).mkdir(parents=True, exist_ok=True)


def load_config(config_file: str = None) -> dict:
    """
    Load configuration from file or environment.
    
    Args:
        config_file: Path to config file (optional)
    
    Returns:
        Configuration dictionary
    """
    config = {
        'random_state': int(os.getenv('RANDOM_STATE', 42)),
        'test_size': float(os.getenv('TEST_SIZE', 0.2)),
        'model_type': os.getenv('MODEL_TYPE', 'random_forest'),
        'n_estimators': int(os.getenv('N_ESTIMATORS', 200)),
        'max_depth': int(os.getenv('MAX_DEPTH', 15)),
    }
    return config


def print_section(title: str, width: int = 70):
    """Pretty print a section header."""
    print("\n" + "="*width)
    print(title.center(width))
    print("="*width)


def memory_usage_summary():
    """Print memory usage summary."""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    
    print(f"\nMemory Usage:")
    print(f"  RSS: {memory_info.rss / 1024 / 1024:.2f} MB")
    print(f"  VMS: {memory_info.vms / 1024 / 1024:.2f} MB")
