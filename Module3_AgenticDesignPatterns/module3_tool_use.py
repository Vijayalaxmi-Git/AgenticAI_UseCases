import os
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool
import sys
import io

# Force UTF-8 encoding for the terminal output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Set a longer timeout for local connections
# os.environ["OTEL_EXPORTER_OTLP_TIMEOUT"] = "300"
# Add this line to satisfy the Pydantic check
os.environ["EMBEDDINGS_OLLAMA_MODEL_NAME"] = "nomic-embed-text"


# 1. Define a CUSTOM TOOL (Simulating a database search)
@tool("LibrarySearchTool")
def library_search(library_name: str) -> str:
    """Useful for finding the latest version and safety rating of a Python library."""
    # In a real app, this would call an API or search the web
    database = {
        "flask": "Version 3.1.0 - Safety Rating: High",
        "requests": "Version 2.32.0 - Safety Rating: High",
        "pickle": "Version 1.0.0 - Safety Rating: DANGEROUS (Code Injection Risk)",
    }
    return database.get(library_name.lower(), "Library not found in secure database.")


# 2. Configure Local LLM
local_llm = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")

# 3. Define the Agent WITH the tool
researcher = Agent(
    role="Safety Researcher",
    goal="Verify if the library {library} is safe to use.",
    backstory="You are a meticulous researcher.",
    tools=[library_search],
    llm=local_llm,
    verbose=True,
    max_iter=2,  # <--- ADD THIS: Stops it after 2 tries
    max_execution_time=60,  # <--- ADD THIS: Stops it after 60 seconds
)

# 4. Define the Task
task = Task(
    description="Check the safety of {library}. If you find information, STOP immediately and summarize it.",
    agent=researcher,
    expected_output="A safety recommendation.",
)

# 5. Kickoff with the dedicated embedding model
crew = Crew(
    agents=[researcher],
    tasks=[task],
    memory=True,
    embedder={
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text",  # Much faster than llama3.2 for memory
            "task_type": "retrieval_document",
        },
    },
    verbose=True,
)

if __name__ == "__main__":
    print("--- Starting Tool Use & Memory Practice ---", flush=True)

    # Run 1: The agent uses the tool to learn about 'pickle'
    print("\n--- RUN 1 (Learning) ---")
    crew.kickoff(inputs={"library": "pickle"})

    # Run 2: The agent should now answer faster or with more context
    # because it "remembers" the safety rating from Run 1
    print("\n--- RUN 2 (Recalling) ---")
    crew.kickoff(inputs={"library": "pickle"})
