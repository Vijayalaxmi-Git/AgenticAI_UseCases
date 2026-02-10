# An extended version of Module 2 that introduces a third agent responsible for:
# Orchestrating the conversation, Managing handoffs, Ensuring quality control, 
# This demonstrates more complex multi-agent pipelines.
# Add a third agent (a "Technical Writer" to document the code).
# The "Coder, Reviewer & Documenter" Team
# This module demonstrates a multi-agent collaboration pattern in Python.
# Agent A : One agent (the Coder) writes code based on a task.
# Agent B : Another agent (the Reviewer) inspects the code for potential issues.
# Agent C : A third agent (the Documenter) creates documentation for the code.
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1/", api_key="ollama", timeout=300.0)


def run_agent_team(user_request):
    # --- AGENT 1: THE CODER ---
    print("\n[1] CODER is drafting code...", flush=True)
    code_draft = (
        client.chat.completions.create(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Python Specialist. Write only the code, no explanation.",
                },
                {"role": "user", "content": user_request},
            ],
        )
        .choices[0]
        .message.content
    )

    # --- AGENT 2: THE SECURITY REVIEWER ---
    print("[2] SECURITY REVIEWER is scanning for vulnerabilities...", flush=True)
    security_audit = (
        client.chat.completions.create(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Cyber-Security Expert. Critique code for risks.",
                },
                {
                    "role": "user",
                    "content": f"Find 2 security risks in this code:\n{code_draft}",
                },
            ],
        )
        .choices[0]
        .message.content
    )

    # --- AGENT 3: THE TECHNICAL WRITER ---
    # This agent takes the work of BOTH previous agents to create the final package
    print("[3] TECHNICAL WRITER is preparing the final documentation...", flush=True)
    final_package = (
        client.chat.completions.create(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Technical Documenter. Summarize the code and the security findings into a clean README format.",
                },
                {
                    "role": "user",
                    "content": f"Code: {code_draft}\n\nSecurity Notes: {security_audit}",
                },
            ],
        )
        .choices[0]
        .message.content
    )

    print("\n" + "=" * 30)
    print("FINAL MULTI-AGENT OUTPUT:")
    print("=" * 30)
    print(final_package, flush=True)


if __name__ == "__main__":
    run_agent_team("Write a script to save user passwords to a local text file.")
