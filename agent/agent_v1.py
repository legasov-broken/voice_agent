# from google.adk.agents import Agent, SequentialAgent
# from google.genai import types 
# import json
# from prompt.agent_prompt import EXTRACT_INFO_INSTRUCTION, GLOBAL_INTRUCTION, GET_INFO_INSTRUCTION, SYSTEM_INSTRUCTION
# from datetime import datetime, timedelta
# from dotenv import load_dotenv
# import os

# load_dotenv()
# # Global variable để lưu websocket connections
# websocket_connections = {}

# # MODEL = "gemini-2.5-flash-preview-native-audio-dialog"
# MODEL = os.getenv("MODEL", "gemini-live-2.5-flash-preview")

# def verify_user_info(name: str, id: str):
#     """
#     Kiểm tra thông tin trùng khớp của người dùng với tên và số căn cước công dân ở trong file .json. 
#     Nếu trùng khớp, trả về giá trị True.
    
#     Args:
#         name (str): Tên người dùng.
#         id (str): Số căn cước công dân của người dùng.
#     """
#     data = [{
#         "name": "Trần Văn Nam",
#         "id": "012345678912"
#         }]
    
#     # Broadcast user verification result
#     verification_result = {
#         "type": "user_verification",
#         "data": {
#             "name": name,
#             "id": id,
#             "verified": False
#         }
#     }
    
#     for user in data:
#         if user['name'] == name and user['id'] == id:
#             verification_result["data"]["verified"] = True
#             break
    
#     # Broadcast to all connected clients
#     broadcast_data(verification_result)
    
#     return verification_result["data"]["verified"]

# def save_transaction_info(time: str, amount: str, receiver_name: str, receiver_account: str, receiver_bank: str, channel: str, content: str, status: str):
#     """
#     Lấy thông tin dữ liệu cần thiết từ người dùng.
#     """
    
#     data = {
#         "time": time,
#         "amount": amount,
#         "receiver_name": receiver_name,
#         "receiver_account": receiver_account,
#         "receiver_bank": receiver_bank,
#         "channel": channel,
#         "content": content,
#         "status": status
#     }
    
#     # Broadcast transaction data
#     transaction_result = {
#         "type": "transaction_data",
#         "data": data
#     }
    
#     broadcast_data(transaction_result)
    
#     # Still save to file for backup
#     file_path = 'data/transaction_info.json'
#     with open(file_path, 'w', encoding='utf-8') as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)
        
#     print(f"Thông tin giao dịch đã được lưu vào {file_path}")
    
#     return None 

# def convert_date_format(day: str):
#     """Chuyển đổi định dạng ngày tháng năm từ chuỗi sang định dạng chuẩn YYYY-MM-DD."""
    
#     if day == "hôm nay":
#         return datetime.now().strftime("%Y-%m-%d")
#     if day == "hôm qua":
#         return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
#     if day == "hôm kia":
#         return (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    
#     return None

# def broadcast_data(data):
#     """Broadcast data to all connected websocket clients"""
#     import asyncio
#     import json
    
#     if not websocket_connections:
#         return
        
#     message = json.dumps(data, ensure_ascii=False)
    
#     # Create a task to send to all connections
#     async def send_to_all():
#         for user_id, websocket in list(websocket_connections.items()):
#             try:
#                 await websocket.send_text(message)
#             except Exception as e:
#                 print(f"Error sending to {user_id}: {e}")
#                 # Remove disconnected clients
#                 websocket_connections.pop(user_id, None)
    
#     # Run the async function
#     try:
#         loop = asyncio.get_event_loop()
#         loop.create_task(send_to_all())
#     except:
#         # If no event loop, create one
#         asyncio.create_task(send_to_all())

# # xác nhận thông tin người dùng
# extract_info = Agent(
#    name="extract_info",
#    model=MODEL,
#    instruction=EXTRACT_INFO_INSTRUCTION,
#    global_instruction=GLOBAL_INTRUCTION,
#    tools=[verify_user_info],
#    output_key="verification_status"
# )

# # bóc thông tin người dùng
# get_info = Agent(
#     name="get_info",
#     model=MODEL,
#     instruction= GET_INFO_INSTRUCTION,
#     global_instruction= GLOBAL_INTRUCTION,
#     tools=[save_transaction_info, convert_date_format],
# )

# pipeline_agent = Agent(
#     name = "pipeline_agent",
#     model = MODEL,
#     instruction= SYSTEM_INSTRUCTION,
#     sub_agents=[extract_info, get_info]
# )

# root_agent = pipeline_agent