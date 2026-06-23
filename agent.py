from langchain_community.utilities import SearxSearchWrapper
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents import create_agent

searx_host = "http://localhost:8888"
searx_wrapper = SearxSearchWrapper(searx_host=searx_host)

# 2. Definir la herramienta de búsqueda académica
@tool
def academic_search(query: str) -> str:
    """Use this tool to search for peer-reviewed scientific papers, 
    academic literature, and technical research regarding computer science, 
    sensor fusion, and human activity recognition."""
    # Forzamos la categoría 'science' para que SearXNG use arXiv, PubMed, etc.
    return searx_wrapper.run(query, categories=["science"])

tools = [academic_search]

# 3. Inicializar el LLM Local con Ollama
# Usamos qwen2.5 de 14b o llama3, configurando la temperatura a 0 para mayor precisión
llm = ChatOllama(
    #model="qwen2.5:14b",
    model="hf.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF:latest",
    temperature=0,
    streaming=True
)

# 4. Instrucciones del Sistema para el Agente Local
promt = (
    "You are an advanced academic research assistant. Your task is to analyze scientific topics "
    "by pulling state-of-the-art literature from your academic search tool. "
    "Always synthesize your findings and cite insights using the data retrieved."
)

# 5. Crear el Agente ReAct Autónomo con LangGraph
agent = create_agent(
    model=llm, 
    tools=tools, 
    system_prompt=promt
)

# 6. Ejecutar la consulta de investigación en local
query_task = (
    "Search for recent papers on Multimodal Human Activity Recognition using sensor fusion. "
    "Summarize the main classification strategies being used."
)

print("--- Iniciando Ejecución con la API moderna `create_agent` ---")

# En LangChain v1.0, invocamos al agente enviando la lista de mensajes estructurada
response = agent.invoke({
    "messages": [
        {"role": "user", "content": query_task}
    ]
})

print("\n--- Respuesta Final del Agente ---")
# El resultado final se almacena en el último bloque de mensaje retornado por el grafo
print(response["messages"][-1].content)