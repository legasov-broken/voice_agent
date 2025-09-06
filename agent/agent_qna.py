from google.adk.agents import Agent, SequentialAgent
from google.genai import types 
import json
from prompt.agent_prompt_qna import HELP_INSTRUCION, GLOBAL_INTRUCTION
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
# Global variable để lưu websocket connections
websocket_connections = {}

# MODEL = "gemini-2.5-flash-preview-native-audio-dialog"
MODEL = os.getenv("MODEL", "gemini-live-2.5-flash-preview")

# bóc thông tin người dùng
pipeline_agent = Agent(
    name="help_user",
    model=MODEL,
    instruction= HELP_INSTRUCION,
    global_instruction= GLOBAL_INTRUCTION,
)

root_agent = pipeline_agent