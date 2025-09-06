import os
import json
import asyncio
import base64
import warnings

from pathlib import Path
from dotenv import load_dotenv

from google.genai.types import (
    Part,
    Content,
    Blob,
)

from google.adk.runners import InMemoryRunner
from google.adk.agents import LiveRequestQueue
from google.adk.agents.run_config import RunConfig
from google.genai import types
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# from agent.agent_v1 import root_agent, websocket_connections

from agent.agent_qna import root_agent, websocket_connections


warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

load_dotenv()

APP_NAME = "ADK Streaming example"

session = None
runner = None

async def start_agent_session(user_id, is_audio=False):
    """Starts an agent session"""
    runner = InMemoryRunner(
        app_name=APP_NAME,
        agent=root_agent,
    )

    session = await runner.session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
    )

    modality = "AUDIO" if is_audio else "TEXT"

    run_config = RunConfig(
        speech_config=types.SpeechConfig(
            language_code="vi-VN",
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name="Zephyr"
                )
            ),
        ),
        # output_audio_transcription=True,
        # input_audio_transcription=True,
        # realtime_input_config=types.RealtimeInputConfig(
        #         automatic_activity_detection=types.AutomaticActivityDetection(
        #             disabled=False,  # True = tắt auto detection, False = bật auto detection
                    
        #             # GIẢM SENSITIVITY - ít nhạy hơn
        #             start_of_speech_sensitivity=types.StartSensitivity.START_SENSITIVITY_LOW,
        #             end_of_speech_sensitivity=types.EndSensitivity.END_SENSITIVITY_LOW,
                    
        #             # # Tăng thời gian để giảm sensitivity
        #             # prefix_padding_ms=500,  # Tăng từ 300 → 500ms (cần speech dài hơn mới commit)
        #             # silence_duration_ms=1000,  # Tăng từ 500 → 1000ms (cần im lặng lâu hơn mới kết thúc)
        #         ),
                
        #         activity_handling=types.ActivityHandling.START_OF_ACTIVITY_INTERRUPTS,
        #         # Options: START_OF_ACTIVITY_INTERRUPTS, NO_INTERRUPTION, ACTIVITY_HANDLING_UNSPECIFIED
                
        #         # turn_coverage=types.TurnCoverage.TURN_INCLUDES_ONLY_ACTIVITY,x
        #         # Options: TURN_INCLUDES_ONLY_ACTIVITY, TURN_INCLUDES_ALL_INPUT, TURN_COVERAGE_UNSPECIFIED
        #     ),    
        response_modalities=[modality],
    )

    live_request_queue = LiveRequestQueue()

    live_events = runner.run_live(
        session=session,
        live_request_queue=live_request_queue,
        run_config=run_config,
    )
    # return live_events, live_request_queue
    
    return live_events, live_request_queue, session, runner  # Thêm session, runner

async def agent_to_client_messaging(websocket, live_events):
    """Agent to client communication"""
    async for event in live_events:
        if event.turn_complete or event.interrupted:
            message = {
                "turn_complete": event.turn_complete,
                "interrupted": event.interrupted,
            }
            await websocket.send_text(json.dumps(message))
            print(f"[AGENT TO CLIENT]: {message}")
            continue

        part: Part = (
            event.content and event.content.parts and event.content.parts[0]
        )
        if not part:
            continue

        is_audio = part.inline_data and part.inline_data.mime_type.startswith("audio/pcm")
        if is_audio:
            audio_data = part.inline_data and part.inline_data.data
            if audio_data:
                message = {
                    "mime_type": "audio/pcm",
                    "data": base64.b64encode(audio_data).decode("ascii")
                }
                await websocket.send_text(json.dumps(message))
                print(f"[AGENT TO CLIENT]: audio/pcm: {len(audio_data)} bytes.")
                continue

        if part.text and event.partial:
            message = {
                "mime_type": "text/plain",
                "data": part.text
            }
            await websocket.send_text(json.dumps(message))
            print(f"[AGENT TO CLIENT]: text/plain: {message}")

async def client_to_agent_messaging(websocket, live_request_queue):
    """Client to agent communication"""
    while True:
        message_json = await websocket.receive_text()
        message = json.loads(message_json)
        mime_type = message["mime_type"]
        data = message["data"]

        if mime_type == "text/plain":
            content = Content(role="user", parts=[Part.from_text(text=data)])
            live_request_queue.send_content(content=content)
            print(f"[CLIENT TO AGENT]: {data}")
        elif mime_type == "audio/pcm":
            decoded_data = base64.b64decode(data)
            live_request_queue.send_realtime(Blob(data=decoded_data, mime_type=mime_type))
        else:
            raise ValueError(f"Mime type not supported: {mime_type}")

app = FastAPI()

STATIC_DIR = Path("static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def root():
    """Serves the index.html"""
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, is_audio: str):
    """Client websocket endpoint"""
    await websocket.accept()
    print(f"Client #{user_id} connected, audio mode: {is_audio}")

    # Add to connections registry
    user_id_str = str(user_id)
    websocket_connections[user_id_str] = websocket

    try:
        # live_events, live_request_queue = await start_agent_session(user_id_str, is_audio == "true")
        
        live_events, live_request_queue, session, runner = await start_agent_session(user_id_str, is_audio == "true")

        agent_to_client_task = asyncio.create_task(
            agent_to_client_messaging(websocket, live_events)
        )
        client_to_agent_task = asyncio.create_task(
            client_to_agent_messaging(websocket, live_request_queue)
        )

        tasks = [agent_to_client_task, client_to_agent_task]
        await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)

        live_request_queue.close()

    finally:
        # # Remove from connections registry
        # websocket_connections.pop(user_id_str, None)
        # print(f"Client #{user_id} disconnected")
        
        websocket_connections.pop(user_id_str, None)
    
        # Delete session if exists
        if session and runner:
            try:
                await runner.session_service.delete_session(
                    app_name=APP_NAME,
                    user_id=user_id_str,
                    session_id=session.id
                )
                print(f"Session {session.id} deleted for user {user_id_str}")
            except Exception as e:
                print(f"Error deleting session: {e}")
        
        print(f"Client #{user_id} disconnected")