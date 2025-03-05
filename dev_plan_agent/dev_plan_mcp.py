import os
import sys
import asyncio
import threading
import requests
from typing import Dict, List
import uuid

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.utils import write_to_log
from mcp.server.fastmcp import FastMCP
from dev_plan_service import app
import uvicorn

# Initialize FastMCP server
mcp = FastMCP("dev_plan")

# Store active threads
active_threads: Dict[str, List[str]] = {}

# FastAPI service URL
SERVICE_PORT = int(os.getenv("SERVICE_PORT", "8200"))
DEV_PLAN_SERVICE_URL = f"http://127.0.0.1:{SERVICE_PORT}"

@mcp.tool()
async def create_thread() -> str:
    """Create a new conversation thread for the Development Plan Agent.
    Always call this tool before invoking the agent for the first time in a conversation.
    (if you don't already have a thread ID)
    
    Returns:
        str: A unique thread ID for the conversation
    """
    thread_id = str(uuid.uuid4())
    active_threads[thread_id] = []
    write_to_log(f"Created new thread for dev plan agent: {thread_id}")
    return thread_id

def _make_request(thread_id: str, user_input: str, config: dict) -> str:
    """Make synchronous request to dev plan service"""
    response = requests.post(
        f"{DEV_PLAN_SERVICE_URL}/invoke",
        json={
            "message": user_input,
            "thread_id": thread_id,
            "is_first_message": not active_threads[thread_id],
            "config": config
        }
    )
    response.raise_for_status()
    return response.json()

@mcp.tool()
async def run_agent(thread_id: str, user_input: str) -> str:
    """Run the Development Plan Agent with user input.
    Only use this tool after you have called create_thread in this conversation to get a unique thread ID.
    If you already created a thread ID in this conversation, do not create another one. Reuse the same ID.
    
    Args:
        thread_id: The conversation thread ID
        user_input: The user's message about their software project
    
    Returns:
        str: The agent's response which includes the development plan
    """
    if thread_id not in active_threads:
        write_to_log(f"Error: Thread not found - {thread_id}")
        raise ValueError("Thread not found")

    write_to_log(f"Processing message for dev plan thread {thread_id}: {user_input}")

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    
    try:
        result = await asyncio.to_thread(_make_request, thread_id, user_input, config)
        active_threads[thread_id].append(user_input)
        return result['response']
        
    except Exception as e:
        raise

def run_service():
    """Run the FastAPI service in a separate thread"""
    uvicorn.run(app, host="127.0.0.1", port=SERVICE_PORT)

if __name__ == "__main__":
    write_to_log("Starting Development Plan MCP server")
    
    # Start the service in a separate thread
    service_thread = threading.Thread(target=run_service, daemon=True)
    service_thread.start()
    
    # Run MCP server
    mcp.run(transport='stdio')
