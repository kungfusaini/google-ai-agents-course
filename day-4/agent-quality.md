# Agent Quality Whitepaper

> Note: This paper has a lot of practical examples, if you wanna see some good implementation ideas, then
> check it out!

1. Agent quality is an architectural pillar, not a final testing phase.

2. Trajectory is Truth: Can't just evaluate the final output, every step of the process is crucial

3. Observability is Foundational: You have to be able to see everything that's happening

4. Human provided judgement or rubics are so important

5. Evaluation is a Continuous Loop

AI can pass 100 unit test and still fail in production because it's not a flaw in the code but a flaw in the
AI's judgement.

How do you debug things like hallucinations?

## Defining Agent Quality

We define agent quality according to four pillars:

1. Effectiveness (goal achievement) -> did it do what we asked of it
2. Efficiently (operational cost) -> Was the problem solved well (cost, time and number of steps)
3. Robustness (reliability) -> how well does the agent deal with unpredictable nature and does it fail
   gracefully)
4. Safety Alignment (trustworthiness) -> is it within ethical boundaries and constraints.

### Outside-In Evaluation
Metrics for task completion:
- Task success rate (Number for PRs accepted, number of successful database transactions)
- User satisfaction
- Overall Quality: If you say summaries these 10 articles, did it manage to actually do that?

> In ADK you can start a web session, and the save an ideal response as a benchmark (Eval case). Then you
> can rate the interactions to follow against this to test regression. It will also save the tool call for
> the Inside-Out eval

### Inside-Out Evaluation
Once Outside-In Evaluation fails, then we move to this and evaluation:
- LLM Plans
- Tool usage
- Tool response
- RAG performance 
- Trajectory (The steps we executed)
- Multi-Agent dynamics

### How to Evaluation

#### Automated Metrics
Basics but a good benchmark. Not because they eval quality, but because if it changes
that marks significant decrease in quality (regression)

#### LLM as a judge
LLM as a judge: requires 
    - Agent Output
    - Agent Prompt
    - Golden answer 
    - Eval rubic (rate helpfulness on 1-5, explain)    

It must be a powerful LLM (like Gemini Pro!). You can pass two answers and from two models in there and then
give the judge a rubic.

#### Agent as a judge
Similar to LLM as a judge but instead judges the whole trace and not just the final output

#### HITL
Is very subjective but good for establishing human-calibrated benchmarks

Good for evaluating:
- Domain Expertise
- Nuance
- Creating "Golden Sets" of answers

> Can use the interruption workflow

#### User Feedback
- Quick thumbs up and thumbs down
- Context rich review: Pairing feedback with context
- Reviewer UI: lets the user flag bad things in the reasoning trace on the fly
- Governance Dashboards

## Agent Observability

There are 3 main pillars
1. Logging
2. Traces
3. Metrics

### Logging
Basically the agents diary, everything it decided to do and did. Has the intent and outcome of the agent. 

There is a trade-off between information and performance

Can use log filtering (INFO, DEBUG etc)

### Traces
Traces connect log lines to show how they are connected!

Isolated Logs might show: ERROR: RAG search failed and ERROR: LLM response 
failed validation. You see the errors, but the root cause is unclear.
 A Trace reveals the full causal chain: User Query → RAG Search (failed) → 
Faulty Tool Call (received null input) → LLM Error (confused by bad 
tool output) → Incorrect Final Answer

OpenTelemetry is the standard, which composes of:
- Spans (operations with traces)
- Attributes (latency, token count etc)
- Context Propagation (links spans together with a trace_id)

### Metrics
The final score, derived from the logs and traces. Answers the question "How well did the performance go,
on average?"

#### System Metrics
Direct from the data

They track:
- Performance
    - Latency, Error Rate
- Cost
    - Tokens, API cost
- Effectiveness
    - Task Completion Rate, Tool use frequency

#### Quality Metrics
Come from applying the judgements we spoke about earlier onto the data
- Correctness & Accuracy
- Trajectory Adherence
- Safety & Responsibility
- Helpfulness & Relevance

### Getting Actionable Insights
How do we put all this together to make this meaningful?

1. Dashboards & Alerting: If something is wrong to display or notify, see how the system adapts and
evolves overtime or reacts to changes
2. Security: Must scrub personal data from logs
3. Granularity vs Overhead: Remember this trade-off! Can implement dynamic scaling (trace 10% of good logs but
100% of error logs)
but 

## Agent Quality Flywheel

Continuous improvement is so important! Here is the process for doing so

1. Define Quality (The Target): Effectiveness, cost efficiency, safety, user trust
2. Instrument of Visibility: You gotta be able to see everything!
3. Evaluate the process: We can now judge the performance!
4. Architect the feedback loop: Build the iteration loop into the system

