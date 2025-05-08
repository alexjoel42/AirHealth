# config.py
import yaml
import os
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    with open("config.yml", "r") as f:
        return yaml.safe_load(f)

# Example usage:
config = load_config()
sensor_port = config["sensor"]["port"]  # Gets "COM3"