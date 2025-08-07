from google.adk.agents import Agent
from google.genai import types 
from google.adk.tools import google_search  # Import the tool
import json
from prompt.extract_info import SYSTEM_INSTRUCTION, GLOBAL_INTRUCTION


def get_info(name: str, phone: str):
    """
    Get the phone number and the name of the user
    
    Args:
        name (str): The name of the user.
        phone (str): The phone number of the user.
    """
    data = {
        'name': name,
        'phone': phone
    }
    file_path: str = 'data/user_info.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"User info saved to {file_path}")
    
    return None



extract_info = Agent(
   name="extract_info",
   model="gemini-live-2.5-flash-preview",
   instruction=SYSTEM_INSTRUCTION,
   global_instruction=GLOBAL_INTRUCTION,
   tools=[get_info],
)
