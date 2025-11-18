##
import os
import random
import time
import vertexai
from vertexai import agent_engines

## Set your PROJECT_ID
PROJECT_ID = "gen-lang-client-0423313805"  # TODO: Replace with your project ID
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID

## Create a simple agent
!mkdir -p sample_agent


## Make some conf files and add some reqs
!touch sample_agent/requirements.txt
!touch sample_agent/.env

##
regions_list = ["europe-west1", "europe-west4", "us-east4", "us-west1"]
deployed_region = random.choice(regions_list)

## Deploy agent
!adk deploy agent_engine --project=$PROJECT_ID --region=$deployed_region sample_agent --agent_engine_config_file=sample_agent/.agent_engine_config.json

## Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=deployed_region)

# Get the most recently deployed agent
agents_list = list(agent_engines.list())
if agents_list:
    remote_agent = agents_list[0]  # Get the first (most recent) agent
    client = agent_engines
    print(f"✅ Connected to deployed agent: {remote_agent.resource_name}")
else:
    print("❌ No agents found. Please deploy first.")

## Test Deployed agent
async for item in remote_agent.async_stream_query(
    message="What is the weather in Tokyo?",
    user_id="user_42",
):
    print(item)

## Delete agent (cleanup)
agent_engines.delete(resource_name=remote_agent.resource_name, force=True)
