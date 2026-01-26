import json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1/", api_key="ollama")


# Define a real Python tool (The "Calculator")
def calculate_complex_math(a, b):
    return (a * b) + (a / b)


def tool_agent_practice():
    print("Agent: I'm thinking about a math problem...", flush=True)

    # In a real agentic workflow, the LLM 'decides' to call this

    # For this practice, we will simulate the 'Tool Use' logic

    val1, val2 = 155, 5

    print(f"Task: Calculate (a * b) + (a / b) for a={val1}, b={val2}", flush=True)

    # Step 1: The 'Agent' calls the Python function
    result = calculate_complex_math(val1, val2)

    # Step 2: The 'Agent' takes the tool output and explains it
    prompt = f"The calculator tool returned the result: {result}. Explain this result to the user."

    response = client.chat.completions.create(
        model="llama3.2", messages=[{"role": "user", "content": prompt}]
    )

    print(f"\nFinal Agent Output: {response.choices[0].message.content}", flush=True)


if __name__ == "__main__":
    tool_agent_practice()
