from openai import OpenAI

import sys
print("Script started successfully!", flush=True) # If you don't see this, Python isn't even starting
# 2026 standard local connection
client = OpenAI(base_url='http://localhost:11434/v1/', api_key='ollama', timeout=300.0)

print("Client created successfully!", flush=True) # If you don't see this, Python isn't even starting

def generate_and_reflect(task):   
    # --- PHASE 1: GENERATION ---
    print("Step 1: Generating initial solution...")
    response = client.chat.completions.create(
        model="llama3.2",
        messages=[{"role": "user", "content": f"Write a Python function to: {task}. Only provide code."}]
    )
    print("Step 1: Generating initial solution...", flush=True)
    # FIX: Added [0] here
    draft = response.choices[0].message.content 
    print(f"\n--- INITIAL DRAFT ---\n{draft}")

    # --- PHASE 2: REFLECTION ---
    print("\nStep 2: Reflecting on the code...")
    response = client.chat.completions.create(
        model="llama3.2",
        messages=[{"role": "user", "content": f"Critique this code for bugs or potential improvements:\n{draft}"}]
    )
    # FIX: Added [0] here
    critique = response.choices[0].message.content
    print(f"\n--- CRITIQUE ---\n{critique}")

    # --- PHASE 3: IMPROVEMENT ---
    print("\nStep 3: Refining based on reflection...")
    response = client.chat.completions.create(
        model="llama3.2",
        messages=[{"role": "user", "content": f"Using this critique: {critique}, rewrite the original code: {draft}"}]
    )
    # FIX: Added [0] here
    final = response.choices[0].message.content
    print(f"\n--- FINAL AGENTIC OUTPUT ---\n{final}")

    # At the very bottom of lesson1_patterns.py
if __name__ == "__main__":
    print("Starting Agentic Workflow...", flush=True)
    generate_and_reflect("calculate the nth Fibonacci number using recursion")














                       
                        






