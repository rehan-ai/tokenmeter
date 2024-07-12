from typing import Dict, Any, Optional
from .models import ModelManager
from .utils import count_tokens

class CostCalculator:
    def __init__(self, force_download: bool = False):
        self.model_manager = ModelManager()
        if force_download:
            self.model_manager.update_pricing_data()

    def calculate_cost(self, model_name: str, input_tokens: int, output_tokens: int) -> Dict[str, Any]:
        """
        Calculate the cost for a given model usage.
        
        :param model_name: Name of the model
        :param input_tokens: Number of input tokens
        :param output_tokens: Number of output tokens
        :return: Dictionary containing cost breakdown and total
        """
        input_price = self.model_manager.get_input_price(model_name)
        output_price = self.model_manager.get_output_price(model_name)
        
        if input_price is None or output_price is None:
            raise ValueError(f"Pricing information not available for model: {model_name}")
        
        input_cost = input_tokens * input_price
        output_cost = output_tokens * output_price
        total_cost = input_cost + output_cost
        
        return {
            "model": model_name,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": total_cost
        }

    def estimate_cost(self, model_name: str, input_text: str, estimated_output_tokens: int) -> Dict[str, Any]:
        """
        Estimate the cost for a given input and estimated output.
        
        :param model_name: Name of the model
        :param input_text: Input text
        :param estimated_output_tokens: Estimated number of output tokens
        :return: Dictionary containing estimated cost breakdown and total
        """
        from .utils import count_tokens  # Import here to avoid circular import
        
        input_tokens = count_tokens(input_text)
        return self.calculate_cost(model_name, input_tokens, estimated_output_tokens)

    def get_max_cost(self, model_name: str) -> Optional[float]:
        """
        Calculate the maximum possible cost for a full context window.
        
        :param model_name: Name of the model
        :return: Maximum possible cost or None if information is not available
        """
        max_tokens = self.model_manager.get_max_tokens(model_name)
        input_price = self.model_manager.get_input_price(model_name)
        output_price = self.model_manager.get_output_price(model_name)
        
        if max_tokens is None or input_price is None or output_price is None:
            return None
        
        return max_tokens * max(input_price, output_price)

# Usage example
if __name__ == "__main__":
    calculator = CostCalculator()
    
    # Example usage
    model_name = "gpt-4"
    input_tokens = 100
    output_tokens = 50
    
    cost = calculator.calculate_cost(model_name, input_tokens, output_tokens)
    print(f"Cost calculation for {model_name}:")
    print(f"Input tokens: {cost['input_tokens']}")
    print(f"Output tokens: {cost['output_tokens']}")
    print(f"Input cost: ${cost['input_cost']:.6f}")
    print(f"Output cost: ${cost['output_cost']:.6f}")
    print(f"Total cost: ${cost['total_cost']:.6f}")
    
    max_cost = calculator.get_max_cost(model_name)
    print(f"\nMaximum possible cost for {model_name}: ${max_cost:.6f}" if max_cost else f"\nMaximum cost information not available for {model_name}")