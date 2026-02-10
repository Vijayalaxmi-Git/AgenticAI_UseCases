#  “Master Crew” orchestrator that coordinates multiple agents and tools across modules.
# Useful for demonstrating:Multi-agent planning,Delegation,Tool integration,High-level orchestration

import os, sys, io,shutil
from crewai import Agent, Task, Crew, LLM, Process
from crewai.tools import tool

# --- AUTOMATED CLEANUP ---
# This removes the memory folder so you don't have to do it manually
memory_path = os.path.join(os.getcwd(), ".crewai")
if os.path.exists(memory_path):
    try:
        shutil.rmtree(memory_path)
        print("🧹 Memory cleared automatically for a fresh local run.", flush=True)
    except Exception as e:
        print(f"⚠️ Could not clear memory: {e}", flush=True)

# 1. Force UTF-8 and set Local Memory Defaults
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# --- THE SECRET SAUCE FOR LOCAL MEMORY ---
os.environ["OPENAI_API_KEY"] = "NA" 
os.environ["EMBEDDINGS_OLLAMA_MODEL_NAME"] = "nomic-embed-text"
# This next line tells the CrewAI RAG system where to find Ollama
os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"
# -----------------------------------------

# 2. Setup Local LLM
local_llm = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")


# 3. Custom Security Tool
@tool("SecurityDatabase")
def security_check(lib_name: str):
    """Checks a library against a security database for known risks."""
    database = {
        "flask": "Safe - High trust rating.",
        "requests": "Safe - Standard library.",
        "pickle": "UNSAFE - This library allows for Remote Code Execution. Do not use!",
    }
    return database.get(
        lib_name.lower(), "Unknown library - proceed with extreme caution."
    )


# 4. Define the Specialist Agents
researcher = Agent(
    role="Security Researcher",
    goal="Identify if {library} has any known vulnerabilities.",
    backstory="You are a paranoid security analyst. Your job is to prevent bad code from being written.",
    tools=[security_check],
    llm=local_llm,
    max_iter=2,           # <--- BRAKE 1: Stop after 3 attempts
    max_execution_time=60,  # <--- BRAKE 2: Stop after 60 seconds
    verbose=True,
    allow_delegation=False
)

coder = Agent(
    role="Python Developer",
    goal="Write a script using {library} ONLY if the researcher confirms it is safe.",
    backstory="You are a developer who follows security guidelines strictly. If a library is unsafe, you refuse to use it.",
    llm=local_llm,
    verbose=True,
    allow_delegation=False,
    max_iter=1
)

# 5. Define the Collaborative Tasks
t1 = Task(
    description="Research the safety of the library: {library}. Use your tool!",
    agent=researcher,
    expected_output="A summary of the safety status of the library.",
)

t2 = Task(
    description="Based on the researcher's report, either write a 5-line Python example using {library} OR write a short refusal explaining why it is dangerous.",
    agent=coder,
    expected_output="Code or a Security Refusal.",
)

# 6. Form the Master Crew (Simplified)
master_crew = Crew(
    agents=[researcher, coder],
    tasks=[t1, t2],
    process=Process.sequential,
    memory=False, # Will now use the env variables above
    verbose=True,
    max_rpm=10
)

if __name__ == "__main__":
    print("🚀 Starting Final Master Crew Graduation Project...", flush=True)

    # We test with 'pickle' to prove the agents actually communicate!
    result = master_crew.kickoff(inputs={"library": "pickle"})

    print("\n" + "=" * 50)
    print("FINAL AGENCY OUTPUT:")
    print("=" * 50)
    print(result)
