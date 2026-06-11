from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Annotated, TypedDict
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama


class State(TypedDict):
    messages: Annotated[list, add_messages]

llm  = ChatOllama(model="qwen3:1.7b", temperature=0.7)

async def assistant_node(state: State) -> State:
    system_instruction = SystemMessage(
        content="You are a helpful, professional backend API assistant."
    )
    full_context = [system_instruction] + state["messages"]
    response = await llm.ainvoke(full_context)
    return {"messages": [response]}


workflow = StateGraph(State)
workflow.add_node("assistant", assistant_node)
workflow.add_edge(START, "assistant")
workflow.add_edge("assistant", END)
graph = workflow.compile()


app = FastAPI(title="Day 7: Single-File Chat API")

class ChatInput(BaseModel):
    message: str

class ChatOutput(BaseModel):
    response: str


@app.post("/chat", response_model=ChatOutput)
async def chat_endpoint(payload: ChatInput):
    try:
        # Initialize state with the user's message
        initial_state = {"messages": [HumanMessage(content=payload.message)]}
        
        # Run the graph
        final_state = await graph.ainvoke(initial_state)
        
        # Extract the final response
        last_message = final_state["messages"][-1]
        
        if not isinstance(last_message, AIMessage):
            raise HTTPException(status_code=500, detail="Invalid execution state.")
            
        return ChatOutput(response=str(last_message.content))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)


    