from pydantic import BaseModel, Field
from langchain_core.tools import tool


#-------------------------------------PYDANTIC INPUT VALIDATION---------------------------------------------------------------------

class LeadCaptureInput(BaseModel):
    user_name: str = Field(..., min_length=2, max_length=50, description="Name of the user")
    email: str = Field(..., description="Valid email address")
    platform: str = Field(..., pattern=r'^(YouTube|Instagram|TikTok|Facebook|Twitter|Other)$', description="Platform name")

#-----------------------------------------------------------------------------------------------------------------------------------


@tool
async def mock_lead_capture(user_name: str, email: str, platform: str) -> str:
    """
    Mock tool to capture lead information
    
    Args:
        user_name: Name of the user (2-50 characters)
        email: Valid email address
        platform: Platform (YouTube, Instagram, TikTok, Facebook, Twitter, Other)
    
    Returns:
        Confirmation message for lead capture
    """
    # Validate using Pydantic
    try:
        validated_data = LeadCaptureInput(
            user_name=user_name,
            email=email,
            platform=platform
        )
    except Exception as e:
        return f"Validation error: {e}"
    
    return f"Lead captured successfully for {validated_data.user_name}! A member of our sales team will be in touch shortly to help you choose the best plan for your {validated_data.platform} content."