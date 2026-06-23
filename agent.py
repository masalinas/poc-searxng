import httpx
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent  # más estable que create_agent ahora mismo

SEARXNG_HOST = "http://localhost:8888"

@tool
def academic_search(query: str) -> str:
    """Search for peer-reviewed scientific papers and academic literature
    on computer science, sensor fusion, and human activity recognition."""
    try:
        response = httpx.get(
            f"{SEARXNG_HOST}/search",
            params={
                "q": query,
                "format": "json",
                "categories": "science",
                "language": "en",
            },
            timeout=15.0,
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return f"Search error: {e}"

    results = data.get("results", [])[:4]
    if not results:
        return "No results found."

    formatted = []
    for r in results:
        engines      = ", ".join(r.get("engines", [])) or "unknown"
        published    = r.get("publishedDate") or "unknown"
        score        = r.get("score")
        score_str    = f"{score:.3f}" if score is not None else "n/a"
        category     = r.get("category") or "n/a"

        entry = (
            f"Title:     {r.get('title', 'No title')}\n"
            f"Link:      {r.get('url', 'No URL')}\n"
            f"Engines:   {engines}\n"
            f"Published: {published}\n"
            f"Score:     {score_str}\n"
            f"Category:  {category}\n"
            f"Snippet:   {r.get('content', 'No snippet')[:300]}"
        )
        formatted.append(entry)

    return "\n\n---\n\n".join(formatted)

# qwen2.5:7b es mucho mejor en tool calling que llama3.1:8b
llm = ChatOllama(
    model="qwen2.5:7b",
    temperature=0,
    # SIN format="json"
)

agent = create_react_agent(
    model=llm,
    tools=[academic_search],
    prompt=(
        "You are an academic research assistant. "
        "Use the academic_search tool to find papers, then write a clear summary. "
        "For each paper mentioned, always include its title, link, and the search engines that found it. "
        "After receiving tool results, ALWAYS write a final text response."
    ),
)

query_task = (
    "Search for recent papers on Multimodal Human Activity Recognition using sensor fusion. "
    "Summarize the main classification strategies being used."
)

print("--- Lanzando agente ---")

for step in agent.stream(
    {"messages": [{"role": "user", "content": query_task}]},
    stream_mode="updates"
):
    node = list(step.keys())[0]
    msgs = step[node].get("messages", [])
    for msg in msgs:
        msg_type = type(msg).__name__
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            print(f"\n[{node}] {msg_type} → tool_call: {msg.tool_calls[0]['name']}({msg.tool_calls[0]['args']})")
        elif msg_type == "ToolMessage":
            print(f"[{node}] {msg_type} → tool executed ✓")
        elif msg_type == "AIMessage" and msg.content:
            # Solo imprimimos preview si NO es el mensaje final. El mensaje final lo guardamos completo
            final_content = msg.content
            print(f"[{node}] {msg_type} → synthesizing...")

print("\n--- Respuesta Final ---")
print(final_content)