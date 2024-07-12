from .models import ModelManager
from .calculator import CostCalculator
from .utils import count_tokens, truncate_text, split_text


class TokenMeter:
    def __init__(self):
        self.model_manager = ModelManager()
        self.calculator = CostCalculator()


    def calculate_cost(self, model_name: str, prompt: str, response: str):
        input_tokens = count_tokens(prompt, model_name)
        output_tokens = count_tokens(response, model_name)
        return self.calculator.calculate_cost(model_name, input_tokens, output_tokens)

    def estimate_cost(self, model_name: str, prompt: str, estimated_output_tokens: int):
        return self.calculator.estimate_cost(model_name, prompt, estimated_output_tokens)

    def get_model_info(self, model_name: str):
        return self.model_manager.get_model_info(model_name)


# Convenience functions
def calculate_cost(model_name: str, prompt: str, response: str):
    return TokenMeter().calculate_cost(model_name, prompt, response)

def estimate_cost(model_name: str, prompt: str, estimated_output_tokens: int):
    return TokenMeter().estimate_cost(model_name, prompt, estimated_output_tokens)

def get_model_info(model_name: str):
    return TokenMeter().get_model_info(model_name)
