import httpx
import asyncio

async def send_a2a_task():
    url = "http://127.0.0.1:8000/message/send"
    task_data = {
        "task_id": "12345",
        "params": {"a": 50, "b": 1200},
        "description": "Add two numbers using the agent's tools."
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=task_data)
            response.raise_for_status()
            print("Successfully sent A2A task.")
            print("Agent's response:", response.json())
    except httpx.HTTPStatusError as e:
        print(f"Error sending task: {e}")

if __name__ == "__main__":
    asyncio.run(send_a2a_task())