# Google Agents Course: Day 1 Tutorial

| Pattern | When to Use | Example | Key Feature |
| :--- | :--- | :--- | :--- |
| **LLM-based (sub\_agents)** | Dynamic orchestration needed | Research + Summarize | LLM decides what to call |
| **Sequential** | Order matters, linear pipeline | Outline → Write → Edit | Deterministic order |
| **Parallel** | Independent tasks, speed matters | Multi-topic research | Concurrent execution |
| **Loop** | Iterative improvement needed | Writer + Critic refinement | Repeated cycles |


## Sequential Agents
In a [[Multi-Agent System]] we usually have some kind of organiser agent that manages the other agents.
Previously, I had given the master agent an LLM prompt to say "Hey dude, use the other agents in this order"
But, this sucks because it might ignore the instruction.

So, we can use something known as a [[Sequential Agent]] who will force that certain agents follow a specific
order of events! Check out the day one exercise for this.

This will be very useful for the [[ai-workforce]] !

## Parallel Agents
Parallel agents are very useful when you wanna do things together, for example:
I have 3 reasearchs tasks that are independant, then an aggregator.

So I define a parallel agent (lets call it research team) that uses all the sub agents (the researchers)
and the I have a Sequential agent that calls first the research team and then then aggregator!

## Loop Agent
Finally, the loop agent is useful when you want iteration.

So let's say I wanna have a blog post that gets developed. 

First I would define an initial writing agent to take the prompt and write a first draft
Then, I define a critic agent, who gives feedback and if he is happy, outputs only "APPROVED"

I also define a function that will end the loop once the criteria is met

Then I define a refiner agent, who will take the feedback and the first story.
If the feedback was "APPROVED", it will call the exit function
Otherwise, it will overwrite the current story

Then a loop agent is defined, who will run the sub agents in a Sequential Loop. We also define the max
iterations here!

Finally we have a sequential agent who will run the initial story agent and then then loop agent!
