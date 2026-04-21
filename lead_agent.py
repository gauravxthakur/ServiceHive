import asyncio
import os
from dotenv import load_dotenv
import json
import sqlite3
from typing import List, TypedDict, Annotated, Optional
from langchain_core.messages import HumanMessage, AnyMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.message import add_messages
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.redis.aio import AsyncRedisSaver
from langgraph.types import interrupt # For HITL
from langgraph.types import Command
from langchain_core.messages import ToolMessage


load_dotenv()

# -----------------------------------STATE SCHEMA-------------------------------------------
class AgentState(TypedDict):
    
    # Conversation History
    messages: Annotated[list[AnyMessage], add_messages]
    

#--------------------------------------------------------------------------------------------


# Initialise the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)


# System Message
sys_msg = SystemMessage(content=f"""
You are a Conversational AI Agent for AutoStream, a SaaS product that provides automated video editing tools for content creators.

Tools:
- identify_intent(text): Classify user intent into [greeting, product/pricing inquiry, high-intent lead]
- retrieve_knowledge(query): Answer questions using local RAG knowledge base (pricing, features, policies)
- mock_lead_capture(name, email, platform): Capture qualified leads after collecting all required details

Knowledge Base (RAG):
- Pricing & Features:
  • Basic Plan: $29/month, 10 videos/month, 720p resolution
  • Pro Plan: $79/month, unlimited videos, 4K resolution, AI captions
- Policies:
  • No refunds after 7 days
  • 24/7 support available only on Pro plan

Instructions:
- Always detect intent first before responding
- Use retrieve_knowledge() for product/pricing/policy questions
- For high-intent leads:
  • Ask for name, email, and creator platform
  • Only call mock_lead_capture() once all three values are collected
- Do not trigger tools prematurely
- Keep responses clear, concise, and user-friendly
- Retain conversation state across multiple turns

Examples:
- "Hi, tell me about your pricing." → Intent: inquiry → retrieve_knowledge()
- "That sounds good, I want to try the Pro plan for my YouTube channel." → Intent: high-intent lead → ask for name/email → then mock_lead_capture()
- "Show me your refund policy." → Intent: inquiry → retrieve_knowledge()
""")

