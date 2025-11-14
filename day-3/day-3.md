# Google Agents Course: Day 3 Tutorial

## Sessions

Sessions are made up of Events (User input, tool call, response etc) and States (Scratchpad, key value pairs
available to all subagents)

ADK offers some tools to help, like the session manager and runner.
Session manager handles the creation, storage and retrieval of session data
Runner manges the flow of info between user and agent, maintains conversation history and manages context
engineering. 

Conceptually
- Session = A notebook
- Events = Individual entries in a single page
- SessionService = The filing cabinet storing notebooks
- Runner = The assistant managing the conversation


| Service | Use Case | Persistence | Best For |
|---|---|---|---|
| InMemorySessionService | Development & Testing | ❌ Lost on restart | Quick prototypes |
| DatabaseSessionService | Self-managed apps | ✅ Survives restarts | Small to medium apps |
| Agent Engine Sessions | Production on GCP | ✅ Fully managed | Enterprise scale |

When making an agent with DatabaseSessionService, literally all of the convo is stored, like this:
```python
('default', 'test-db-session-01', 'user', '{"parts": [{"text": "Hi, I am Sam! What is the capital of the United States?"}], "role": "user"}')
('default', 'test-db-session-01', 'text_chat_bot', '{"parts": [{"text": "Hi Sam! The capital of the United States is Washington, D.C."}], "role": "model"}')
('default', 'test-db-session-01', 'user', '{"parts": [{"text": "Hello! What is my name?"}], "role": "user"}')
('default', 'test-db-session-01', 'text_chat_bot', '{"parts": [{"text": "Your name is Sam!"}], "role": "model"}')
('default', 'test-db-session-01', 'user', '{"parts": [{"text": "What is the capital of India?"}], "role": "user"}')
('default', 'test-db-session-01', 'text_chat_bot', '{"parts": [{"text": "The capital of India is New Delhi."}], "role": "model"}')
('default', 'test-db-session-01', 'user', '{"parts": [{"text": "Hello! What is my name?"}], "role": "user"}')
('default', 'test-db-session-01', 'text_chat_bot', '{"parts": [{"text": "Your name is Sam!"}], "role": "model"}')

```

In this tutorial, we used ADK's default summarizer. For more advanced use cases, you can provide your own by defining a custom SlidingWindowCompactor and passing it to the config. This allows you to control the summarization prompt or even use a different, specialized LLM for the task.

ADK also provides Context Caching to help reduce the token size of the static instructions that are fed to the LLM by caching the request data.

You can create session tools that store and retrieval specific pieces of information! Like username and
location, it's good for that kind of thing!

## Memory
Memory provides capabilities that Sessions alone cannot:

| Capability | What It Means | Example |
| :--- | :--- | :--- |
| **Cross-Conversation Recall** | Access information from any past conversation | "What preferences has this user mentioned across all chats?" |
| **Intelligent Extraction** | LLM-powered consolidation extracts key facts | Stores "allergic to peanuts" instead of 50 raw messages |
| **Semantic Search** | Meaning-based retrieval, not just keyword matching | Query "preferred hue" matches "favorite color is blue" |
| **Persistent Storage** | Survives application restarts | Build knowledge that grows over time |
Session: They remember what you said 10 minutes ago in THIS conversation
Memory: They remember your preferences from conversations LAST WEEK

ADK provides multiple MemoryService implementations through the BaseMemoryService interface:

- InMemoryMemoryService - Built-in service for prototyping and testing (keyword matching, no persistence,
  stores everything without consolidation)
- VertexAiMemoryBankService - Managed cloud service with LLM-powered consolidation and semantic search
- Custom implementations - You can build your own using databases, though managed services are recommended
In the tutorial we used InMemoryMemoryService to learn the core mechanics. The same methods work identically with production-ready services like Vertex AI Memory Bank.


Configuration vs. Usage: Adding memory_service to the Runner makes memory available to your agent, but doesn't automatically use it. You must explicitly:
- Ingest data using add_session_to_memory()
- Enable retrieval by giving your agent memory tools (load_memory or preload_memory)


Two ways to load memory:
load_memory (Reactive)
- Agent decides when to search memory
- Only retrieves when the agent thinks it's needed
- More efficient (saves tokens)
- Risk: Agent might forget to search

preload_memory (Proactive)
- Automatically searches before every turn
- Memory always available to the agent
- Guaranteed context, but less efficient
- Searches even when not needed

Think of it like studying for an exam: load_memory is looking things up only when you need them, while preload_memory is reading all your notes before answering each question.

With manual memory fetching, you gotta match terms well. You can't ask for age if only birthday was mentioned.
You can't even ask for bday. This is a limitation  of the InMemoryMemoryService not the
VertexAiMemoryBankService (as that uses semantic search)

### Automatic Memory Saving
In order to automatically save sessions to memory after every turn, we need to use callbacks

```python
# Agent with automatic memory saving
auto_memory_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="AutoMemoryAgent",
    instruction="Answer user questions.",
    tools=[preload_memory],
    after_agent_callback=auto_save_to_memory,  # Saves after each turn!
)
```

| Timing | Implementation | Best For |
| :--- | :--- | :--- |
| **After every turn** | `after_agent_callback` | Real-time memory updates |
| **End of conversation** | Manual call when session ends | Batch processing, reduce API calls |
| **Periodic intervals** | Timer-based background job | Long-running conversations |

### Memory Consolidation

Before (Raw Storage):
User: "My favorite color is BlueGreen. I also like purple. 
       Actually, I prefer BlueGreen most of the time."
Agent: "Great! I'll remember that."
User: "Thanks!"
Agent: "You're welcome!"
→ Stores ALL 4 messages (redundant, verbose)

After (Consolidation):
Extracted Memory: "User's favorite color: BlueGreen"
→ Stores 1 concise fact

If you use VertexAiMemoryBankService, you get this for free!!!
