from langgraph.graph import StateGraph, START, END
from app.agents.state import AgentState
from app.agents.router import router_agent
from app.agents.constitution_agent import constitution_agent
from app.agents.case_law_agent import case_law_agent
from app.agents.reasoning_agent import reasoning_agent
from app.agents.validation_agent import validation_agent
from app.agents.verdict_agent import verdict_agent

# Initialize StateGraph using the shared AgentState structure
workflow = StateGraph(AgentState)

# Add pass-through trigger node to fan-out/split parallel flow
def retrieval_trigger(state: AgentState):
    return {}

# Add nodes to the graph
workflow.add_node("router", router_agent)
workflow.add_node("retrieval_trigger", retrieval_trigger)
workflow.add_node("constitution_agent", constitution_agent)
workflow.add_node("case_law_agent", case_law_agent)
workflow.add_node("reasoning_agent", reasoning_agent)
workflow.add_node("validation_agent", validation_agent)
workflow.add_node("verdict_agent", verdict_agent)

# Set entry point
workflow.add_edge(START, "router")

# Define conditional logic based on router decision
def route_decision(state: AgentState) -> str:
    val_res = state.get("validation_result") or {}
    if val_res.get("action") == "stop" or state.get("detected_legal_issue") == "Non-Legal":
        # Bypass retrieval & reasoning nodes, go directly to Verdict Agent to formulate off-topic notice
        return "stop"
    return "continue"

# Route conditionally to retrieval trigger or direct stop
workflow.add_conditional_edges(
    "router",
    route_decision,
    {
        "continue": "retrieval_trigger",
        "stop": "verdict_agent"
    }
)

# Connect the trigger to Constitution Agent, then Case Law Agent, then Reasoning Agent
workflow.add_edge("retrieval_trigger", "constitution_agent")
workflow.add_edge("constitution_agent", "case_law_agent")
workflow.add_edge("case_law_agent", "reasoning_agent")

# Connect the rest of the flow sequentially
workflow.add_edge("reasoning_agent", "validation_agent")
workflow.add_edge("validation_agent", "verdict_agent")
workflow.add_edge("verdict_agent", END)

# Compile the workflow graph
agent_workflow = workflow.compile()
