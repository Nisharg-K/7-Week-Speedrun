from typing import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph import StateGraph,START, END
from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen3:1.7b", temperature=0)



class State(TypedDict):
    input : str
    intent: str
    response: str



def router(state: State) -> State:
    response = llm.invoke(
        f"""
        Classifiy the following
        Classify the following input into exactly one category.
        Categories: greeting, math, general
        
        Rules:
        - greeting: any form of hello, hi, hey, welcome
        - math: any mathematical expression or calculation
        - general: anything else
        
        Return only one word (greeting, math, or general). Nothing else.
        Input: {state['input']}
        """,
    )

    intent = response.content.strip().lower()

    if intent not in ["greeting", "math", "general"]:
        intent = "general"

    return {"intent": intent}

def Greet(state: State) -> State:
   response = llm.invoke("""
        Generate a warm and friendly greeting response.
        Keep it short, one sentence only.
        User said: {state["input"]}
    """)
   
   return {"response": response.content.strip()}
def mathNode(state: State) -> State:
    formatted = llm.invoke(f"""
         Convert the following input into a valid Python math expression.
        Return only the expression, nothing else. No explanation.
        
        Examples:
        Input: what is 5 plus 5      → 5 + 5
        Input: 15 times 12           → 15 * 12
        Input: 100 divided by 4      → 100 / 4
        
        Input: {state["input"]}
    """)

    expression = formatted.content.strip()

    try:
        result = eval(expression)
        return {"response": f"The result of {expression} is {result}."}
    except Exception as e:
        return {"response": f"Sorry, I couldn't evaluate the expression: {expression}. Error: {str(e)}"}

def general_node(state: State) -> State:
   
    response = llm.invoke(f"""
        Answer the following question briefly and clearly.
        Keep it to 2-3 sentences max.
        
        Question: {state["input"]}
    """)
    return {"response": response.content.strip()}


def decisionMaker(state: State) -> State:
    return state["intent"]

builder = StateGraph(State)


builder.add_node("router", router)
builder.add_node("Greet", Greet)
builder.add_node("mathNode", mathNode)
builder.add_node("general_node", general_node)


builder.add_edge(START, "router")


builder.add_conditional_edges(
    "router",
    decisionMaker,
    {
        "greeting": "Greet",
        "math": "mathNode",
        "general": "general_node"
    }
)


builder.add_edge("Greet", END)
builder.add_edge("mathNode", END)
builder.add_edge("general_node", END)

graph = builder.compile()

result = graph.invoke({"input": "Hello"})
print(result["response"])
