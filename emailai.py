from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model="qwen3:1.7b", temperature=0.7)





class State(TypedDict):
    EmailTopic: str
    draft: str
    Approved: bool
    output: str




def GenerateEmail(state: State) -> State:
    print("Generating Email Draft")


    system = SystemMessage(content="""You are an email Writer
                          Write clear, concise and professional emails.
                            Always include:
                            - Subject line
                            - Greeting 
                            - Body 1 (intent)
                            - Body 2 (action) --if and only if required
                            - Sign off (From Nisharg Patel, AI Engineer Trainee, Aditi Tech Consulting)
                            Keep it under 150 words.""") 
   
    human = HumanMessage(content=f"""Write a professional email about {state['EmailTopic']}""")


    draft = ""

    for chunk in llm.stream([system, human]):
        print(chunk.content, end="", flush=True)
        draft += chunk.content
    
    print("\n")  
    
    return {"draft": draft}


def ApprovalNode(state: State) -> State:
    print("\n" + "=" * 50)
    print("EMAIL DRAFT FOR REVIEW:")
    print("=" * 50)
    print(state["draft"])
    print("=" * 50)
    
    while True:
        decision = input("\nApprove and send? (Y/N): ").strip().upper()
        
        if decision == "Y":
            print("\nApproved! Sending email...")
            return {"Approved": True}
        
        elif decision == "N":
            print("\nRejected! Stopping workflow...")
            return {"Approved": False}
        
        else:
            print("Invalid input. Please enter Y or N.")


def rejected_node(state: State) -> State:
    print("\n─" * 50)
    print("Email was rejected.")
    print("Workflow stopped. No email was sent.")
    print("─" * 50)
    
    return {"final": "Email rejected by human. Not sent."}


def SendEmail(state: State) -> State:
    print("\n📤 Sending email...")
    print("─" * 50)

    print("Email sent successfully!")
    print("─" * 50)
    print(f"Final Email:\n{state['draft']}")
    
    return {"final": f"Email sent successfully:\n\n{state['draft']}"}

builder = StateGraph(State)


builder.add_node("generate_email", GenerateEmail)
builder.add_node("human_approval", ApprovalNode)
builder.add_node("send_email", SendEmail)
builder.add_node("rejected", rejected_node)

builder.add_edge(START, "generate_email")
builder.add_edge("generate_email", "human_approval")


def should_send(state: State) -> str:
    if state["Approved"]:
        return "send_email"
    return "rejected"



builder.add_conditional_edges(
    "human_approval",
    should_send,
    {
        "send_email": "send_email",
        "rejected":   "rejected"
    }
)

builder.add_edge("send_email", END)
builder.add_edge("rejected", END)

graph = builder.compile()




if __name__ == "__main__":
    print("=" * 50)
    print("📬 Email Approval Workflow")
    print("=" * 50)
    
    topic = input("\nWhat should the email be about?\n→ ").strip()
    
    if not topic:
        topic = "Request a team meeting for project updates"
    
    initial_state = {
        "EmailTopic": topic,
        "draft": "",
        "Approved": False,
        "output": ""
    }
    
    final_state = graph.invoke(initial_state)
    
    # Final output
    print("\n" + "=" * 50)
    print("WORKFLOW COMPLETE")
    print("=" * 50)
    print(f"Topic:    {final_state['EmailTopic']}")
    print(f"Approved: {final_state['Approved']}")
    print(f"Outcome:  {final_state['output'][:60]}...")