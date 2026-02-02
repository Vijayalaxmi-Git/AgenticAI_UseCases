# The "Coder & Reviewer" Team
# This module demonstrates a multi-agent collaboration pattern in Python.
# Agent A : One agent (the Coder) writes code based on a task.
# Agent B : Another agent (the Reviewer) inspects the code for potential issues.


from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1/", api_key="ollama", timeout=300.0)


def multi_agent_collaboration(task):
    # --- AGENT 1: THE CODER ---
    print("--- CODER is working... ---", flush=True)
    coder_response = (
        client.chat.completions.create(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Python Developer. Write clean, functional code.",
                },
                {"role": "user", "content": task},
            ],
        )
        .choices[0]
        .message.content
    )
    print(f"\nCODER OUTPUT:\n{coder_response}\n", flush=True)

    # --- AGENT 2: THE REVIEWER ---
    # The reviewer receives the CODER's output as its input
    print("--- REVIEWER is inspecting the code... ---", flush=True)
    reviewer_response = (
        client.chat.completions.create(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Senior Security Engineer. Find vulnerabilities or bugs in code.",
                },
                {
                    "role": "user",
                    "content": f"Review this code for security issues:\n{coder_response}",
                },
            ],
        )
        .choices[0]
        .message.content
    )
    print(f"REVIEWER CRITIQUE:\n{reviewer_response}", flush=True)


if __name__ == "__main__":
    multi_agent_collaboration("Write a Python script to upload a file to a server.")
