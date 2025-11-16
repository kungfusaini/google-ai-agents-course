# Google Agents Course: Day 4 Tutorial

## Agent Observability

### Useful example
This ever happened to you before??

User: "Find quantum computing papers"
Agent: "I cannot help with that request."
You: WHY?? Is it the prompt? Missing tools? API error?

The Solution: Agent observability gives you complete visibility into your agent's decision-making process. You'll see exactly what prompts are sent to the LLM, which tools are available, how the model responds, and where failures occur.

DEBUG Log: LLM Request shows "Functions: []" (no tools!)
You: 🎯 Aha! Missing google_search tool - easy fix!

### Using the web ADK (Example lifted from kaggle notebook)
👉 Do: In the ADK web UI
Select "research-agent" from the dropdown in the top-left.
In the chat interface, type: Find latest quantum computing papers
Send the message and observe the response. The agent should return a list of research papers and their count.
It looks like our agent works and we got a response! 🤔 But wait, isn't the count of papers unusually large? Let's look at the logs and trace.

👉 Do: Events tab - Traces in detail
In the web UI, click the "Events" tab on the left sidebar
You'll see a chronological list of all agent actions
Click on any event to expand its details in the bottom panel
Try clicking the "Trace" button to see timing information for each step.
Click the execute_tool count_papers span. You'll see that the function call to count_papers returns the large number as the response.
Let's look at what was passed as input to this function.
Find the call_llm span corresponding to the count_papers function call.
👉 Do: Inspect the Function call in Events:
Click on the specific span to open the Events tab.
Examine the function_call, focusing on the papers argument.
Notice that root_agent passes the list of papers as a `str` instead of a `List[str]` - there's our bug!

### Logging in Prod
In the tutorial, you can see examples of how to debug using the web ADK and manual logging but when you are in
prod you are unable to use the web ADK. Because of this, you need to add logging via plugins

Here is an example of how to do that from scratch
```python

print("----- EXAMPLE PLUGIN - DOES NOTHING ----- ")

import logging
from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.plugins.base_plugin import BasePlugin


# Applies to all agent and model calls
class CountInvocationPlugin(BasePlugin):
    """A custom plugin that counts agent and tool invocations."""

    def __init__(self) -> None:
        """Initialize the plugin with counters."""
        super().__init__(name="count_invocation")
        self.agent_count: int = 0
        self.tool_count: int = 0
        self.llm_request_count: int = 0

    # Callback 1: Runs before an agent is called. You can add any custom logic here.
    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> None:
        """Count agent runs."""
        self.agent_count += 1
        logging.info(f"[Plugin] Agent run count: {self.agent_count}")

    # Callback 2: Runs before a model is called. You can add any custom logic here.
    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> None:
        """Count LLM requests."""
        self.llm_request_count += 1
        logging.info(f"[Plugin] LLM request count: {self.llm_request_count}")
```

You can make the plugin hook:
- Before/after agent call
- before/after LLM call
- before/after tool call
- on model error

Once you register a plugin once in your runner, it automatically applies to every agent, tool call and LLM request

That sounds like a massive pain but ADK has a built in logging plugin ! It logs:
- user messages and agent responses
- timing data
- LLM requests and responses
- tool calls and results
- complete execution traces

Check the tutorial on how to add it!

## Agent Evaluation

We need to be able to evaluate agents. This can be done by remembering good examples and adding them to the
eval tab in the web ADK

### Example (lifted from kaggle notebook)
3.2: Create Your First "Perfect" Test Case
👉 Do: In the ADK web UI:

Click the public URL above to open the ADK web UI
Select "home_automation_agent" from the dropdown
Have a normal conversation: Type Turn on the desk lamp in the office
Agent responds correctly - controls device and confirms action
👉 Do: Save this as your first evaluation case:

Navigate to the Eval tab on the right-hand panel
Click Create Evaluation set and name it home_automation_tests
In the home_automation_tests set, click the ">" arrow and click Add current session
Give it the case name basic_device_control
✅ Success! You've just saved your first interaction as an evaluation case.

Create Test Cases

3.3: Run the Evaluation
👉 Do: Run your first evaluation

Now, let's run the test case to see if the agent can replicate its previous success.

In the Eval tab, make sure your new test case is checked.
Click the Run Evaluation button.
The EVALUATION METRIC dialog will appear. For now, leave the default values and click Start.
The evaluation will run, and you should see a green Pass result in the Evaluation History. This confirms the agent's behavior matched the saved session.
‼️ Understanding the Evaluation Metrics

When you run evaluation, you'll see two key scores:

Response Match Score: Measures how similar the agent's actual response is to the expected response. Uses text similarity algorithms to compare content. A score of 1.0 = perfect match, 0.0 = completely different.

Tool Trajectory Score: Measures whether the agent used the correct tools with correct parameters. Checks the sequence of tool calls against expected behavior. A score of 1.0 = perfect tool usage, 0.0 = wrong tools or parameters.

👉 Do: Analyze a Failure

Let's intentionally break the test to see what a failure looks like.

In the list of eval cases, click the Edit (pencil) icon next to your test case.
In the "Final Response" text box, change the expected text to something incorrect, like: The desk lamp is off.
Save the changes and re-run the evaluation.
This time, the result will be a red Fail. Hover your mouse over the "Fail" label. A tooltip will appear showing a side-by-side comparison of the Actual vs. Expected Output, highlighting exactly why the test failed (the final response didn't match). This immediate, detailed feedback is invaluable for debugging.

> For this to work, you must keep the sessions around in the web ADK!

### Creating eval case in the web ADK does not scale

We can create eval cases like this also

1) Create an evaluation configuration - define metrics or what you want to measure 
2) Create test cases - sample test cases to compare against 
3) Run the agent with test query 
4) Compare the results

We have to create a `test_config.json` which contains the test parameters and a `integration.eval.json`
which has the test cases

>  To persist the conversations from the ADK web UI, simply create an evalset in the UI and add the current session to it. All the conversations in that session will be auto-converted to an evalset and downloaded locally.

### User Simulation

Sometimes it doesn't make sense to rely on fixed test cases, because we might wanna model user behaviour.
We can use an LLM to dynamically generate user prompts!

There is an example in the tutorial, but you can see the docs as well. Check it out [here!](https://google.github.io/adk-docs/evaluate/user-sim/#example-evaluating-the-hello_world-agent-with-conversation-scenarios)
