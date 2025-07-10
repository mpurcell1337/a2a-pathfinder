import os
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv
from subagent import run_subagent

# Set your OpenAI API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_SECRET_KEY"))

# Load the lead agent prompt from a markdown file (i.e. manager.md)
with open("./prompts/manager-art.md", "r") as f:
    lead_agent = f.read()

# Replace the placeholder with today's date
lead_agent = lead_agent.replace("{{.CurrentDate}}", datetime.today().strftime("%Y-%m-%d"))

# Define the user's query
user_query = "We are going to create an AI art company that will be used to create massive amounts of art. We need to create a plan to do this."

# Initialize the conversation
messages = [
    {
        "role": "system",
        "content": lead_agent
    },
    {
        "role": "user",
        "content": user_query
    }
]

# First API call to initiate the plan
response = client.chat.completions.create(model="gpt-4",
messages=messages,
temperature=0.7)

# Print assistant's initial strategic plan
strategic_plan = response.choices[0].message.content
print("Assistant (Strategic Plan):\n", strategic_plan)
messages.append({"role": "assistant", "content": strategic_plan})

# Save strategic plan to file
with open("outputs/strategic_plan.md", "w") as f:
    f.write(f"# Strategic Plan\n\n{strategic_plan}")

# Parse the strategic plan to extract subagent tasks
# This is a simplified approach - in a real implementation, you'd want more sophisticated parsing
print("\nExtracting subagent tasks from strategic plan...")

# Ask the lead agent to identify specific subagent tasks
task_extraction_prompt = """
Based on your strategic plan, identify 3-5 specific research tasks that need to be performed by subagents.
For each task, provide:
1. A clear, specific task description
2. The expected output format
3. Any specific sources or approaches to use

Format your response as a numbered list of tasks.
"""

messages.append({"role": "user", "content": task_extraction_prompt})

response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    temperature=0.7
)

task_list = response.choices[0].message.content
print("Identified tasks:\n", task_list)
messages.append({"role": "assistant", "content": task_list})

# Run actual subagents for each identified task
print("\nRunning subagents...")
subagent_results = []

# Extract tasks from the response (simplified parsing)
lines = task_list.split('\n')
tasks = []
for line in lines:
    if line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
        # Extract the task description
        task_desc = line.split('.', 1)[1].strip()
        if task_desc:
            tasks.append(task_desc)

# Run subagents for each task
for i, task in enumerate(tasks[:3], 1):  # Limit to 3 tasks for efficiency
    print(f"\nRunning Subagent {i}: {task[:50]}...")
    
    context = f"""
    This is part of a research project to answer the user's query: "{user_query}"

    The strategic plan identified this as a key research area that needs investigation.
    """
    
    result = run_subagent(task, context)
    subagent_results.append(f"## Subagent {i} Results\n\n**Task:** {task}\n\n{result}")
    
    print(f"Subagent {i} completed.")

# Combine all subagent results
subagent_reports = "\n\n".join(subagent_results)
print("\nAll subagents completed!")

# Save subagent reports to file
with open("outputs/subagent_reports.md", "w") as f:
    f.write(f"# Subagent Reports\n\n{subagent_reports}")

# Add the subagent results to the conversation for synthesis
messages.append({"role": "user", "content": f"Here are the subagent research results:\n\n{subagent_reports}"})

# Final user request to synthesize
final_user_request = "Based on the strategic plan and the subagent research results, synthesize everything into a comprehensive executive summary with actionable recommendations."
messages.append({"role": "user", "content": final_user_request})

# Third API call for final synthesis
response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    temperature=0.7
)

# Print the executive summary
executive_summary = response.choices[0].message.content
print("\nAssistant (Executive Summary):\n", executive_summary)

# Save executive summary to file
with open("outputs/executive_summary.md", "w") as f:
    f.write(f"# Executive Summary\n\n{executive_summary}")

# Create a comprehensive output file with all results
with open("outputs/complete_design_output.md", "w") as f:
    f.write(f"""# Complete Design Output

## Strategic Plan
{strategic_plan}

## Subagent Reports
{subagent_reports}

## Executive Summary
{executive_summary}

---
*Generated on: {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}*
*User Query: {user_query}*
""")

print(f"\nOutputs saved to:")
print(f"- outputs/strategic_plan.md")
print(f"- outputs/subagent_reports.md") 
print(f"- outputs/executive_summary.md")
print(f"- outputs/complete_design_output.md")
