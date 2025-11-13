import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from config import TEMPORAL_HOST, TASK_QUEUE
from temporal_agent import (
    TemporalAgentWorkflow,
    read_file_activity,
    list_files_activity,
    get_time_activity,
    strands_chat_activity
)


async def create_worker():
    client = await Client.connect(TEMPORAL_HOST)
    
    return Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[TemporalAgentWorkflow],
        activities=[
            read_file_activity,
            list_files_activity,
            get_time_activity,
            strands_chat_activity
        ]
    )


async def main():
    worker = await create_worker()
    print(f"Worker started on {TASK_QUEUE}")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
