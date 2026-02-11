import yaml
import os
from pathlib import Path
from typing import Dict, List, Optional
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.topics: Dict[str, Dict] = {}
        self.topic_descriptions: Dict[str, List[str]] = {}
        self.default_agent: Optional[str] = None
        self.load_config()

    def _substitute_env_vars(self, value: str) -> str:
        """Substitute environment variables in a string."""
        def replace_var(match):
            var_name = match.group(1)
            return os.getenv(var_name, match.group(0))
        
        return re.sub(r'\${([^}]+)}', replace_var, value)

    def load_config(self):
        """Load configuration from YAML file."""
        config_path = Path(self.config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(config_path) as f:
            config = yaml.safe_load(f)

        # Process topics
        for topic, data in config.get("topics", {}).items():
            self.topics[topic] = {
                "route": self._substitute_env_vars(data["route"])
            }
            self.topic_descriptions[topic] = data.get("descriptions", [])

        # Process default agent
        self.default_agent = self._substitute_env_vars(config.get("default_agent", ""))
        if not self.default_agent:
            raise ValueError("default_agent must be specified in config")

    def get_agent_url(self, topic: str) -> str:
        """Get the agent URL for a given topic."""
        return self.topics.get(topic, {}).get("route", self.default_agent)

    def get_topic_descriptions(self) -> Dict[str, List[str]]:
        """Get all topic descriptions."""
        return self.topic_descriptions 