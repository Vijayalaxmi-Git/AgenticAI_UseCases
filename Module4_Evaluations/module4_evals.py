import os, sys, io
from crewai import Crew, Agent, Task, LLM, Process
from crewai.tools import tool

# 1. Force UTF-8 for Windows Emojis
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
os.environ["EMBEDDINGS_OLLAMA_MODEL_NAME"] = "nomic-embed-text"

# 2. Re-define the Tool and LLM (to keep this test independent)
@tool("LibrarySearchTool")
def library_search(library_name: str) -> str:
    """Finds safety ratings for Python libraries."""
    database = {"pickle": "DANGEROUS (Code Injection Risk)", "flask": "Safe"}
    return database.get(library_name.lower(), "Unknown")

local_llm = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")

# 3. Define the Crew (The "Subject" of our Evaluation)
researcher = Agent(
    role="Researcher", 
    goal="Check safety of {library}", 
    # We tell it EXACTLY which word to use
    backstory="""You are a strict security auditor. If a library is unsafe, 
    you MUST use the word 'DANGEROUS' in your final answer. 
    Never be vague.""", 
    tools=[library_search], 
    llm=local_llm, 
    max_iter=2
)

task = Task(description="Check {library}", agent=researcher, expected_output="Safety status")
eval_crew = Crew(agents=[researcher], tasks=[task], verbose=False) # Keep verbose off for clean scores

# 4. THE EVALUATION LOOP (Module 4 Logic)
def run_eval(test_count=3):
    print(f"🧪 Starting Evaluation on Llama 3.2...")
    passes = 0
    
    for i in range(test_count):
        print(f"Run {i+1}: ", end="", flush=True)
        output = eval_crew.kickoff(inputs={'library': 'pickle'})
        
        # Grading Logic: Did the agent catch the 'DANGEROUS' keyword?
        if "DANGEROUS" in str(output).upper():
            print("✅ PASS")
            passes += 1
        else:
            print("❌ FAIL")
            
    print(f"\nScore: {passes}/{test_count} ({(passes/test_count)*100}%)")

if __name__ == "__main__":
    run_eval(3)
