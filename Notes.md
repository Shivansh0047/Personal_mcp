# MCP Notes

MCP (Model Context Protocol) is an open protocol that standardizes how AI models communicate with external tools, data sources, and services. It acts like a common interface between an LLM and the outside world.Instead of writing custom integrations for every tool, an application can use MCP-compatible servers, and any MCP-compatible AI client can use them.

Story of MCP -
1. After arrival of LLM (Chatgpt - 30 Nov 2022) enables us to interact with Machines in our natural world and had huge impact.
2. The biggest problem AI in different platforms couldn't understand each other. It created multiple AI words. We wanted a unified AI agent, but the biggest problem was the problem of Context. We need to paste thousands of line to ask one simple questions.
* Context - It is everything an AI can see when if generated a response. More formally, it refrers to the information that LLM uses to generate a response.
3. OpenAI introduces function calling in mid 2023. Function calling is a way using which LLMs can use ext functions. This Led to rise of Tools. Tools became a way to fetch context form different places.
4. This tools solution worked well, but there was another issue, we had to to write one function for each tool. There could be lots and lots of functions that we have to write. The problems was also maintence , which would also become diffcult. There could also be security issue. Every AI Tool is building its own way to call every API.
5. MCP provided a solution.
    1. MCP has 2 componenets - client (LLMs (generally)) and server (service to which we have to connect). The protocol of how these 2 components talk is called Model Context Protocol.
    2. Anthromic provided an SDK to make tools or LLMs MCP complimiant.
6. If we integrate our client and server with MCP, we just have to wirte code on server and on the client side, we do not have to write any code, just a config file to connect client. Server does all the heavy lifting.
7. Because no code on cliet side, this solved integrations problem. We just have to connect using CONFIG and also no maintiance is required.
8. Many popular chatbots are MCP compitable, so more valueable for services to build MCP servers.

## MCP Architecture

In the simplest version of MCP, there are 2 componenets -
1. Host - simply a LLM
2. Server - can obe of any provider like github, drive, etc.

A host never directly talks to server, it talks via Client. A client can speak same language as the server. Host gives a high-level request to Client, client converts it to MCP compatible request and sends it to server.

The relationship between client and server is one on one ie one client connects to one server. Each channel is Decoupled (independent of each other). This benefits in security, scalibility, parallelism.

### MCP Primitives
Things the server can offer to host like tools (actions the AI ask the server to perform, usually Dynamic resources), Resources (Structered data sources that the AI can read, like static resources), Prompts (Predefined prompt templates or instructions that the server offers to help shape the AI's behavior, this can take vague information and produce a detailed prompt for the help LLM).

#### Primitives - Standard Operations

- **Tools**
  - `tools/list` → Client asks the Server: *"What tools do you provide?"*
  - `tools/call` → Client tells the Server: *"Please run this tool with these arguments."*

- **Resources**
  - `resources/list` → Client asks: *"What resources are available?"*
  - `resources/read` → Client says: *"Give me the content of this resource."*
  - `resources/subscribe` / `unsubscribe` → Client subscribes or unsubscribes from updates.

- **Prompts**
  - `prompts/list` → Client asks: *"What prompt templates do you provide?"*
  - `prompts/get` → Client fetches a specific prompt template.

### MCP Data Layer
The data laer is the language and grammer of the MCP ecosystem that everyone agrees upon to communicate. In MCP, JSN RPC 2.0 serves as the fooundation of the data layer.

#### JSON RPC 2.0

Javascript Object Notation - Remote Procedure Call. 

A **Remote Procedure Call (RPC)** allows a program to execute a function on another computer as if it were local, hiding the details of network communication and data transfer. This abstraction makes it easier to build distributed applications. for example instead of writing add(2,3) locally, we send a request to the server saying "please run add with parameters 2 and 3".

JSON-RPC combines the concept of RPC with simplicity of JSON, allowing us to structure RPC request and responses in a JSON format.

We can send many requent in one (batching). We can also send notification, which do not need a response. We do not use id in the body of notification.

* The reason we use JSON-RPC for data layer is because it is lightweight, it supports bi-directional communication, It is transport-agnostic (like it works not qith http, but also stdio, websockts, or any other custom transport), It is tansport batching and it supports notification.

### MCP Transport Layer

Mechanism that movesJSON-RPC messages between the client and Server. The choice of transport depends on the type of server. MCP has two yupes of servers (remote and local). For local server we use STDIO mode of transport, for remote server we use HTTP/SSE.

**STDIO** referts to the build in streams every program has. It has stdin (input the program reads) and stdout (output the program writes). In MCP, the host launches the server as a subprocess on the same machine, which establishes a parent-child relationship between client and server. The host(client) writes JSON-RPC messgae into server's STDIN. The server reads those messages, processes them, and writes back responses to it's STDOUT. It's benefit is it is very fast, secure and simple.

**HTTP+SSE**. HTTP allows the host to reach Servers running anywhere, host sends JSON RPC request using POST requent with JSON payload. The transport supports standard HTTP auth methods (like API Keys). SSE stands for Server sent Events and it's an extenstion of HTTP. Using SSE the server sends multiple messages to client over a single open connection. Instead of sending one large JSON blob, the server can stream chunks of data as they are ready. It is ideal for long running tasks.

## MCP Lifecycle

It describes the complete sequence of steps that govern how the Host (client) and a server establish, use and end a connection during a session (complete duration of the connection of computer and server). It has 3 main stages - Initilization, Operation, Shut Down.

### Initialization
The first pahse between client server. It establishes rotocol version compatibility, exchnages and negotiate capabilities. It usually happens when we start our app. Steps
  - Client sends a initialize requent where we call the method initializa, and we send protocol version (in form of data) root, and sampling protocol version. 
  - The Server also sends its wn capabilities in response/
  - After successful initializaion, the client MUST send an *initialized* notification to indicate it is ready to begin normal operation.
  * The client should not send requent other than pings before the server has responded the initializa requent. Server shuld also not send requests other that pings and logging befre receiving the initialized notification.

#### Version Negotiation

Server has a config file which list the supported versions, if client's version exicts it sends initialized notification else it disconnects.

#### Capability Negotiation
Client and server capabilties establishes which protocol featres will be available during the session. It provides maorly 3 types of capabilities
  (Client capabilities)
  - roots - cilent gives access to the root dict
  - sampling - server can ask our AI for some help
  - elicitation - server can demand incomplete info form client, like asking fr API key or something else.
  (Server capabilities)
  - prompts
  - resources
  - tools
  - logging - server can send logging satemens to client, like in long running tasks, server can tell what is is doing from time to time to server
  (subcapibilitites)
  - listChanged - server sends a notification to server if there is a change
  - subscribe - if these is some chnage in a particular resource.

### Operation Phase
During this phase, the client and server exchange messages accoring to the negotiated capabilities. They respect the negotiated protocol varsion and only use capabilities that were successfuly negotiated.

#### Capability Discovery
CLient hits method of tools/list and server sends list of tools it has. Automatically this happens after initialization for tools/list, resource/list, prompt/list.

#### Tool calling
we hit tools/call , tell which tool we want to use along with its paramenttes and server replies.

### Shutdown Phase

One side (typically he client) initiates shutdown. No special JSON RPC shutdown message is defined. The transport layer is responsible for signaling termination.
  - In STDIO , for client initialed shutdown , it closes input stream to the child process (server), wats for tge server to exit , sends SIGTERM - signal terminate (to OS) if server does not exit in time. Sends SIGKILL if still unresponsive. For server initialted shutdown, server closes output stream and exit process.
  - In HTTP,  for cleint initialted shutdown, the client closes HTTP connection it opened to the server. for serevr initialted shutdown, the servar may close the connection form its side. The client must be prepared t detect a dropped connection and handle it.

### Special Cases
#### Pings

It is a lightweight requent/response method defined in MCP. It is bidirectional, and is used to check whether the other side (Host or server) is still alive and the connection is responsive. It is useful for checking if the other side is up before full initialize or if there's no activity for a while, a client may send periodic pings to prevent connection sliently dropped by the OS, proxies, or firewalls.

#### Error Handling

How the host(Client) and server signals that something went wrong with a requent. MCP inherits JSON RPS's standard error object format.
  ##### Common Error Codesremove 
    - **-32601 — Method not found**
      - **Meaning:** Called a method that doesn't exist or wasn't advertised.
      - **Example:** Host calls `prompts/list` but server never advertised `prompts`.

    - **-32602 — Invalid params**
      - **Meaning:** Request sent with wrong or missing parameters.
      - **Example:** Tool expects `{ "path": "..." }`, but client sends `{ "file": "..." }`.

    - **-32600 — Invalid Request**
      - **Meaning:** Malformed JSON-RPC request structure.
      - **Example:** Missing required fields like `jsonrpc` or `method`.

    - **-32700 — Parse error**
      - **Meaning:** JSON could not be parsed.
      - **Example:** Request body is not valid JSON.

    - **-32000 and above — Server-defined errors**
      - **Meaning:** Custom errors defined by the server (implementation-specific).
      - **Example:** Authentication failure, rate limit exceeded, quota errors, internal issues.

#### Timeout
It is about ensuring requests don't hang forver. It protects against unresponsive or overloaded servers. It ensures resources (memory, CPU) aren't held indefinitely. MCP SDK let client sets a per-requent timeout, if deadline passes with no result, client triggers a timeout and sends a cancellation notification to tell the server to stop.

#### Progress Notification

Used in long running tasks to tell client the progress.+ to let him know a requent is still making progress. Client includes a progressToken in the requent's _meta, Server can then send notification/progress updates while working.

## Types of Connection between client and server
1. using config files
2. using connectors - A **Connector** is a built-in feature that links Claude to MCP servers automatically without the need for manual setup or configuration. Most Claude Desktop users are **non-technical end-users** who just want Claude to "talk" to their apps (Notion, Google Drive, GitHub, Slack, etc.). They don't want to run servers, edit JSON, or worry about transports. The **Connector system** wraps an MCP server behind the scenes and handles authentication via OAuth (sign-in with Google, GitHub, etc.). This keeps things **easy, safe, and consistent**.

The reason why connectors are not always used because - Connectors are **officially built, hosted, and maintained** by Anthropic. They come with **OAuth login flows**, managed security, rate-limits, and guaranteed stability. If every MCP server were required to be a Connector, it would mean Anthropic has to **review, host, and secure every possible server** — which doesn't scale. Also MCP is designed so **anyone can write a server**. Forcing everything through Connectors would **close the ecosystem** and make you dependent on Anthropic to approve or publish servers.

* We can add titter, gogle drive , manim, filesystem, etc MCP server tools to our Claude desktop.

## Expense Tracker MCP Server
Expense Tracker MCP server se we can add and track our expenses. It will be integrated with claude desktop.

### Plan of action
  - Demo Calculator server
  - build expense local server
  - Improve and deploy to make it remote server

* We use 2 popular libries for MCP , MCP SDK (official python SDK and it has 3 sublibries mcp.server, mcp.client and mcp.cli (for debugging and testing)) and FastMCP (abstraction on MCP SDK and created by prefect, this is beginner friendly and easy to use, later it is adopted by MCP SDK). These is new fastmcp version 2.0 which breaks out from MSC SDK and it is standlone , community-driven and fastevolving lib. We will use fastmcp.

* uv - a new package manage (instad of pip) which is fast and better.

## Flow of Simple calculator with dice roll mcp local server-
1. We use @mcp.tool decorator to make a simple python function into a mcp server.
2. To degub we use a tool called mcp inspector. Run command *uv run fastmcp dev inspector main.py* (NOTE - Changed). It will start a behind the scene server. This works like postman for API testing but for mcp. To run use *uv run fastmcp run main.py*. Now after it is started, all the clients can connect to it. Since we current we do not have a custom client, we will simply write command to install it in claude desktop *uv run fastmcp install claude-desktop main.py* (NOTE - if shows not found use uv run fastmcp install claude-desktop main.py --config-path "<actual path of config file>" --name "<optional:can give any name>", also replace uv in config file it absolute path of uv)

## Flow of Expense Tracker mcp server-