# A more advanced autonomous workflow combining:
# Planning,Tool use,Memory,Multi-step execution,Self‑correction
# This script represents a near‑production autonomous agent pattern.

import os, sys, io
from crewai import Agent, Task, Crew, LLM, Process

# 1. Windows Fixes
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
os.environ["OPENAI_API_KEY"] = "NA" 

# 2. Local LLM (Using Llama 3.2 as the Boss)
local_llm = LLM(model="ollama/llama3.2", 
    base_url="http://localhost:11434",
    timeout=600  # <--- Increase to 600 seconds (10 min)
)

# 3. Define the Workers (No tasks assigned yet!)
researcher = Agent(
    role="Security Researcher", 
    goal="Investigate library safety", 
    backstory="You are a meticulous auditor.",
    llm=local_llm
)

coder = Agent(
    role="Python Developer", 
    goal="Write secure code", 
    backstory="You are a logic-driven engineer.",
    llm=local_llm
)

# 4. Define the Tasks (Notice we don't assign an agent here!)
# In Module 5, the Manager decides who gets these tasks.
t1 = Task(description="Research the safety of the 'pickle' library.", expected_output="A safety report.")
t2 = Task(description="Write a Python script for 'pickle' or refuse if unsafe.", expected_output="Code or Refusal.")

# 5. EXECUTION: The Hierarchical Crew
autonomous_crew = Crew(
    agents=[researcher, coder],
    tasks=[t1, t2],
    process=Process.hierarchical, # <--- The Module 5 Pattern
    manager_llm=local_llm,        # <--- The 'Autonomous' Brain
    verbose=True
)

if __name__ == "__main__":
    print("🧠 The Manager is now planning the workflow...", flush=True)
    result = autonomous_crew.kickoff()
    print(f"\nFINAL RESULT:\n{result}")
