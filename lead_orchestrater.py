import os
import openai
from datetime import datetime

# Set your OpenAI API key

openai.api_key = os.getenv("OPENAI_SECRET_KEY")

# Load the lead agent prompt from a markdown file (i.e. manager.md)
with open("prompts/manager.md", "r") as f:
    lead_agent = f.read()

# Replace the placeholder with today's date
lead_agent = lead_agent.replace("{{.CurrentDate}}", datetime.today().strftime("%Y-%m-%d"))

# Define the user's query
user_query = "I need you to design a new cat toy that will be used for integrating cats between doors."


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
# followup = "Please simulate the subagent responses."
# messages.append({"role": "user", "content": followup})

# # Second API call
# response = openai.ChatCompletion.create(
#     model="gpt-4",
#     messages=messages,
#     temperature=0.7
# )

# # Print simulated subagent results
# assistant_reply = response['choices'][0]['message']['content']
# print("\nAssistant (Subagent Reports):\n", assistant_reply)
# messages.append({"role": "assistant", "content": assistant_reply})

# # Final user request to synthesize
# final_user_request = "Synthesize all of that into a strategic executive summary."
# messages.append({"role": "user", "content": final_user_request})

# # Third API call
# response = openai.ChatCompletion.create(
#     model="gpt-4",
#     messages=messages,
#     temperature=0.7
# )

# # Print the executive summary
# assistant_reply = response['choices'][0]['message']['content']
# print("\nAssistant (Executive Summary):\n", assistant_reply)
