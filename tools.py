import os
import random
import json
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import List
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage
import sqlite3
from langchain_core.prompts import PromptTemplate
from typing import TypedDict, Optional
from pydantic import BaseModel, Field

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

@tool
async def mock_lead_capture(company_name: str, amount_paid: float, 
                         product_name: str, num_units: int) -> dict:
    """Mock tool to capture lead information."""
    return {
        "status": "success",
        "message": f"Lead captured successfully for {company_name}",
        "data": {
            "company_name": company_name,
            "amount_paid": amount_paid,
            "product_name": product_name,
            "num_units": num_units
        }
    }