from typing import TypedDict, Annotated
from langgraph.graph import StateGraph
from langgraph.graph import StateGraph,START, END
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode


def keep_last_3(existing: list, new: str) -> list:
    combined = existing + [new]
    return combined[-3:]


class State(TypedDict):
    messages: Annotated[list, add_messages]




llm = ChatOllama(model="qwen3:1.7b", temperature=0)

def chat_node(state: State) -> State:
    system = SystemMessage(content="""You are a memory chatbot.
    Remember everything the user tells you in this conversation.
    When asked about previous information always refer to conversation history.
    Be concise and direct in your responses.""")
    messages = [system] + keep_last_3(state["messages"], state["messages"][-1].content)
    
    response = llm.invoke(messages)
    
    return {"messages": [AIMessage(content=response.content)]}



builder = StateGraph(State)

builder.add_node("chat", chat_node)

builder.add_edge(START, "chat")
builder.add_edge("chat", END)

graph = builder.compile()

if __name__ == "__main__":
    print("Memory Chatbot Started!")
    print("Type 'exit' to quit\n")
    
    state = {"messages": []}
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        state["messages"].append(HumanMessage(content=user_input))
                
        state = graph.invoke(state)
        
        last_message = state["messages"][-1]
        print(f"Bot: {last_message.content}\n")

