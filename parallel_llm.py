from typing import TypedDict, Annotated
from langgraph.graph import StateGraph
from langgraph.graph import StateGraph,START, END
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

class State(TypedDict):
    input: str
    benefits: str
    risks: str
    alternatives: str
    combinedOutput: str

llm = ChatOllama(model="qwen3:1.7b", temperature=0.7)

def analyzeBenefits(state: State) -> State:
    system = SystemMessage(content="""You are a helpful assistant that analyzes the benefits of a given topic. 
                          Provide a concise list of benefits in bullet points.""") 
   
    human = HumanMessage(content=f"""Analyze the benefits of {state['input']}.""")

    benefits = ""

    for chunk in llm.stream([system, human]):
        print(chunk.content, end="", flush=True)
        benefits += chunk.content
    
    print("\n")  
    
    return {"benefits": benefits}

def analyzeRisks(state: State) -> State:
    system = SystemMessage(content="""You are a helpful assistant that analyzes the risks of a given topic. 
                          Provide a concise list of risks in bullet points.""") 
   
    human = HumanMessage(content=f"""Analyze the risks of {state['input']}.""")

    risks = ""

    for chunk in llm.stream([system, human]):
        print(chunk.content, end="", flush=True)
        risks += chunk.content
    
    print("\n")  
    
    return {"risks": risks}

def analyzeAlternatives(state: State) -> State:
    system = SystemMessage(content="""You are a helpful assistant that analyzes the alternatives of a given topic. 
                          Provide a concise list of alternatives in bullet points.""") 
   
    human = HumanMessage(content=f"""Analyze the alternatives to {state['input']}.""")

    alternatives = ""

    for chunk in llm.stream([system, human]):
        print(chunk.content, end="", flush=True)
        alternatives += chunk.content
    
    print("\n")  
    
    return {"alternatives": alternatives}

def combineOutputs(state: State) -> State:
    system = SystemMessage(content="""You are an expert AI research assistant. You have 3 different analyses on a topic: benefits, risks, and alternatives.
    Your task is to combine these analyses into a single, concise summary that highlights the key points of""") 
   
    human = HumanMessage(content=f"""combine and summarize the different aspects of this topic : {state['input']}. Here are the benefits: {state['benefits']}. Here are the risks: {state['risks']}. Here are the alternatives: {state['alternatives']}.""")

    combined = ""

    for chunk in llm.stream([system, human]):
        print(chunk.content, end="", flush=True)
        combined += chunk.content
    
    print("\n")  
    
    return {"combinedOutput": combined}


builder = StateGraph(State)

builder.add_node("analyzeBenefits", analyzeBenefits)
builder.add_node("analyzeRisks", analyzeRisks)
builder.add_node("analyzeAlternatives", analyzeAlternatives)
builder.add_node("combineOutputs", combineOutputs)


#Parralel execution of the first 3 nodes
builder.add_edge(START, "analyzeBenefits")
builder.add_edge(START, "analyzeRisks")
builder.add_edge(START, "analyzeAlternatives")

builder.add_edge("analyzeBenefits", "combineOutputs")
builder.add_edge("analyzeRisks", "combineOutputs")
builder.add_edge("analyzeAlternatives", "combineOutputs")

builder.add_edge("combineOutputs", END)

graph = builder.compile()


if __name__ == "__main__":
    topic = input("Enter a topic to analyze: ")
    result = graph.invoke({"input": topic})
    print("\nFinal Summary:")
    print(result["combinedOutput"])