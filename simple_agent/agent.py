from strands import Agent
from strands.models import OllamaModel
from strands_tools import http_request

# Use local Ollama instance with mistral model
model = OllamaModel(host=None, model_id="mistral")
agent = Agent(model=model, tools=[http_request])

agent("who won the India Pakistan cricket match on 15th February 2026")