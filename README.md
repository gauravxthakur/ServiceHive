https://github.com/user-attachments/assets/b5241b1c-1897-4fb3-9b1e-74fcb9c277a5


# Social-to-Lead Agent

A conversational AI agent for AutoStream that converts social media conversations into qualified business leads using LangGraph and RAG.

## Quick Start

### Clone the repository
```bash
git clone https://github.com/gauravxthakur/ServiceHive.git
cd ServiceHive
```

### Create virtual environment
```bash
python -m venv venv
venv/Scripts/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Set up environment variables
```bash
GOOGLE_API_KEY = your_api_key
```

### Run the agent
```bash
python lead_agent.py
```

## Architecture

### Why LangGraph?

I chose **LangGraph** because:

1. **State Management**: LangGraph provides built-in state persistence across conversation turns through its `AgentState` schema and `thread_id` configuration
2. **Tool Integration**: Seamless tool binding with conditional routing between agent and tool nodes
3. **Visual Workflow**: Graph-based approach makes the agent flow (START -> agent -> tools -> END) explicit and debuggable
4. **Production Ready**: Better suited for real-world deployment with proper error handling and state recovery

### State Management

The agent maintains conversation state using:
- **AgentState TypedDict**: Stores message history with `add_messages` annotation
- **Thread-based Persistence**: Each conversation gets a unique `thread_id` for state isolation
- **LangGraph Memory**: Automatic state management across 5-6 conversation turns as required
- **Tool Context**: Tool results are automatically incorporated into conversation state

### RAG Implementation

Knowledge retrieval is implemented using:
- **External Knowledge Base**: `knowledge_base.md` file contains pricing, features, and policies
- **Dynamic Loading**: Knowledge is loaded at runtime and injected into the system prompt
- **Simple File Reading**: No vector databases used because the knowledge base is small (~7 lines) and the information is straightforward - using vector databases would be overengineering for this scale
- **Efficient Approach**: Direct file reading is faster and more maintainable for small knowledge bases while still providing full RAG benefits

## Agent Capabilities

### 1. Intent Identification
The agent classifies user intent into three categories:
- **Casual Greeting**: "Hi", "Hello", etc.
- **Product/Pricing Inquiry**: Questions about features, pricing, policies
- **High-Intent Lead**: Users ready to sign up or purchase

### 2. Lead Capture Workflow
When high-intent is detected:
1. Agent asks for name, email, and creator platform
2. Validates input using Pydantic models
3. Calls `mock_lead_capture()` tool only after all details collected
4. Returns confirmation message

### 3. Tool Execution
- **Input Validation**: Strict Pydantic validation for name length (2-50 chars), platform restrictions, and email format
- **Error Handling**: Graceful validation error messages
- **Output Control**: Tool results displayed exactly as returned without rephrasing

## WhatsApp Integration

To deploy this agent on WhatsApp using webhooks:

1. **WhatsApp Business API Setup**
   - Configure WhatsApp Business API endpoint
   - Set up webhook URL pointing to your server
   - Handle authentication and rate limiting

2. **Alternative Integration**
   - Third-party services like WHAPI Cloud can be used for simpler setup
   - Experience with such integrators available for implementation

2. **Message Processing**
   - Set up webhook endpoint to receive incoming messages
   - Extract message content and sender information
   - Process message through the agent
   - Send response back via WhatsApp API

3. **State Management**
   - Use phone number as `thread_id` for conversation persistence
   - Store conversation state in database or Redis
   - Handle webhook acknowledgments and rate limiting

4. **Deployment**
   - Deploy webhook endpoint (Flask/FastAPI) to receive WhAPI/WhatsApp Business API messages
   - Host on any cloud platform (Heroku, Vercel, AWS)
   - Add basic authentication and error handling

## File Structure

```
ServiceHive/
 lead_agent.py          # Main agent logic and LangGraph implementation
 tools.py              # Tool definitions and validation
 knowledge_base.md     # External knowledge base
 requirements.txt      # Python dependencies
 .env                  # Environment variables
 README.md            # This file
```

## Dependencies

- `langgraph`: State management and graph execution
- `langchain-google-genai`: Gemini LLM integration
- `pydantic`: Input validation
- `python-dotenv`: Environment variable management
- `asyncio`: Async execution support

## Evaluation Criteria Met

- **Agent Reasoning**: Intent detection and conversation flow

- **RAG Implementation**: External knowledge base integration

- **State Management**: LangGraph thread-based persistence

- **Tool Calling**: Proper lead capture with validation

- **Code Quality**: Clean, modular structure

- **Deployability**: Ready for real-world integration
