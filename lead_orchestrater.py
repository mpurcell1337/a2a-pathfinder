import openai
from datetime import datetime

# Set your OpenAI API key
openai.api_key = "your-api-key-here"  # Replace with your actual key or use an environment variable

# Load the CEO prompt from a markdown file
with open("ceo_research_prompt.md", "r") as f:
    ceo_prompt = f.read()

# Replace the placeholder with today's date
ceo_prompt = ceo_prompt.replace("{{.CurrentDate}}", datetime.today().strftime("%Y-%m-%d"))

# Define the user's query
user_query = "What are the top trends in generative AI for enterprise applications in 2025?"

# Initialize the conversation
messages = [
    {
        "role": "system",
        "content": "You are the CEO of a research organization. Set direction and delegate to subagents to answer user queries. Act with strategic planning and high-level orchestration."
    },
    {
        "role": "user",
        "content": f"{ceo_prompt}\n\n---\n\n### User Query\n{user_query}"
    }
]

# First API call to initiate the plan
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=messages,
    temperature=0.7
)

# Print assistant's initial strategic plan
assistant_reply = response['choices'][0]['message']['content']
print("Assistant (Strategic Plan):\n", assistant_reply)
messages.append({"role": "assistant", "content": assistant_reply})

# Add a follow-up message to simulate subagent responses
followup = "Please simulate the subagent responses."
messages.append({"role": "user", "content": followup})

# Second API call
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=messages,
    temperature=0.7
)

# Print simulated subagent results
assistant_reply = response['choices'][0]['message']['content']
print("\nAssistant (Subagent Reports):\n", assistant_reply)
messages.append({"role": "assistant", "content": assistant_reply})

# Final user request to synthesize
final_user_request = "Synthesize all of that into a strategic executive summary."
messages.append({"role": "user", "content": final_user_request})

# Third API call
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=messages,
    temperature=0.7
)

# Print the executive summary
assistant_reply = response['choices'][0]['message']['content']
print("\nAssistant (Executive Summary):\n", assistant_reply)
