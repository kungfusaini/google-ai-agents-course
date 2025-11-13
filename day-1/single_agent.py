##
import os
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types
print("Imported All!")

try:
    GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
    print("Key SUCCESS!")
except Exception as e:
    print("Couldn't find your key")

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)


##
root_agent = Agent(
    name="helpful_assistant",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
    tools=[google_search],
)

runner = InMemoryRunner(agent=root_agent)

##
response = await runner.run_debug(
        "What is the weather in london Hayes UB33AE right now?"
)

##
# You can run this code to acces the Web UI!
!adk create sample-agent --model gemini-2.5-flash-lite --api_key $GOOGLE_API_KEY
!adk web
