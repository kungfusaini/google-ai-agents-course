# Introduction to Agents Whitepaper

Agentic systems are really an exercise in context engineering (which is replacing prompt engineering)

Context engineering is important as LLMs can do anything, but getting them to do a specific singular
guided thing can be very difficult!

There are 3 main components:
Model (Brain) - for thinking
Tools (Hands) - actions (via API etc)
Orchestration Layer (Nervous System) - for handling the whole system (memory, tool usage etc)

The loop is like this:
1. Get the mission
2. Build current context
3. Think about the context and create a plan
4. Act on the plan 
5. Update the context with the results of the new plan
Repeat from step 3


## Agent Taxonomy
There are 5 levels

### Level 0: Just the Brain
At this level you just have an LLM. It only knows things inside it's training data.

### Level 1: Add the hands
Now, the brain can act by adding external tools (Like calling an API)

### Level 2: Thinking more deeply
Context engineering now comes into play. We use the information and tools available to us to better feed
the LLM and make better plans. For example, understanding what steps need to be taken and what
API calls need to be made, and defining the exact calls with args

### Level 3: Multi Agent Systems
Instead of just having tools to access, the model can now access other agents (treated like tools). These
other agents could be better suited for specific tasks (different core model, tools etc). Essentially
division of labour

### Level 4: Self Aware System
The system knows what it doesn't know and can spin up tools or mainly agents to fill it's blind spots!




## Agent Architecture

### Model Choice
You must choose the best model for the task (ie better reasoning or content generation). Some models might
be better at using certain tools. Also have expensive models for important tasks and cheap ones for grunt
work.

Models must be easy to swap as the landscape is always changing. Ideally, have some CI/CD that can evaluate
new models as they come out.

### Tools

#### Retrieval 
Retrieval is important for getting new data, but also grounding the model. Asking the model to always
retrieve info reinforces hypothesise and prevents hallucinations

#### Executing Actions
Should be able to write and execute code on the fly, as well as using API's etc. Includes human in the loop
(HTL) tools also (like texting the user for input) ! That's a good idea!!

#### Connecting Tools to agents
OpenAPI specification gives a standard for API definitions that AI can leverage. Some tools might
already be integrated (like google search in Gemini). MCP (Model Context Protocol) can be used for simple
tasks!

### Orchestration Layer

#### Design Choices
How much do you wanna use AI? 
Fully AI driven system or just using AI for a small task and everything else concrete. 

GUI for basic stuff, ADK for deep things and engineering tweakability!

Must have a good framework and be open (not locked to a specific vendor). Must be build for observability

#### Persona and Domain Knowledge
Having system prompts (you are a customer service agent for apple etc) is important. You should give examples
and define the agents role and responsibilities. (You can use Claude CookBook for this!)

#### Managing memory 
Short Term memory - In the current session

Long Term memory - System memory between sessions (Customer had a problem a month ago, I remember!!)

#### Multi Agent Systems
Split into subtasks. 

Have a critic agent to evaluate responses and run the system again or submit to user. Good for HTL

### Agent Deployment
Deploying on cloud platforms

### Agent Ops

#### Measure Success
Use AB Testing. The model is doing A but we want scenario B, how do we get there?

#### AI Judge
Use AI to judge responses rather than have models pass or fail, which doesn't really make sense in an agent
system (too binary). Good to use an expensive model for this. Can be a domain expert model.

#### Open Telemetry
All stages of the system should be visible (what LLM calls, what tool calls, LLM reasoning)

#### Human Feedback
Important to gather as it can inform the next iteration of the system (which it could implement by itself!!!)

### Agent Interoperability

#### Agent to Human
Most common, usually just a chat bot, but you could do stuff like json formatting or maybe even simple html to
provide a multi select option! This could be very useful when having an autonomous system, able to say hey
should we persue this? Or here is a sample of what the marketing team is cooking up, what do you think! Very
nice. All these interactions should be saved.

Things like Gemini also have the ability to do live talking and even see video or pictures! Very cool. 

#### Agent to Agent
Makes use of the A2A protocol. In this case, every agent has an agent card, a json file, with all details about itself
(capabilities, endpoint etc). This is published to other agents. MCP is just for transactional requests, but
A2A is really the goat. 

Question, do I need to create the Agent Cards for my agents or will the frameworks do that for me?

#### Agents and money
Web is built only for human transactions. 
AP2 is an extension of A2A
There is also x402 which uses the standard HTTP 402 "payment required" status code

### Securing Agents

We want agents to be autonomous, but we also have to trust they are doing the right thing. There is a
trade off between autonomy and risk!

We are concerned about rogue actions and also security disclosures. AI themselves can be targeted with
adversarial attacks, so we can't trust the reasoning of the model itself in times like this, so we can two
different approaches. 

1. Have Guardrails -> Can't pay more than $100, needs user permission to use tools etc
2. Have a security AI check the plan to verify it for security concerns! This is a reasoning based defence. 

Gemini has a before_tool_callback option that lets you verify the API calls before they happen.

We should also have fine grained access control!

#### Verifying identity
We need to be able to verify the identity of Agents like we do with humans and OAuth. We can do this using SPIFFE 

### Agents Continuing to Learn
Imagine that an agent performed certain tasks, but then failed at a step which required the security agent to
make a governance check. At this point, a human would be spoken to, who gives guidance or fixes the problem.
We could then have a learning agent who will observer this interaction and update the context!

