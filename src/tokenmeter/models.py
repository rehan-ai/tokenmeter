import json
import requests
from typing import Dict, Any, Optional
import os

class ModelManager:
    PRICING_URL = "https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json"
    LOCAL_JSON_PATH = "model_pricing.json"

    def __init__(self):
        self.model_data: Dict[str, Any] = {}
        self._load_pricing_data()

    def _load_pricing_data(self, force_download: bool = False) -> None:
        """Load pricing data, either from local file or by downloading."""
        if not force_download and os.path.exists(self.LOCAL_JSON_PATH):
            self._load_local_pricing_data()
        else:
            self._download_pricing_data()

    def _load_local_pricing_data(self) -> None:
        """Load pricing data from local JSON file."""
        try:
            with open(self.LOCAL_JSON_PATH, 'r') as f:
                self.model_data = json.load(f)
            print("Loaded pricing data from local file.")
        except FileNotFoundError:
            print("Local pricing data file not found. Downloading from source.")
            self._download_pricing_data()
        except json.JSONDecodeError:
            print("Error decoding local JSON file. Downloading from source.")
            self._download_pricing_data()

    def _download_pricing_data(self) -> None:
        """Download the latest pricing and context information from GitHub."""
        try:
            response = requests.get(self.PRICING_URL)
            response.raise_for_status()
            self.model_data = response.json()
            
            # Save the data locally
            with open(self.LOCAL_JSON_PATH, 'w') as f:
                json.dump(self.model_data, f, indent=2)
            
            print("Pricing data downloaded and saved successfully.")
        except requests.RequestException as e:
            print(f"Error downloading pricing data: {e}")
            if not self.model_data:  # If download fails and we don't have any data, raise an exception
                raise

    def update_pricing_data(self) -> None:
        """Force update the pricing data from the source."""
        self._download_pricing_data()

    def get_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve information for a specific model."""
        return self.model_data.get(model_name)

    def get_input_price(self, model_name: str) -> Optional[float]:
        """Get the input price per token for a specific model."""
        model_info = self.get_model_info(model_name)
        return model_info.get('input_cost_per_token') if model_info else None

    def get_output_price(self, model_name: str) -> Optional[float]:
        """Get the output price per token for a specific model."""
        model_info = self.get_model_info(model_name)
        return model_info.get('output_cost_per_token') if model_info else None

    def get_max_tokens(self, model_name: str) -> Optional[int]:
        """Get the maximum number of tokens for a specific model."""
        model_info = self.get_model_info(model_name)
        return model_info.get('max_tokens') if model_info else None

    def get_max_input_tokens(self, model_name: str) -> Optional[int]:
        """Get the maximum number of input tokens for a specific model."""
        model_info = self.get_model_info(model_name)
        return model_info.get('max_input_tokens') if model_info else None

    def get_max_output_tokens(self, model_name: str) -> Optional[int]:
        """Get the maximum number of output tokens for a specific model."""
        model_info = self.get_model_info(model_name)
        return model_info.get('max_output_tokens') if model_info else None

    def supports_function_calling(self, model_name: str) -> bool:
        """Check if a model supports function calling."""
        model_info = self.get_model_info(model_name)
        return model_info.get('supports_function_calling', False) if model_info else False

    def supports_vision(self, model_name: str) -> bool:
        """Check if a model supports vision tasks."""
        model_info = self.get_model_info(model_name)
        return model_info.get('supports_vision', False) if model_info else False

    def get_provider(self, model_name: str) -> Optional[str]:
        """Get the provider for a specific model."""
        model_info = self.get_model_info(model_name)
        return model_info.get('litellm_provider') if model_info else None

    def list_available_models(self) -> list[str]:
        """List all available models."""
        return list(self.model_data.keys())

    def update_pricing_data(self) -> None:
        """Update the pricing data from the source."""
        self.download_pricing_data()

# Usage example
if __name__ == "__main__":
    manager = ModelManager()
    manager.download_pricing_data()
    
    # Example usage of methods
    model_name = "gpt-4"
    print(f"Input price for {model_name}: {manager.get_input_price(model_name)}")
    print(f"Output price for {model_name}: {manager.get_output_price(model_name)}")
    print(f"Max tokens for {model_name}: {manager.get_max_tokens(model_name)}")
    print(f"Supports function calling: {manager.supports_function_calling(model_name)}")
    print(f"Provider: {manager.get_provider(model_name)}")