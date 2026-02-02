import os
from crewai import Agent, Task, Crew, LLM

# 1. Configure the Local LLM Object
# This avoids LangChain and uses CrewAI's native local provider
local_llm = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")

# 2. Define Agents using the local_llm object
coder = Agent(
    role="Senior Python Developer",
    goal="Write optimized Python code for: {topic}",
    backstory="You are a logic-driven engineer who loves clean code.",
    llm=local_llm,
    allow_delegation=False,
)

reviewer = Agent(
    role="Security Auditor",
    goal="Find vulnerabilities in the code provided by the developer.",
    backstory="You are a paranoid security expert.",
    llm=local_llm,
    allow_delegation=False,
)

writer = Agent(
    role="Technical Writer",
    goal="Write a professional README.",
    backstory="You make complex technical details easy to understand.",
    llm=local_llm,
    allow_delegation=False,
)

# 3. Define Tasks
t1 = Task(
    description="Write code for {topic}", agent=coder, expected_output="Python code."
)
t2 = Task(
    description="Audit the code for risks.",
    agent=reviewer,
    expected_output="Security risk list.",
)
t3 = Task(
    description="Create a final README.",
    agent=writer,
    expected_output="Markdown README.",
)

# 4. Form and Run the Crew
my_crew = Crew(agents=[coder, reviewer, writer], tasks=[t1, t2, t3])

print("--- Crew is starting work! ---", flush=True)
result = my_crew.kickoff(inputs={"topic": "A simple file uploader"})
print(f"\n\nFINAL RESULT:\n{result}")
