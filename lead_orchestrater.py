import os
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv
from subagent import run_subagent
from utils.elasticsearch_client import ElasticsearchClient

# Set your OpenAI API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_SECRET_KEY"))

# Initialize Elasticsearch client
es_client = ElasticsearchClient()
es_client.create_index()

# Load the lead agent prompt from a markdown file (i.e. manager.md)
with open("./prompts/manager_lead_agent.md", "r") as f:
    lead_agent = f.read()

# Replace the placeholder with today's date
lead_agent = lead_agent.replace("{{.CurrentDate}}", datetime.today().strftime("%Y-%m-%d"))

# Define the user's query
ORGANIZATION_NAME = "AI Art Company"
ORGANIZATION_NAME_SANITIZED = ORGANIZATION_NAME.replace(" ", "_").lower()
ORGANIZATION_QUERY = f"Help design an AI art company that will be used generate large amounts of art using language models."

# Create outputs directory if it doesn't exist
import os
output_dir = f"outputs/{ORGANIZATION_NAME_SANITIZED}"
os.makedirs(output_dir, exist_ok=True)

# Initialize the conversation
messages = [
    {
        "role": "system",
        "content": lead_agent
    },
    {
        "role": "user",
        "content": ORGANIZATION_QUERY
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
with open(f"{output_dir}/strategic_plan.md", "w") as f:
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
    This is part of a research project to answer the user's query: "{ORGANIZATION_QUERY}"

    The strategic plan identified this as a key research area that needs investigation.
    """
    
    result = run_subagent(task, context)
    subagent_results.append(f"## Subagent {i} Results\n\n**Task:** {task}\n\n{result}")
    
    print(f"Subagent {i} completed.")

# Combine all subagent results
subagent_reports = "\n\n".join(subagent_results)
print("\nAll subagents completed!")

# Save subagent reports to file
with open(f"{output_dir}/subagent_reports.md", "w") as f:
    f.write(f"# Subagent Reports\n\n{subagent_reports}")

# Add the subagent results to the conversation for synthesis
messages.append({"role": "user", "content": f"Here are the subagent research results:\n\n{subagent_reports}"})

# Final user request to synthesize - using a more focused prompt
final_user_request = """Based on the strategic plan and the subagent research results, create a comprehensive executive summary with actionable recommendations.

Please structure your response as follows:
1. Executive Summary (2-3 paragraphs)
2. Key Findings (bullet points)
3. Strategic Recommendations (numbered list)
4. Implementation Roadmap (brief overview)
5. Risk Assessment (key risks and mitigation strategies)

Make sure to synthesize all the information from the subagent reports into a cohesive, actionable plan."""
messages.append({"role": "user", "content": final_user_request})

# Third API call for final synthesis - using GPT-4 with higher max_tokens
try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=4000  # Increase token limit for longer response
    )
    
    # Print the executive summary
    executive_summary = response.choices[0].message.content
    print("\nAssistant (Executive Summary):\n", executive_summary)
    
    # Validate that the response is complete (not truncated)
    if len(executive_summary) < 100:
        print("Warning: Executive summary seems too short, may be truncated")
        # Try again with a simpler prompt
        simple_request = "Create a comprehensive executive summary based on the strategic plan and subagent research results. Include key findings, recommendations, and next steps."
        messages[-1] = {"role": "user", "content": simple_request}
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=4000
        )
        executive_summary = response.choices[0].message.content
        print("\nAssistant (Executive Summary - Retry):\n", executive_summary)
    
except Exception as e:
    print(f"Error generating executive summary: {e}")
    # Fallback to a simpler approach
    executive_summary = f"""# Executive Summary

Based on the strategic plan and subagent research results, here is a comprehensive summary for the AI Art Company:

## Key Findings
- AI technology (GANs and transformer-based language models) is essential for art generation
- Creative team is needed to curate and interface with AI technology
- Multiple revenue streams: direct sales, subscriptions, and licensing
- Market is growing but competitive, requiring strong marketing
- Legal and ethical considerations need careful navigation

## Strategic Recommendations
1. Invest in advanced AI technology infrastructure
2. Build a skilled creative team
3. Develop multiple monetization strategies
4. Focus on marketing and community engagement
5. Establish clear legal and ethical guidelines

## Implementation Roadmap
Phase 1: Technology setup and team building
Phase 2: Platform development and testing
Phase 3: Market launch and scaling
Phase 4: Expansion and optimization

## Risk Assessment
- Technical risks: AI model performance and scalability
- Market risks: Competition and changing preferences
- Legal risks: Copyright and IP issues
- Operational risks: Resource management and quality control

*Note: This is a fallback summary due to API response issues.*"""

# Save executive summary to file
with open(f"{output_dir}/executive_summary.md", "w") as f:
    f.write(f"# Executive Summary\n\n{executive_summary}")

# Create a comprehensive output file with all results
with open(f"{output_dir}/complete_design_output.md", "w") as f:
    f.write(f"""# Complete Design Output

## Strategic Plan
{strategic_plan}

## Subagent Reports
{subagent_reports}

## Executive Summary
{executive_summary}

---
*Generated on: {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}*
*User Query: {ORGANIZATION_QUERY}*
""")

print(f"\nOutputs saved to:")
print(f"- {output_dir}/strategic_plan.md")
print(f"- {output_dir}/subagent_reports.md") 
print(f"- {output_dir}/executive_summary.md")
print(f"- {output_dir}/complete_design_output.md")

# Store the complete plan in Elasticsearch with individual chunking embeddings
print("\nStoring plan with chunking in Elasticsearch...")
try:
    plan_id = es_client.store_plan_with_chunking(
        user_query=ORGANIZATION_QUERY,
        strategic_plan=strategic_plan,
        subagent_reports=subagent_reports,
        executive_summary=executive_summary,
        plan_type=ORGANIZATION_NAME
    )
    print(f"✅ Plan stored in Elasticsearch with ID: {plan_id}")
    print(f"🔍 You can search chunking at: http://localhost:5601 (Kibana)")
    print(f"📊 Elasticsearch endpoint: http://localhost:9200")
    print(f"📝 Individual chunks now searchable for retrieval")
except Exception as e:
    print(f"❌ Error storing plan in Elasticsearch: {e}")
    print("Make sure Elasticsearch is running with: docker-compose up -d")
