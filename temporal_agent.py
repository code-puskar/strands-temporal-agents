import os
from datetime import datetime, timedelta
from temporalio import activity, workflow
from temporalio.common import RetryPolicy
from config import OLLAMA_HOST, OLLAMA_MODEL, FILE_TIMEOUT, TIME_TIMEOUT, CHAT_TIMEOUT, DEFAULT_RETRIES, TIME_RETRIES


@activity.defn
async def read_file_activity(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"File not found: {path}"
    except Exception as e:
        return f"Error: {str(e)}"


@activity.defn
async def list_files_activity(directory: str = ".") -> str:
    try:
        files = os.listdir(directory)
        return "\n".join(files)
    except Exception as e:
        return f"Error: {str(e)}"


@activity.defn
async def get_time_activity() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@activity.defn
async def strands_chat_activity(prompt: str) -> str:
    try:
        # Import Strands only in activity, not at module level
        from strands import Agent
        from strands.models.ollama import OllamaModel
        
        agent = Agent(
            model=OllamaModel(host=OLLAMA_HOST, model_id=OLLAMA_MODEL),
            system_prompt="You are a helpful assistant."
        )
        
        result = agent(prompt)
        
        if hasattr(result, 'content'):
            return str(result.content)
        elif hasattr(result, 'text'):
            return str(result.text)
        else:
            return str(result)
            
    except Exception as e:
        return f"Error: {str(e)}"


@workflow.defn
class TemporalAgentWorkflow:
    
    @workflow.run
    async def run(self, task: str) -> str:
        task_lower = task.lower()
        
        if "read file" in task_lower:
            filename = task.split()[-1]
            return await workflow.execute_activity(
                read_file_activity,
                filename,
                start_to_close_timeout=timedelta(seconds=FILE_TIMEOUT),
                retry_policy=RetryPolicy(maximum_attempts=DEFAULT_RETRIES)
            )
        
        if "list files" in task_lower:
            return await workflow.execute_activity(
                list_files_activity,
                ".",
                start_to_close_timeout=timedelta(seconds=FILE_TIMEOUT),
                retry_policy=RetryPolicy(maximum_attempts=DEFAULT_RETRIES)
            )
        
        if "time" in task_lower:
            return await workflow.execute_activity(
                get_time_activity,
                start_to_close_timeout=timedelta(seconds=TIME_TIMEOUT),
                retry_policy=RetryPolicy(maximum_attempts=TIME_RETRIES)
            )
        
        return await workflow.execute_activity(
            strands_chat_activity,
            task,
            start_to_close_timeout=timedelta(seconds=CHAT_TIMEOUT),
            retry_policy=RetryPolicy(
                maximum_attempts=DEFAULT_RETRIES,
                initial_interval=timedelta(seconds=1),
                maximum_interval=timedelta(seconds=10)
            )
        )
