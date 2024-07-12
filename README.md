# TokenMeter

TokenMeter is a Python library for calculating and estimating costs associated with using various language models. It provides tools for token counting, cost calculation, and includes integration with OpenAI's API.

## Features

- Calculate costs for language model usage based on input and output tokens
- Estimate costs before making API calls
- Retrieve model information including pricing and token limits
- Integrated OpenAI API handler for easy response generation
- Utility functions for token counting, text truncation, and text splitting

## Installation

You can install TokenMeter using pip:

```bash
pip install tokenmeter
```

## Usage

Here are some basic usage examples:

```python
from tokenmeter import TokenMeter, calculate_cost, estimate_cost, get_model_info, use_openai

# Initialize TokenMeter
tm = TokenMeter()

# Calculate cost for a completed interaction
model_name = "gpt-3.5-turbo"
prompt = "Tell me a joke about programming."
response = "Why do programmers prefer dark mode? Because light attracts bugs!"
cost = tm.calculate_cost(model_name, prompt, response)
print(f"Actual cost: ${cost['total_cost']:.6f}")

# Estimate cost before making an API call
estimated_output_tokens = 50
estimated_cost = tm.estimate_cost(model_name, prompt, estimated_output_tokens)
print(f"Estimated cost: ${estimated_cost['total_cost']:.6f}")

# Get model information
model_info = tm.get_model_info(model_name)
print(f"Model info: {model_info}")


# You can also use the convenience functions directly
direct_cost = calculate_cost(model_name, prompt, response)
print(f"Direct cost calculation: ${direct_cost['total_cost']:.6f}")
```


## Contributing

Contributions to TokenMeter are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project uses pricing data from [LiteLLM](https://github.com/BerriAI/litellm).
- Token counting is performed using the [tiktoken](https://github.com/openai/tiktoken) library.

## Support

If you encounter any problems or have any questions, please open an issue on the [GitHub repository](https://github.com/rehan-ai/tokenmeter/issues).