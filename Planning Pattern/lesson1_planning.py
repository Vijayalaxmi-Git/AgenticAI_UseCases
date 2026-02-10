#1. Planner -> Converts goal → steps
#2. Executor
#   - Executes each step
#   - Uses tools / agents
#3. Controller (optional)
#   - Tracks progress
#   - Handles failures
# Module 1: The "Planning" Pattern
# This module demonstrates the "Planning" design pattern in Python.
# The "Planning" pattern involves creating a plan or strategy before executing tasks.
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1/", api_key="ollama")


def planning_agent(goal):
    # Step 1: Generate a Step-by-Step Plan
    print(f"Goal: {goal}\n", flush=True)
    plan_prompt = (
        f"Break down the following goal into a numbered list of 3 logical steps: {goal}"
    )

    plan = (
        client.chat.completions.create(
            model="llama3.2", messages=[{"role": "user", "content": plan_prompt}]
        )
        .choices[0]
        .message.content
    )

    print(f"--- THE PLAN ---\n{plan}\n", flush=True)

    # Step 2: Execute based on the plan
    exec_prompt = f"Based on this plan: {plan}, write a very brief final response for the goal: {goal}"

    final_result = (
        client.chat.completions.create(
            model="llama3.2", messages=[{"role": "user", "content": exec_prompt}]
        )
        .choices[0]
        .message.content
    )

    print(f"--- FINAL EXECUTION ---\n{final_result}", flush=True)


if __name__ == "__main__":
    planning_agent("How to start a garden from scratch?")
