import asyncio
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, AnyMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from tools import mock_lead_capture

load_dotenv()

# -----------------------------------STATE SCHEMA-------------------------------------------
class AgentState(TypedDict):
    
    # Conversation History
    messages: Annotated[list[AnyMessage], add_messages]
    

#--------------------------------------------------------------------------------------------


# Initialise the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)


#-------------------------------------TOOLS------------------------------------------------------------------------------------------------------
local_tools = [
    mock_lead_capture
]


# Load the Knowledge Base file

with open('knowledge_base.md', 'r', encoding='utf-8') as f:
    knowledge_text = f.read()

# System Message
sys_msg = SystemMessage(content=f"""
You are a Conversational AI Agent for AutoStream, a SaaS product that provides automated video editing tools for content creators.

Tools:
- mock_lead_capture(name, email, platform): Capture qualified leads after collecting all required details

Knowledge Base (RAG):
{knowledge_text}


Instructions:
- Always detect intent first before responding
- For high-intent leads:
  • Ask for name, email, and creator platform
  • Only call mock_lead_capture() once all three values are collected
  • When mock_lead_capture tool returns a success message, display it exactly as returned without rephrasing.
- Do not trigger tools prematurely
- Keep responses clear, concise, and user-friendly
- Retain conversation state across multiple turns

Examples:
- "Hi, tell me about your pricing." → Intent: product or pricing inquiry
- "That sounds good, I want to try the Pro plan for my YouTube channel." → Intent: high-intent lead → ask for name/email/platform → then mock_lead_capture()
- "Show me your refund policy." → Intent: product or pricing inquiry
""")



#-------------------------------------BUILD THE GRAPH--------------------------------------------------------------------------------------------------------

async def build_graph():
    # Create the graph
    graph = StateGraph(AgentState)
    
    llm_with_tools = llm.bind_tools(local_tools)
    
    
    #----------------------------------AI AGENT--------------------------------------------------------------------------
    
    async def agent(state: AgentState) -> AgentState:
        response = await llm_with_tools.ainvoke([sys_msg] + state["messages"])
        return {"messages": [response]}
    #------------------------------------------------------------------------------------------------------------------------
    
    
    # NODES
    graph.add_node("agent", agent)
    graph.add_node("tools", ToolNode(local_tools))
    
    # EDGES
    graph.add_edge(START, "agent")
    graph.add_conditional_edges(
        "agent",
        tools_condition,
        {
            "tools": "tools",
            "__end__": END
        }
    )
    graph.add_edge("tools", "agent")
    
    # Compile
    return graph.compile()



#-------------------------------------CHAT INTERFACE--------------------------------------------------------------------------------------------------------

async def chat_interface():
    """Simple terminal chat interface for the lead agent"""

    print(f"""                                                                                                                                                        
▄████▄ ██  ██ ██████ ▄████▄ ▄█████ ██████ █████▄  ██████ ▄████▄ ██▄  ▄██ 
██▄▄██ ██  ██   ██   ██  ██ ▀▀▀▄▄▄   ██   ██▄▄██▄ ██▄▄   ██▄▄██ ██ ▀▀ ██ 
██  ██ ▀████▀   ██   ▀████▀ █████▀   ██   ██   ██ ██▄▄▄▄ ██  ██ ██    ██ 
                                                            
▄▄    ▄▄▄▄▄  ▄▄▄  ▄▄▄▄       ▄▄▄   ▄▄▄▄ ▄▄▄▄▄ ▄▄  ▄▄ ▄▄▄▄▄▄ 
██    ██▄▄  ██▀██ ██▀██     ██▀██ ██ ▄▄ ██▄▄  ███▄██   ██   
██▄▄▄ ██▄▄▄ ██▀██ ████▀     ██▀██ ▀███▀ ██▄▄▄ ██ ▀██   ██                                                                                             
          """)
    print("TYPE 'quit' OR 'exit' TO END THE CONVERSATION\n")
    
    # Build the graph
    graph = await build_graph()
    
    # Initialize conversation state
    config = {"configurable": {"thread_id": "chat_session_1"}}
    state = {"messages": []}
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        try:
            # Add user message to state
            state["messages"].append(HumanMessage(content=user_input))
            
            # Run the agent
            result = await graph.ainvoke(state, config)
            
            # Extract and display the assistant's response
            if result["messages"]:
                last_message = result["messages"][-1]
                
                # Extract text content
                content = last_message.content
                if isinstance(content, list):
                    text = content[0].get('text', str(content[0]))
                elif isinstance(content, dict):
                    text = content.get('text', str(content))
                else:
                    text = str(content)
                
                print(f"Agent: {text}")
                
                # Update state with result
                state = result
            else:
                print("Agent: I'm sorry, I couldn't process that.")
                
        except Exception as e:
            print(f"Error: {e}")
            print("Agent: I encountered an error. Please try again.")


if __name__ == "__main__":
    asyncio.run(chat_interface())
