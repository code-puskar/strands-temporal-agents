import os
from datetime import datetime
from strands import Agent, tool
from strands.models.ollama import OllamaModel
from config import OLLAMA_HOST, OLLAMA_MODEL


@tool
def read_file(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"File not found: {path}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def list_files(directory: str = ".") -> str:
    try:
        files = os.listdir(directory)
        return "\n".join(files)
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def get_current_time() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def create_agent():
    return Agent(
        model=OllamaModel(host=OLLAMA_HOST, model_id=OLLAMA_MODEL),
        tools=[read_file, list_files, get_current_time],
        system_prompt="You are a helpful assistant. Give responses in not more than 2-3 lines."
    )


def run_demo():
    agent = create_agent()
    
    demo_tasks = [
        "What time is it?",
        "List files in current directory", 
        "Read file ../requirements.txt",
        "What is artificial intelligence?"
    ]
    
    for task in demo_tasks:
        print(f"Task: {task}")
        try:
            result = agent(task)
            print(f"Result: {result}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    run_demo()
