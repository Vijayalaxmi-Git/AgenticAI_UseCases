import os, sys, io
from crewai import Agent, Task, Crew, LLM, Process
from crewai.tools import tool

# 1. Windows & Memory Environment Fixes
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
os.environ["EMBEDDINGS_OLLAMA_MODEL_NAME"] = "nomic-embed-text"

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
    verbose=True,
    allow_delegation=False,
)

coder = Agent(
    role="Python Developer",
    goal="Write a script using {library} ONLY if the researcher confirms it is safe.",
    backstory="You are a developer who follows security guidelines strictly. If a library is unsafe, you refuse to use it.",
    llm=local_llm,
    verbose=True,
    allow_delegation=False,
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

# 6. Form the Master Crew
master_crew = Crew(
    agents=[researcher, coder],
    tasks=[t1, t2],
    process=Process.sequential,  # This creates the 'Chain' of collaboration
    memory=True,
    embedder={"provider": "ollama", "config": {"model": "nomic-embed-text"}},
)

if __name__ == "__main__":
    print("🚀 Starting Final Master Crew Graduation Project...", flush=True)

    # We test with 'pickle' to prove the agents actually communicate!
    result = master_crew.kickoff(inputs={"library": "pickle"})

    print("\n" + "=" * 50)
    print("FINAL AGENCY OUTPUT:")
    print("=" * 50)
    print(result)
