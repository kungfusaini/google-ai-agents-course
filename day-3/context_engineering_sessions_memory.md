# Context Engineering, Sessions and Memory

## Context Engineering
[[Context Engineering]] is the **mise en place** for an agent. If prompt engineering is just getting the
recipe ready, the Context Engineering is also getting the ingredients, tools, understanding of the dish
presentation etc.

There are a few components:
- Context for guiding reasoning
    - System Instructions
    - Tool Definitions
    - Examples
- Evidence and Data
    - Long Term Memory
    - External Knowledge (RAG)
    - Tool Output
    - Subagent output
    - Artifacts (files)
- Conversational Info
    - Convo History
    - State/Scratchpad: temporary info
    - User Prompt

We might notice "context rot" as the context gets larger (basically the LLM getting more and more dumb as the
context grows)

### Flow of Context
1. Fetch - Agent retrieves context 
2. Prepare - Framework constructs the full prompt from the context
3. Invoke LLM and tools - Tools and model output added to context
4. Upload Context - New useful info stored into long term memory

### Sessions vs Memory
Sessions are like the workbench where you make stuff. It's a mess!
Memory is the filling cabinet into which you put completed work. It's organised.
We sort the context from the session into the Memory. 

## Sessions

Session history is distinct from content. Session history is the permanent unabridged transcript, but the
context is carefully crafted for a single turn. The context might contain only relevant stuff from the history
or might add some special formatting or preamble.

Google ADK uses shared session with using LLM driven delegation (sub-agents)

When using A2A or agent as tool, the agent's history is private, and it acts like a blackbox to other agents.

It's not easy for this private history to be swapped between frameworks easily. This can be circumvented by
using a shared MEMORY as the data is processed and is framework agnostic. 

Session data is retrieved on each turn, so it's useful to filter/compact them

## Context Management
The context window is like a suitcase. You don't wanna over or under pack, you need to pack exactly what you
need in the space!

There are 3 main approaches to context management:
1. Only include the last N messages
2. Have a token limit and don't include older message over the limit
3. Get another LLM to summarize the history every now and then (done async)
None of these actually effect the session history.

They can be triggered:
1. Count based: the convo goes above a number of messages (considered good enough)
2. Time based: after 30 mins
3. Event Based: After a task is done or a topic has ended.

## Memory
Generated from session memories or context, persists across sessions
RAG is for static external data whereas memory is for dynamic and user specific context

RAG = Expert on facts. Shared. Batch processed. Library
Memory = Expert on user. Isolated to prevent data leaks. Event based. Personal assistant

A memory has two components:
- Content: Framework agnostic   
    - Structured: developer declared {"seat_preference": "Window"}
    - Unstructured: The user prefers a window seat
- Metadata: Simple string containing unique ID on the memory, owner and labels describing content and source

Types of Info:
- Declarative memory: Info the agent has declared (facts, figures and events). What questions
- Procedural:  Skills and workflows. How questions

Organisation Patterns
- Collections: Content is multiple self contained NLP memories for a single user
- Structured User Profile: Contact card of new info on the user
- Rolling summary: all event into a single rolling memory. Master document, used to compact long sessions

Storage Architectures:
- Vector Databases:
    Knowledge based on semantic similarity (finds  closest matches to users query)
- Knowledge graphs: Entity (node) and relationships (edges). You traverse the graph to find connection. It's
  helpful for understanding connection sin data. Relational
- Hybrid approach

Memory Types:
- Explicit: Remember this, notes this down. Ashlyn's bday is xxx Implicitly: Ashlyn's bday is next Wednesday, help me find a gift Internal
- External: API calls to other memory

You can create memories from multimodal content, either by converting to text (easier) or storing the actual
media (harder to store and retrieve)

## Creating Memories
Done by the memory manager
1. Ingestion or raw data
2. Extraction & Filtering
3. Consolidation into existing memory (Merger, delete or create memory)
4. Storage: to vector database of knowledge graph

### Memory Extraction
We might have to tell the LLM what is a meaningful interaction so that it knows to create e a memory. WE do
this via examples and giving your own topic definitions

### Memory Provenance
The LLM needs to have a weighting of memories. 
This can be done by the source type, freshness and amount of times the memory is consolidates (how many
source)
Sources are 3 types:
- Bootstrapped data: Preloaded from internal systems,  like CRM. HIGH TRUST
- User Input: A form could be high trust but implicitly memories from convos could be less trustworthy
- Tool Output: Memories from tool output is generally discourages because they can be brittle and stale,
  better for short term.

Memories can be removed by:
- Being too old
- Being Low Confidence: weak inference and not corroborated
- Irrelevance

### Triggering Memory Generation
Can be done at:
- Session Completion
- Turn Cadence: eg 5 turns
- Real-time: every turn
- Explicit Command: Remember this!

Tradeoff between frequency (more memories at higher fidelity) but more expensive and context bloat! 
SHOULD ALWAYS BE ASYNC, it's EXPENSIVE!!

#### Memory As A Tool
You can explicitly get memory to work as a tool by calling the memory generation with some criteria for
important memories, and letting the framework do it for the whole session or just the last x turns

You can also get the LLM to extract the memories himself and then pass it to the memory bank

## Retrieving Memories

Can be done by:
- Relevance (Semantic)
- Recency
- Importance

Relying on just vector approaches is bad because just because something is similar doesn't mean it's fresh or
non-trivial. 

To get the data we could:
- LLM could rewrite the users vague query to get better info
- get the top 50 memories and then the LLM can re-rank them
- get a specialised retriever class!

When to get them:
- Proactive, start of every turn
- Reactive (Memory as a tool), but LLM might not know that something useful can be retrieved, you might have
  to tell him via tool prompts

Then the memories have to be injected into the context window. System prompts are good for stable global
memories (like user profiles) and memory as a tool is good for small immediate things. 
System prompts are high authority but also run the risk that the agent might be over-influenced by that, trying
to always relate back.
If you inject the memory into the convo via MAAT, the LLM might think it was something said in the convo not a
memory (dialogue injection)
 
## Evaluating Memories
Creation:
- Precision: Of all created how good are they
- Recall: Of all important facts, how many memories were made?
- F1 Score

Retrieval:
- Recall@K: Is the correct memory in the top K retrieved memories?
- Latency: How long does it take
