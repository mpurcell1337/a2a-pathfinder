import os
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_SECRET_KEY"))

def run_subagent(task_description, context=""):
    """
    Run a subagent to perform a specific research task.
    
    Args:
        task_description (str): The specific task for the subagent to perform
        context (str): Additional context about the overall project
    
    Returns:
        str: The subagent's research results
    """
    
    # Load the subagent prompt template
    with open("./reference/research_subagent_simple.md", "r") as f:
        subagent_prompt = f.read()
    
    # Replace the placeholder with today's date
    subagent_prompt = subagent_prompt.replace("{{.CurrentDate}}", datetime.today().strftime("%Y-%m-%d"))
    
    # Create the full task description
    full_task = f"""
{context}

## Your Specific Task:
{task_description}

Please research this task thoroughly and provide a detailed report of your findings.
"""
    
    # Initialize the conversation for the subagent
    messages = [
        {
            "role": "system",
            "content": subagent_prompt
        },
        {
            "role": "user", 
            "content": full_task
        }
    ]
    
    # Call the API for the subagent
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    # Test the subagent
    test_task = "Research the latest developments in cat toy design and materials"
    result = run_subagent(test_task, "This is part of a project to design a new cat toy for door integration.")
    print("Subagent Result:")
    print(result) 