import os

# Temporal configuration
TEMPORAL_HOST = os.getenv("TEMPORAL_HOST", "localhost:7233")
TASK_QUEUE = "strands-temporal-agent-queue"

# Ollama configuration  
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")

# Timeouts (seconds)
FILE_TIMEOUT = 30
TIME_TIMEOUT = 10
CHAT_TIMEOUT = 120

# Retry settings
DEFAULT_RETRIES = 3
TIME_RETRIES = 2
