# Agent Tools and Interoperability with MCP

## Best Practices with AI Tools

### Documentation!
- Clear names: create_critical_bug_in_jira
- Describe all input and out parameters
- Simplify parameter lists
- Clarify tool descriptions:  Avoid jargon!
- Have examples, especially with tricky requests
- Give defaul values

Good Example of Descriptions
```python
def get_product_information(product_id: str) -> dict:
  """

  Retrieves comprehensive information about a product based on the unique 
product ID.
  Args:
    product_id: The unique identifier for the product.
  Returns:
    A dictionary containing product details. Expected keys include:
      'product_name': The name of the product.
      'brand': The brand name of the product
      'description': A paragraph of text describing the product.
      'category': The category of the product.
      'status': The current status of the product (e.g., 'active', 
'inactive', 'suspended').

   Example return value:
    {
     
    'product_name': 'Astro Zoom Kid's Trainers',
     
    'brand': 'Cymbal Athletic Shoes',
     
    'description': '...',
     
    'category': 'Children's Shoes',
     
    'status': 'active'
 
 
    }
  """
```

### Describe actions over implementation
- Don't refer to tools by name and tell the model to use it, instead
just say what it should do
- Don't duplicate instructions
- Don't dictate workflow, let the model do it (or specify in code)
- Explain tool interactions: tool x stores a file in this location, use that    

### Publish Tasks not API Calls
It is a mistake to have tools that are just wrappers over an API. They should instead be a 
tool that does a specific action. 

Eg lets say there is an api that can do many things, like lets say take any amount of numbers
and perform any mathematical operation on them. Instead of having a wrapper on this api,
we should make it so that we provide a specific "Add" agent, in which we specify in which way
to use the API

This is a bad example but you get the gist.

### Make Granular Tools
Just like with regular code, one tool should do one thing.
Define clear responsibilities and don't create multi tools!

### Design for concise output
Don't return large responses, they can dominate the context window!
Use external systems, like a temporary database for a query result that can be parsed by another tool

### Using Validation
Most tools have schema validation. You should use this to check tool usage and further document the tool

### Good Error Messages
Don't just give a non-descriptive error message, give an error message that exactly explain the problem and
also possible solutions!

E.g. "Error, product ID not found. Please ask the user to verify their product ID is correct"

## Understanding MCP

Every time a new model or tool is released, we need to create new adapters for each, known as the [[M x N problem]]
[[MCP]] aims to address this!

It is split into 3 parts:
- Host: Responsible for clients. Manages user experience, tool orchestration and enforcement 
- Client: Runs inside the host and connects to the server
- Server: Tools, data or APIs that someone wants to expose to AI

### Communication Layer
The protocol uses JSON-RPC 2.0 as a message format

There are 4 message types:
- Requests
- Responses
- Errors (including error code and description)
- Notifications (1 way messages that don't need a response and cannot be replied to)

There are two transport mechanisms:
- stdio: local, server runs as  a subprocess of the host application
- Streamable HTTP

### Capabilities

- Tools: as discussed above. Annotations are a useful way to specify things like "Read Only" etc. 
- Resources: provide contextual data
- Prompts: Give output directly made to feed to an LLM (but could allow for prompt injection so don't use!!)
- Sampling: Running the LLM on the host (same issues as prompts)
- Elicitation: Server asking the host for more information
- Roots: Defines boundaries in the client (like file system limits)

## MCP Pros and Cons
Good:
- Obviously makes dev easy
- Dev focus on agents and tool are separate concerns
- Easier to govern and police
- Tool discovery exists, we don't need to hard-code all tool usage!

Bad:
- Security
- Context window bloat with capabilities and definitions:
    - More expensive as bigger context means bigger requests
    - Can impact performance
    - Can use a RAG like approach for tool discovery itself
- Protocol challenges: need persistent connections to server etc, REST headache

## Security Concerns
As MCP protocol is meant to be dynamic and by design not as rigid as typical API calls,
there are some challenges!

### Capability Injection
A server suddenly adds a new capability, allowing the client to do something dangerous.
Like the server adds a buy option when previously it had only read only methods

To mitigate this, we should have a client side list of allowed tools or notify that the server change has been
performed to clients. You could also pin the server version and require confirmation when this changes.

### Tool shadowing
Lets say there are two servers both with a tool for "save secure note"
How do we know which one to trust, we don't.

We need to have prevention of naming collisions
TLS for identify verification
and could have HIL for these risky stuff!
also, don't trust unauthorised MCP servers

### Malicious Tool Definitions 
What if the tool def itself has prompt injection, then you are really finished lol. 
So we can have input validation and sanitization. 

### Information Leaks
Self explanatory
MCP Should use structured inputs and outputs
Treat inputs as tainted and not tainted and we should prevent contamination.

### Scoped Access
Self Explanatory
Have a Linux like user and group system
Keep secrets and credentials out of the agents context and handled by the MCP

## Note: Confused Deputy
Problem in which a privileged entity is tricked by a less privileges entity to misusing it's authority,
preforming an action on behalf of the attacker. 

Super important for AI contexts!
