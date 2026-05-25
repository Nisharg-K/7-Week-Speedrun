from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_ollama import OllamaLLM

search = DuckDuckGoSearchRun()

topic = input("Please enter your research topic: ")

llm = OllamaLLM(model="qwen2.5:1.5b")

class GraphState(TypedDict):
    topic: str
    search_results: str
    final_report: str


def resercher_node(state: GraphState):
    print("===================Researcher working===================")
    output = search.run(topic)
    return {"search_results": "Search results for " + state["topic"] + ": " + output}

def writer_node(state: GraphState):
    print("===================Writer working===================")
    llmresp = llm.invoke("Based on the following search results, please create a final report: " + state["search_results"])
    return {"final_report": llmresp}

workflow = StateGraph(GraphState)

workflow.add_node("researcher", resercher_node)
workflow.add_node("writer", writer_node)

workflow.add_edge(START, "researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", END)

app = workflow.compile()


final_state = app.invoke({"topic": topic})

print("====================Final Report===================")
print(final_state["final_report"])