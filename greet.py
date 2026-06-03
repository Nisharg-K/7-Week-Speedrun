from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class GST(TypedDict):
    name: str
    cleanedName: str
    greetMsg: str



def cleaning(state: GST) -> GST:
    clean = state["name"].strip().title()
    return {"cleanedName": clean}



def greeting(state: GST) -> GST:
    greeting = f"Hello, {state['cleanedName']}!, welcome to AI Lab!"
    return {"greetMsg": greeting}


builder = StateGraph(GST)



builder.add_node("cleaning", cleaning)
builder.add_node("greeting", greeting)

builder.add_edge(START, "cleaning")
builder.add_edge("cleaning", "greeting")
builder.add_edge("greeting", END)


graph = builder.compile()





result = graph.invoke({"name": "john smith"})
print(result["greetMsg"])

