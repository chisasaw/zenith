# src/agents/base_agent.py
import logging
from typing import Dict, Any
import pandas as pd  # Ensure pandas is properly imported 

class BaseAgent:
    def __init__(self, name: str, config_path: str):
        self.name = name
        self.config_path = config_path
        self.state = "initialized"
        self.last_update = None
        self.config = self.load_config()
        
        # Set up logging
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from a file."""
        # Placeholder for configuration loading logic.
        return {}

    def validate_message(self, message: Dict[str, Any]) -> bool:
        """Validate an incoming message."""
        required_keys = ["type", "data"]
        for key in required_keys:
            if key not in message:
                self.logger.warning(f"Invalid message: missing {key}")
                return False
        return True

    def create_signal(self, signal_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a structured signal."""
        return {
            "type": signal_type,
            "data": data,
            "timestamp": pd.Timestamp.now()
        }

    def get_status(self) -> Dict[str, Any]:
        """Get the status of the agent."""
        return {
            "name": self.name,
            "state": self.state,
            "last_update": self.last_update
        }
