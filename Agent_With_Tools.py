from typing import TypedDict, Annotated
from langgraph.graph import StateGraph
from langgraph.graph import StateGraph,START, END
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

class CalculatorInput(BaseModel):
    expression: str = Field(
        description="A mathematical expression to evaluate which is valid in python math expression eval function, e.g., '2 + 2 * (3 - 1)'"
    )

llm = ChatOllama(model="qwen3:1.7b", temperature=0)

class State(TypedDict):
    input : str
    messages: Annotated[list, add_messages]
    response: str




class FinalResponse(BaseModel):
    answer: str
    tools_used: str
    confidence: str

structured_llm = llm.with_structured_output(FinalResponse)


@tool
def knowledge_lookup(query: str) -> str:
    """Perform a knowledge lookup based on the query."""
    knowledge_base = {
        "What is the capital of France?": "The capital of France is Paris.",
        "Who is the president of the United States?": "As of 2024, the president of the United States is Joe Biden.",
        "What is the largest mammal?": "The largest mammal is the blue whale.",
        "ai": "Artificial Intelligence is the simulation of human intelligence by machines.",
        "python": "Python is a high level programming language known for simplicity.",
        "langgraph": "LangGraph is a library for building stateful multi-actor applications with LLMs."
    
    }
    query_lower = query.lower()
    for key, value in knowledge_base.items():
        if key in query_lower:
            return value
    
    return f"No specific information found for: {query}"





@tool (args_schema=CalculatorInput)
def calculator_tool(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        # WARNING: Using eval can be dangerous. In production, consider using a safe math parser.
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"
    

@tool
def date_tool() -> str:
    """
    Returns the current date and time.
    Use this when the user asks about today's date or current time.
    This tool requires NO input arguments.
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

builder = StateGraph(State)

tools = [knowledge_lookup, calculator_tool, date_tool]
llm_with_tools = llm.bind_tools(tools)

def agent_node(state: State) -> State:
    system = SystemMessage(content="""You are a helpful assistant with access to these tools:
    - calculator_tool: for ANY math calculations
    - date_tool: for current date and time (NO arguments needed)
    - knowledge_lookup: for general knowledge questions
    For date/time questions, call date_tool with NO arguments.""")
    if not state["messages"]:
        messages = [system, HumanMessage(content=state["input"])]
    else:
        messages = [system] + list(state["messages"])
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


def should_continue(state) -> str:
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return "tools"
    return END

#-----------------------------------------------------------------------------------
tool_node = ToolNode(tools)

builder.add_node("agent", agent_node)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

builder.add_edge("tools", "agent")

graph = builder.compile()




#-------------------------------------
#Use

if __name__ == "__main__":
    initial_state = {
        "input": "What is the capital of France? and also, what is today's date?",
        "messages": []
    }
    final_state = graph.invoke(initial_state)
    print("Final State:", final_state)
    print("--------------------------------------------------------------------------------------------------------------------------------------------")
    print("Final Answer:", final_state['messages'][-1].content)