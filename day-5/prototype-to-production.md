# Prototype to Production Whitepaper

Watch [this video](https://www.youtube.com/watch?v=kJRgj58ujEk) to see how agent ops looks in action!

There are two primary ways of evaluating an agents behavioural quality:
- Manual Pre-PR Eval: Run the test locally and then link the PR in the pull request
- Automated in-pipeline gate: The test run in the CI/CD pipeline 

### Ways to test new changes
- Canary: Start with 1% of users and monitor for any issues or abuse
- Blue-Green: Run two production envs and switch between them
- A/B Testing: Compare the outputs of two models, can use the LLM as a judge from [[agent-quality-whitepaper]]
- Feature Flags: Deploy code but control release dynamically

### Threats and Solutions

The major threats are:
- Prompt Injections & Rogue Actions
- Data Leakage
- Memory Poisioning: False info stored in the agent's memory can corrupt all future interactions

and the defences are:
1. Agent Constitution: Policy Definition and System Instructions 
2. Enforcement Layer: Guardrails, Safeguards and Filtering - IO filtering and HITL
3. Continuous Assurance and testing

### Design Notes
For long running tasks, you can have a simple service for publiishing tasks that can trigger a cloud run. 

Vertex AI Agent has built in memory but Cloud Run can let you use your own database!

Make sure you have a failsafe. This means that if a threat is identified, the system should go it
immediate containment. It should then triage and try to resolve the issue

## A2A
We have to use agent cards for the A2A protocol
```json
{
  "name": "check_prime_agent",
  "version": "1.0.0",
  "description": "An agent specialized in checking whether numbers are prime",
  "capabilities": {},
  "securitySchemes": {
     "agent_oauth_2_0": {
        "type": "oauth2",
  }
  "defaultInputModes": ["text/plain"],
  "defaultOutputModes": ["application/json"],
  "skills": [
    {
      "id": "prime_checking",
      "name": "Prime Number Checking",
      "description": "Check if numbers are prime using efficient algorithms",
      "tags": ["mathematical", "computation", "prime"]
    }
  ],
  "url": "http://localhost:8001/a2a/check_prime_agent"
}
```

Google ADK can implement this very easily
```python
# Example using ADK: Exposing an agent via A2A
from google.adk.a2a.utils.agent_to_a2a import to_a2a
# Your existing agent
root_agent = Agent(
    name='hello_world_agent',
    # ... your agent code ...
)
# Make it A2A-compatible
a2a_app = to_a2a(root_agent, port=8001)
# Serve with uvicorn
# uvicorn agent:a2a_app --host localhost --port 8001
# Or serve with Agent Engine
# from vertexai.preview.reasoning_engines import A2aAgent
# from google.adk.a2a.executor.a2a_agent_executor import A2aAgentExecutor
# a2a_agent = A2aAgent(
#    agent_executor_builder=lambda: A2aAgentExecutor(agent=root_agent)
# )

# Example using ADK: Consuming a remote agent via A2A
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
prime_agent = RemoteA2aAgent(
    name="prime_agent",
    description="Agent that handles checking if numbers are prime.",
    agent_card="http://localhost:8001/a2a/check_prime_agent/ 
               .well-known/agent-card.json"
)

# Example using ADK: Hierarchical agent composition
# ADK Local sub-agent for dice rolling
roll_agent = Agent(
    name="roll_agent",
    instruction="You are an expert at rolling dice."
)
# ADK Remote A2A agent for prime checking
prime_agent = RemoteA2aAgent(
    name="prime_agent",
    agent_card="http://localhost:8001/.well-known/agent-card.json"
)
# ADK Root orchestrator combining both
root_agent = Agent(
    name="root_agent",
    instruction="""Delegate rolling dice to roll_agent, prime checking 
to prime_agent.""",
    sub_agents=[roll_agent, prime_agent]
)
```

Lightweight local agents are better for small tight tasks, A2A can be overkill!

> MCP and A2A are not competing! A2A is for agent to agent communication but MCP is for tool usage

## Registerys

A tool resigstary is a repo of tools, their function and thier usage. This is useful when there ends up being
so many tools. 

Agents that acces the repo can be:
- GeneralistL able to access all tools
- Specialiased, can only acces a subset of tools, which speeds up performace
- Adative: able to access tools on the fly to adapt to new tools and requests.

You can also have an agent regisgtary, which has the agent cards!
