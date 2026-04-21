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



#---------------------------------------PYDANTIC SCHEMA-----------------------------------------------------------------------

# INPUT VALIDATION
class LeadData(BaseModel):
    user_name: str = Field(..., description="Name of the user")
    email: str = Field(..., description="Email of the user")
    platform: str = Field(..., description="Platform of the user like Youtube, Instagram, etc.")
 

# OUTPUT VALIDATION
class LeadResponse(BaseModel):
    status: str
    message: str
    data: LeadData
    
#----------------------------------------------------------------------------------------------------------


@tool
async def mock_lead_capture(user_name: str, email: str, 
                         platform: str) -> LeadResponse:
    """Mock tool to capture lead information."""
    return LeadResponse(
        status="success",
        message=f"Lead captured successfully for {user_name}",
        data=LeadData(
            user_name=user_name,
            email=email,
            platform=platform
        )
    )