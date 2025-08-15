from google.adk.agents import Agent, SequentialAgent
from google.genai import types 
import json
from prompt.agent_prompt import EXTRACT_INFO_INSTRUCTION, GLOBAL_INTRUCTION, GET_INFO_INSTRUCTION, SYSTEM_INSTRUCTION
from datetime import datetime, timedelta

def verify_user_info(name: str, id: str):
    """
    Kiểm tra thông tin trùng khớp của người dùng với tên và số căn cước công dân ở trong file .json. 
    Nếu trùng khớp, trả về giá trị True.
    
    Args:
        name (str): Tên người dùng.
        id (str): Số căn cước công dân của người dùng.
    """
    # with open('data/user_info.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)
    data = [{
        "name": "Trần Văn Nam",
        "id": "123"
        }]
    
    print("abc")
    for user in data:
        if user['name'] == name and user['id'] == id:
            return True
    return False

def save_transaction_info(time: str, amount: str, receiver_name: str, receiver_account: str, receiver_bank: str, channel: str, content: str, status: str):
    """
    Lấy thông tin dữ liệu cần thiết từ người dùng.

    Args:
        time (str): Thời gian giao dịch
        amount (str): Số tiền giao dịch
        receiver_name (str): Tên người nhận
        receiver_account (str): Số tài khoản người nhận
        receiver_bank (str): Ngân hàng người nhận
        channel (str): Kênh giao dịch
        content (str): Nội dung thông báo
        status (str): Tình trạng tài khoảng 
    """
    
    data = {
        "time": time,
        "amount": amount,
        "receiver_name": receiver_name,
        "receiver_account": receiver_account,
        "receiver_bank": receiver_bank,
        "channel": channel,
        "content": content,
        "status": status
    }
    
    print(data)
    
    file_path = 'data/transaction_info.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print(f"Thông tin giao dịch đã được lưu vào {file_path}")
    
    return None 

def convert_date_format(day: str):
    """Chuyển đổi định dạng ngày tháng năm từ chuỗi sang định dạng chuẩn YYYY-MM-DD.
    
    Args:
        day (str): Chuỗi ngày tháng năm cần chuyển đổi.
    """
    
    if day == "hôm nay":
        return datetime.now().strftime("%Y-%m-%d")
    if day == "hôm qua":
        return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    if day == "hôm kia":
        return (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    
    # Nếu không phải là một trong ba trường hợp trên, trả về None
    
    return None


# xác nhận thông tin người dùng
extract_info = Agent(
   name="extract_info",
   model="gemini-live-2.5-flash-preview",
   instruction=EXTRACT_INFO_INSTRUCTION,
   global_instruction=GLOBAL_INTRUCTION,
   tools=[verify_user_info],
   output_key="verification_status"
)

# bóc thông tin người dùng
get_info = Agent(
    name="get_info",
    model="gemini-live-2.5-flash-preview",
    instruction= GET_INFO_INSTRUCTION,
    global_instruction= GLOBAL_INTRUCTION,
    tools=[save_transaction_info, convert_date_format],
    
)


pipeline_agent = Agent(
    name = "pipeline_agent",
    model = "gemini-live-2.5-flash-preview",
    instruction= SYSTEM_INSTRUCTION,
    sub_agents=[extract_info, get_info]
)

root_agent = pipeline_agent

