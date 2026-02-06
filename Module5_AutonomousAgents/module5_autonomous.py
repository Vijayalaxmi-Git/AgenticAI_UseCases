import os, sys, io
from crewai import Agent, Task, Crew, LLM, Process

# Standard fixes for your Windows VS Code setup
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
os.environ["OPENAI_API_KEY"] = "NA" 

# 1. Setup Local LLM
local_llm = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")

# 2. Define specialized workers WITH backstories
researcher = Agent(
    role="Researcher", 
    goal="Find safety facts", 
    backstory="You are a meticulous security auditor who specializes in finding risks in Python libraries.", # ADDED
    llm=local_llm
)

coder = Agent(
    role="Developer", 
    goal="Write safe Python code", 
    backstory="You are a Senior Python Engineer who writes clean, production-ready code based on research.", # ADDED
    llm=local_llm
)

# 3. Define the tasks WITHOUT a forced order
t1 = Task(description="Research the library {library}", expected_output="Safety report")
t2 = Task(description="Write a script using {library}", expected_output="Python code")

# 4. The Hierarchical Crew
# Note: I added 'backstory' logic to the manager too!
autonomous_crew = Crew(
    agents=[researcher, coder],
    tasks=[t1, t2],
    process=Process.hierarchical, 
    manager_llm=local_llm,      
    verbose=True
)

if __name__ == "__main__":
    print("🧠 Starting Autonomous Manager Mode...", flush=True)
    autonomous_crew.kickoff(inputs={'library': 'flask'})
