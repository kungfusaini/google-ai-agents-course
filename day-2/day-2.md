# Google Agents Course: Day 2 Tutorial

## Agent Tools vs Subagents
Agent Tools:
Agent A calls Agent B as a tool
Agent B's response goes back to Agent A
Agent A stays in control and continues the conversation
Use case: Delegation for specific tasks (like calculations)

Subagents:
Agent A transfers control completely to Agent B
Agent B takes over and handles all future user input
Agent A is out of the loop
Use case: Hand off to specialists (like customer support tiers)

## Custom Tools
We can define custom tools in python code for agents to use, super handy!

We can also get create an agent that will generate it's own code and remotely execute it
The pattern for the is have a master tool and a coder tool
The coder tool only produces pure code

Workflow:
Master tool calls code tool
It gets the code, and executes this with the BuiltInCodeExecutor

## Types of Tools
### Custom Tools
Tools you build yourself for specific needs
Complete control over functionality — you build exactly what your agent needs

- Function Tools: Python functions converted to agent tools
- Long Running Function Tools: Functions for operations that take significant time e.g. Human-in-the-loop approvals, file processing. Agents can start tasks and continue with other work while waiting
- Agent Tools: Other agents used as tools
- MCP Tools: Tools from Model Context Protocol servers
- OpenAPI Tools: Tools automatically generated from API specifications


### Build in Tools
Pre-built tools provided by ADK

Gemini Tools: Tools that leverage Gemini's capabilities
Google Cloud Tools [needs Google Cloud access]
Third-party Tools: Hugging Face, Firecrawl, GitHub Tools

## Pausable-tool recipe

1. Tool – call request_confirmation when you need a human:
```python
   def my_tool(arg: str, ctx: ToolContext) -> dict:
       if big_order:
           ctx.request_confirmation(hint="Approve?", payload={"arg": arg})
           return {"status": "pending"}
       return {"status": "done"}
```

2. App & Runner – make it resumable:
```python
   agent = LlmAgent(tools=[FunctionTool(my_tool)])
   app   = App(root_agent=agent, resumability_config=ResumabilityConfig(is_resumable=True))
   runner = Runner(app, InMemorySessionService())
```

3. Loop – run, pause, resume:
```python
   # initial call
   async for ev in runner.run_async(uid, sid, user_msg):
       if confirm_event(ev):              # adk_request_confirmation seen
           aid = ev.content.parts[0].function_call.id
           iid = ev.invocation_id
           break

   # build human answer
   resume = types.Content(parts=[types.Part(
           function_response=types.FunctionResponse(
               id=aid, name="adk_request_confirmation",
               response={"confirmed": True}))])

   # continue frozen call
   async for ev in runner.run_async(uid, sid, resume, invocation_id=iid):
       handle_final(ev)
```
