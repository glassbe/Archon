from pydantic_ai import Agent, RunContext
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated, List, Any, Dict, Optional
from langgraph.config import get_stream_writer
from langgraph.types import interrupt
from dotenv import load_dotenv
import os
import sys
import uuid
from langsmith import Client
from langchain_core.tracers.langchain import wait_for_all_tracers

# Load environment variables
load_dotenv()

# Initialize model names
reasoner_model = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229") if os.getenv("ANTHROPIC_API_KEY") else os.getenv("OPENAI_MODEL", "gpt-4")
planner_model = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229") if os.getenv("ANTHROPIC_API_KEY") else os.getenv("OPENAI_MODEL", "gpt-4")

# Define the state for our agent
class AgentState(TypedDict):
    latest_user_message: str
    messages: List[dict]
    project_scope: str
    development_plan: str

# Reasoner Node: Analyze project requirements and define scope
async def define_scope_with_reasoner(state: AgentState):
    """
    Analyze the user's project description and define the scope of the project.
    This is the first step in our workflow.
    """
    # Get the stream writer function
    stream_writer = get_stream_writer()
    
    # Create a Reasoner agent
    reasoner = Agent(
        model=reasoner_model,
        system_prompt="""You are an expert software project analyst. Your job is to analyze the user's project description 
        and define a clear scope for the project. Extract key information such as:
        
        1. Project goals and objectives
        2. Target users/audience
        3. Key features and functionalities
        4. Technical constraints or requirements
        5. Integration points with other systems
        6. Potential challenges or risks
        
        Provide a comprehensive but concise analysis that will help a development planner create a detailed project plan.
        """
    )
    
    # Process the user's message
    result = await reasoner.run(state["latest_user_message"])
    # Extract the data from the AgentRunResult object
    state["project_scope"] = result.data if hasattr(result, 'data') else str(result)
    
    # Add messages to the state
    state["messages"] = [
        {"role": "system", "content": "I'll analyze your project requirements and create a development plan."},
        {"role": "user", "content": state["latest_user_message"]},
        {"role": "assistant", "content": f"First, let me analyze your project requirements:\n\n{result}"}
    ]
    
    # Stream the response
    if stream_writer:
        stream_writer(f"First, let me analyze your project requirements:\n\n{result}")
    
    return state

# Planner Node: Create a detailed development plan
async def create_development_plan(state: AgentState):
    """
    Create a detailed development plan based on the project scope.
    This is the second step in our workflow.
    """
    # Get the stream writer function
    stream_writer = get_stream_writer()
    
    # Create a Planner agent
    planner = Agent(
        model=planner_model,
        system_prompt="""You are an expert software development planner. Your job is to create a comprehensive 
        development plan based on the project scope provided. Your plan should include:
        
        1. Project phases (e.g., Discovery, Design, Development, Testing, Deployment)
        2. Detailed milestones for each phase
        3. Specific tasks and sub-tasks
        4. Time estimates for each task
        5. Resource requirements and allocation
        6. Dependencies between tasks
        7. Risk mitigation strategies
        8. Testing and quality assurance approach
        9. Deployment strategy
        
        Format your plan in a clear, structured manner that can be easily followed by a development team.
        """
    )
    
    # Process the project scope
    result = await planner.run(state["project_scope"])
    # Extract the data from the AgentRunResult object
    state["development_plan"] = result.data if hasattr(result, 'data') else str(result)
    
    # Add messages to the state
    state["messages"] = state["messages"] + [
        {"role": "assistant", "content": f"Based on this analysis, here's a detailed development plan for your project:\n\n{result}"}
    ]
    
    # Stream the response
    if stream_writer:
        stream_writer(f"\n\nBased on this analysis, here's a detailed development plan for your project:\n\n{result}")
    
    return state

# Interrupt the graph to get the user's next message
def get_next_user_message(state: AgentState):
    """
    Interrupt the graph to get the user's next message.
    This allows for interactive refinement of the plan.
    """
    # Return a dictionary with the interrupt message
    return {"latest_user_message": interrupt("What do you think of this plan? Would you like me to refine any part of it?")}

# Route the user's message
def route_user_message(state: AgentState):
    """
    Determine if the user wants to refine the plan or finish the conversation.
    """
    # Check if user's message indicates they want to refine the plan
    # Include both English and German keywords
    refine_keywords_en = ["refine", "change", "update", "modify", "adjust", "improve", "revise", "add", "details", "more"]
    refine_keywords_de = ["verfeinern", "ändern", "aktualisieren", "anpassen", "verbessern", "überarbeiten", 
                         "hinzufügen", "details", "mehr", "könntest", "bitte", "danke für", "würde", "gerne", 
                         "wissen", "datensicherheit", "datenschutz", "implementierung", "priorisieren"]
    
    user_msg = state["latest_user_message"].lower()
    
    # Check for keywords in both languages
    has_refine_keywords = any(keyword in user_msg for keyword in refine_keywords_en + refine_keywords_de)
    
    # Check for question marks or request patterns
    has_question = '?' in user_msg
    has_request_pattern = any(pattern in user_msg for pattern in ["könntest du", "kannst du", "bitte", "ich möchte", "ich würde"])
    
    # If the message is longer than 20 words, it's likely a detailed request rather than a simple acknowledgment
    is_detailed_message = len(user_msg.split()) > 20
    
    # Route to refine_plan if any of these conditions are met
    if has_refine_keywords or has_question or has_request_pattern or is_detailed_message:
        return "refine_plan"
    else:
        return "finish_conversation"

# Refine the development plan based on user feedback
async def refine_plan(state: AgentState):
    """
    Refine the development plan based on user feedback.
    """
    # Get the stream writer function
    stream_writer = get_stream_writer()
    
    # Create a Refiner agent
    refiner = Agent(
        model=planner_model,
        system_prompt="""You are an expert software development planner. You've already created a development plan,
        and now the user has provided feedback. Your job is to refine the plan based on this feedback.
        
        Maintain the overall structure of the plan, but make specific adjustments based on the user's requests.
        Be clear about what changes you're making and why.
        """
    )
    
    # Prepare context with original plan and user feedback
    context = f"Original plan:\n{state['development_plan']}\n\nUser feedback:\n{state['latest_user_message']}"
    
    # Process the refinement request
    result = await refiner.run(context)
    # Extract the data from the AgentRunResult object
    state["development_plan"] = result.data if hasattr(result, 'data') else str(result)
    
    # Add messages to the state
    state["messages"] = state["messages"] + [
        {"role": "user", "content": state["latest_user_message"]},
        {"role": "assistant", "content": f"I've refined the development plan based on your feedback:\n\n{result}"}
    ]
    
    # Stream the response
    if stream_writer:
        stream_writer(f"I've refined the development plan based on your feedback:\n\n{result}")
    
    return state

# Finish the conversation
async def finish_conversation(state: AgentState):
    """
    Wrap up the conversation with final instructions.
    """
    # Get the stream writer function
    stream_writer = get_stream_writer()
    
    final_message = """
    Thank you for using the Development Plan Agent! You now have a comprehensive plan for your software project.
    
    Next steps:
    1. Share this plan with your development team
    2. Set up project management tools (like Jira, Trello, or GitHub Projects)
    3. Schedule regular check-ins to track progress against the plan
    4. Be prepared to adapt the plan as you learn more during development
    
    Good luck with your project!
    """
    
    # Add messages to the state
    state["messages"] = state["messages"] + [
        {"role": "user", "content": state["latest_user_message"]},
        {"role": "assistant", "content": final_message}
    ]
    
    # Stream the response
    if stream_writer:
        stream_writer(final_message)
    
    return state

# Build workflow
builder = StateGraph(AgentState)

# Add nodes
builder.add_node("define_scope_with_reasoner", define_scope_with_reasoner)
builder.add_node("create_development_plan", create_development_plan)
builder.add_node("get_next_user_message", get_next_user_message)
builder.add_node("refine_plan", refine_plan)
builder.add_node("finish_conversation", finish_conversation)

# Set edges
builder.add_edge(START, "define_scope_with_reasoner")
builder.add_edge("define_scope_with_reasoner", "create_development_plan")
builder.add_edge("create_development_plan", "get_next_user_message")
builder.add_conditional_edges(
    "get_next_user_message",
    route_user_message,
    {"refine_plan": "refine_plan", "finish_conversation": "finish_conversation"}
)
builder.add_edge("refine_plan", "get_next_user_message")
builder.add_edge("finish_conversation", END)

# Configure persistence
memory = MemorySaver()

# # Configure tracing for visualization
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
# os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
# os.environ["LANGCHAIN_PROJECT"] = "dev-plan-agent"

# Compile the graph with tracing
dev_plan_flow = builder.compile(
    checkpointer=memory,
    name="Development Plan Agent",
    # tracing=os.getenv("LANGCHAIN_API_KEY") is not None
)

# # Function to get the LangSmith URL for the trace
# def get_langsmith_url(run_id: Optional[str]) -> Optional[str]:
#     """Get the LangSmith URL for a run."""
#     if not run_id or not os.getenv("LANGCHAIN_API_KEY"):
#         return None
    
#     client = Client()
#     try:
#         run_info = client.read_run(run_id)
#         trace_url = f"https://smith.langchain.com/o/{run_info.project_name}/runs/{run_id}?trace=true"
#         return trace_url
#     except Exception as e:
#         print(f"Error getting LangSmith URL: {e}")
#         return None
