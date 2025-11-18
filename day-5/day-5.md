# Google Agents Course: Day 5 Tutorial

## A2A

ADK can use the `to_a2a()` function to make an agent available to other agents! It's more complex than just
using sub agents!

The function:
Wraps your agent in an A2A-compatible server
Auto-generates an agent card that includes:
Serves the agent card at /.well-known/agent-card.json (standard A2A path)
Handles all A2A protocol details (request/response formatting, task endpoints)

Once we have an agent being served via uvicorn for example, we can then then create a remoteA2A agent. This
will find the agent card at the server IP and then add some wrappers to make it act like a local agent. It's a
client side proxy

## Tutorial Example

1. Customer asks Support Agent a question about a product
1. Support Agent realizes it needs product info
1. Support Agent calls the remote_product_catalog_agent (RemoteA2aAgent)
1. ADK sends an A2A protocol request to http://localhost:8001
1. Product Catalog Agent processes the request and responds
1. Support Agent receives the response and continues
1. Customer gets the final answer

[Example Info Flow](https://storage.googleapis.com/github-repo/kaggle-5days-ai/day5/a2a_03.png)

## Deployment
First set up some auth with the gcloud cli tool

`gcloud auth application-default login`  - Authorise the gcloud CLI
`gcloud auth login` - Authorise code 

Enable the following API's in the cloud console:
- Vertex AI API
- Cloud Storage API
- Cloud Logging API
- Cloud Monitoring API
- Cloud Trace API
- Telemetry API
[This Link](https://console.cloud.google.com/flows/enableapi?apiid=aiplatform.googleapis.com,storage.googleapis.com,logging.googleapis.com,monitoring.googleapis.com,cloudtrace.googleapis.com,telemetry.googleapis.com) is a shortcut to doing that

> For my own stuff, I would not use vertex but google cloud, which is set up
> [here](https://google.github.io/adk-docs/deploy/cloud-run/)

The `adk deploy agent_engine` command:
Packages your agent code (sample_agent/ directory)
Uploads it to Agent Engine
Creates a containerized deployment
Outputs a resource name like: projects/PROJECT_NUMBER/locations/REGION/reasoningEngines/ID
