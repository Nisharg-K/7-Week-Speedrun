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
    #Keep last 3 messages in the conversation history to prevent context overflow
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
    
    # This lives OUTSIDE the graph
    # and carries state between turns
    state = {"messages": []}
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Add human message to state
        state["messages"].append(HumanMessage(content=user_input))
        
        # Run graph for one turn
        state = graph.invoke(state)
        
        # Print last AI response
        last_message = state["messages"][-1]
        print(f"Bot: {last_message.content}\n")



        #AI - Supersmart Coder having all knowledge of this code
        #Human - Taking help of this AI

        #AI: I am a memory chatbot?
        #Human: Does this code allows the bot to remember last 3 messages? or all messages?
        #AI: This code allows the bot to remember all messages in the conversation history. The state maintains a list of all messages, and the chatbot can refer to this history when responding to user inputs.
        #Human: So why there is a function called keep_last_3? Does it have any role in the current code?
        #AI: The function keep_last_3 is defined in the code but is not currently used anywhere. It seems to be a utility function that takes an existing list of messages and a new message, combines them, and returns only the last three messages. However, since it is not called or integrated into the current chatbot logic, it does not have any role in the current code. The chatbot as implemented will remember all messages in the conversation history without limiting it to the last three.
        #Human: If I want to modify the code to only remember the last 3 messages, how can I integrate the keep_last_3 function into the chat_node?
        #AI: To modify the code to only remember the last 3 messages, you can integrate the keep_last_3 function into the chat_node function. Here's how you can do it:
