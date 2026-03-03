"""
Configuration Manager
Handles API keys and trading parameters
"""

import os
import json
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class TradingConfig:
    """Trading configuration parameters"""
    initial_capital: float = 30000.0
    max_position_size: float = 0.05  # 5% per trade
    min_otm_percent: float = 10.0
    max_otm_percent: float = 15.0
    min_delta: float = 0.20
    max_delta: float = 0.35
    min_dte: int = 7
    max_dte: int = 14
    min_weekly_yield: float = 0.007
    min_open_interest: int = 200
    earnings_buffer_days: int = 7

class ConfigManager:
    """Manages configuration and API keys"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.path.expanduser("~/.kelvin/config.json")
        self.trading_config = TradingConfig()
        self._api_keys: Dict[str, str] = {}
    
    def load_from_env(self):
        """Load API keys from environment variables"""
        self._api_keys = {
            'tradier': os.getenv('TRADIER_TOKEN', ''),
            'finnhub': os.getenv('FINNHUB_TOKEN', ''),
            'marketaux': os.getenv('MARKETAUX_TOKEN', '')
        }
        return self
    
    def load_from_file(self) -> bool:
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
                self._api_keys = data.get('api_keys', {})
                
                # Load trading config if present
                if 'trading' in data:
                    for key, value in data['trading'].items():
                        if hasattr(self.trading_config, key):
                            setattr(self.trading_config, key, value)
                return True
        except FileNotFoundError:
            return False
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.config_path}")
            return False
    
    def save_to_file(self):
        """Save configuration to JSON file"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        data = {
            'api_keys': self._api_keys,
            'trading': {
                'initial_capital': self.trading_config.initial_capital,
                'max_position_size': self.trading_config.max_position_size,
                'min_otm_percent': self.trading_config.min_otm_percent,
                'max_otm_percent': self.trading_config.max_otm_percent,
                'min_delta': self.trading_config.min_delta,
                'max_delta': self.trading_config.max_delta,
                'min_dte': self.trading_config.min_dte,
                'max_dte': self.trading_config.max_dte,
                'min_weekly_yield': self.trading_config.min_weekly_yield,
                'min_open_interest': self.trading_config.min_open_interest,
            }
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_api_key(self, name: str) -> Optional[str]:
        """Get API key by name"""
        return self._api_keys.get(name)
    
    def set_api_key(self, name: str, value: str):
        """Set API key"""
        self._api_keys[name] = value
    
    def validate(self) -> bool:
        """Check if required API keys are present"""
        required = ['tradier', 'finnhub']
        return all(self._api_keys.get(key) for key in required)

if __name__ == "__main__":
    # Demo
    config = ConfigManager()
    config.load_from_env()
    
    if config.validate():
        print("✓ Configuration valid")
        print(f"  Tradier key: {config.get_api_key('tradier')[:10]}...")
        print(f"  Finnhub key: {config.get_api_key('finnhub')[:10]}...")
    else:
        print("✗ Missing required API keys")
        print("  Set TRADIER_TOKEN and FINNHUB_TOKEN environment variables")
