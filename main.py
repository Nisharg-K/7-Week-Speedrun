from typing import TypedDict, Literal
import json
import re
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_core.messages import SystemMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen3:1.7b", temperature=0)

search = DuckDuckGoSearchRun()

@tool
def Web_Search(query: str):
    """Search the web for the given query."""
    return search.run(query)

llm_with_tools = llm.bind_tools([Web_Search])

def extract_thinking(content: str):
    """Separate <think> block from actual response."""
    think_match = re.search(r'<think>(.*?)</think>', content, re.DOTALL)
    if think_match:
        thinking = think_match.group(1).strip()
        clean_content = content.replace(think_match.group(0), "").strip()
        return thinking, clean_content
    return None, content

def stream_text(stream):
    full = ""
    for chunk in stream:
        if chunk.content:
            full += chunk.content

    thinking, clean = extract_thinking(full)
    if thinking:
        print("[Thinking] ------------")
        print(thinking)
        print("\n[Response] ------------")
    print(clean)

def parse_manual_tool_call(content: str):
    """Fallback parser if model outputs raw <tool_call> instead of JSON."""
    match = re.search(r'<tool_call>(.*?)</tool_call>', content, re.DOTALL)
    if match:
        try:
            parsed = json.loads(match.group(1).strip())
            return {"name": parsed["name"], "args": parsed["arguments"], "id": "manual_01"}
        except json.JSONDecodeError:
            return None
    return None

if __name__ == "__main__":
    print("======================= CHAT INTERFACE =======================")
    user_input = input("Enter your question: ")
    messages = [
        SystemMessage(content="""You have access to a Web_Search tool.

When you need to search, respond ONLY with this exact format and nothing else:
<tool_call>
{"name": "Web_Search", "arguments": {"query": "your search query here"}}
</tool_call>

Rules:
- For any current, recent, news-related, or unknown question — use the tool
- Never say "I don't have real-time access"
- Never answer from memory for recent events
- Do not add any explanation before or after the tool call
"""),
        HumanMessage(content=user_input),
    ]

    print(f"\n[Query] {user_input}")

    response = llm_with_tools.invoke(messages)

    # ── Strip thinking from response content before parsing ───────────────────
    thinking, clean_content = extract_thinking(response.content or "")

    if thinking:
        print("\n[Thinking] ------------")
        print(thinking)

    # ── Resolve tool call: native or manual fallback ──────────────────────────
    tool_call = None

    if response.tool_calls:
        tool_call = response.tool_calls[0]
        print(f"\n[Tool Decision] {tool_call['name']} → query: {tool_call['args']}")

    elif "<tool_call>" in clean_content:
        tool_call = parse_manual_tool_call(clean_content)
        if tool_call:
            print(f"\n[Tool Decision - manual] {tool_call['name']} → query: {tool_call['args']}")
        else:
            print("Tool call detected but failed to parse.")

    # ── Execute tool OR print direct answer — ONE place only ─────────────────
    if tool_call and tool_call["name"] == "Web_Search":
        print(f"\n[Tool: Web Search] ------------")
        tool_result = Web_Search.invoke(tool_call["args"])
        print(tool_result)

        messages.append(AIMessage(content=response.content or ""))
        messages.append(ToolMessage(content=str(tool_result), tool_call_id=tool_call["id"]))

        print("\n[Response] ------------")
        stream_text(llm_with_tools.stream(messages))
        print()

    else:
        # Direct answer — already have it, no second LLM call
        print("\n[Response] ------------")
        print(clean_content)