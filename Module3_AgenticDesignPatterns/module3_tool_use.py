import os, sys, io
from crewai import Agent, Task, Crew, LLM, Process
from crewai.tools import tool

# 1. Environment & Encoding Fixes
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
os.environ["EMBEDDINGS_OLLAMA_MODEL_NAME"] = "nomic-embed-text"

# 2. Setup Local LLM
local_llm = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")

# 3. Custom Tool
@tool("LibrarySearchTool")
def library_search(library_name: str) -> str:
    """Useful for finding safety ratings of Python libraries."""
    database = {
        "flask": "Safe",
        "pickle": "DANGEROUS (Code Injection Risk)"
    }
    return database.get(library_name.lower(), "Library not found in secure database.")

# 4. Define Agents (The missing variables)
researcher = Agent(
    role="Safety Researcher",
    goal="Verify if the library {library} is safe.",
    backstory="You are a meticulous analyst.",
    tools=[library_search],
    llm=local_llm,
    verbose=True,
    max_iter=3,           # <--- BRAKE 1: Stop after 3 attempts
    max_execution_time=60  # <--- BRAKE 2: Stop after 60 seconds
)

coder = Agent(
    role="Python Developer",
    goal="Write code ONLY if safe.",
    backstory="You prioritize security.",
    llm=local_llm,
    verbose=True
)

# 5. Define Tasks (The other missing variables)
t1 = Task(description="Check safety of {library}.", agent=researcher, expected_output="A safety report.")
t2 = Task(description="Write code or a refusal based on the report.", agent=coder, expected_output="Python code or refusal.")

# 6. The Crew
crew = Crew(
    agents=[researcher, coder], # Both now defined!
    tasks=[t1, t2],             # Both now defined!
    process=Process.sequential,
    memory=True,
    verbose=True
)

if __name__ == "__main__":
    print("🚀 Starting Module 3 Graduation Run...", flush=True)
    crew.kickoff(inputs={'library': 'pickle'})
