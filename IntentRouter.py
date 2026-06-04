from typing import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph import StateGraph,START, END

class State(TypedDict):
    input : str
    intent: str
    response: str



def router(state: State) -> State:
    text = state["input"].lower()

    if any(word in text for word in ["hello", "hi", "hey"]):
        intent = "greet"
    

    elif any(op in text for op in ["+", "-", "*", "/", "x"]) or \
         any(char.isdigit() for char in text):
        intent = "math"


    else:
        intent = "general"

    return {"intent": intent}

def cleanAndGreet(state: State) -> State:
   
    return {"response": f"Hello, ! Welcome to AI Lab!"}

def mathNode(state: State) -> State:
    try:
        expression = state["input"].lower().replace("x", "*")
        result = eval(expression)
        return {"response": f"The result of {state['input']} is {result}."}
    except Exception as e:
        return {"response": "Sorry, I couldn't evaluate that expression. Please use format like: 5 + 5"}
    

def general_node(state: State) -> State:
    return {"response": f"You asked: '{state['input']}'. This is a general query — try connecting an LLM here on Day 3!"}




def decisionMaker(state: State) -> State:
    return state["intent"]

builder = StateGraph(State)


builder.add_node("router", router)
builder.add_node("cleanAndGreet", cleanAndGreet)
builder.add_node("mathNode", mathNode)
builder.add_node("general_node", general_node)


builder.add_edge(START, "router")


builder.add_conditional_edges(
    "router",
    decisionMaker,
    {
        "greet": "cleanAndGreet",
        "math": "mathNode",
        "general": "general_node"
    }
)


builder.add_edge("cleanAndGreet", END)
builder.add_edge("mathNode", END)
builder.add_edge("general_node", END)

graph = builder.compile()

result = graph.invoke({"input": "Other"})
print(result["response"])
