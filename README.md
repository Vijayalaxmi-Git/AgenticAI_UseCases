# AgenticAI_UseCases
# Module 1: Intro to Agentic Workflows (Reflection & Iteration)
 Self-Reflection Agent: Self Reflection Pattern
 “An agent that evaluates and improves its own outputs before finalizing.”

Tool-Using Agent: Tool Use Pattern
“An agent that delegates deterministic tasks to tools and uses LLMs for reasoning.”

Planning Pattern
The agent first creates a plan (steps/subtasks) before executing actions, instead of reacting immediately.
1. Planner -> Converts goal → steps
2. Executor
   - Executes each step
   - Uses tools / agents
3. Controller (optional)
   - Tracks progress
   - Handles failures

# Module 2: Multi-Agent Collaboration (Role-playing & Handoffs) 
Multi-agent Collaboration (Two LLMs talking to each other)
Agent A (The Coder): Writes the initial Python code.
Agent B (The Reviewer): Acts as a senior engineer to find security flaws

# Module 3: Capabilities (Tool Use)
 Agentic Design Patterns (Tool Use & Memory)

 ## Created new environment ->use the script -> py -3.11 -m venv crewenv 
 ## For venv old environment use the script-> 





