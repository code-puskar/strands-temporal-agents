import asyncio
from temporalio.client import Client
from config import TEMPORAL_HOST, TASK_QUEUE
from temporal_agent import TemporalAgentWorkflow


async def execute_task(client, task, task_id):
    try:
        result = await client.execute_workflow(
            TemporalAgentWorkflow.run,
            task,
            id=f"task-{task_id}",
            task_queue=TASK_QUEUE
        )
        return result
    except Exception as e:
        return f"Error: {e}"


async def run_demo():
    client = await Client.connect(TEMPORAL_HOST)
    
    demo_tasks = [
        "What time is it?",
        "List files in current directory", 
        "Read file ../requirements.txt",
        "What is artificial intelligence?"
    ]
    
    for i, task in enumerate(demo_tasks, 1):
        print(f"Task: {task}")
        result = await execute_task(client, task, i)
        print(f"Result: {result}\n")


if __name__ == "__main__":
    asyncio.run(run_demo())
