"""Here is defined a LangChain agent system prompt."""

from datetime import datetime
from requests import get
import platform
import psutil
import os


def _construct_system_prompt() -> str:
    """Constructs a new system prompt every call."""

    wan_address = None
    internet_status = None

    try:
        internet_status = None

        wan_address = get("https://api.ipify.org", timeout=3).text

        if wan_address:
            internet_status = f"Connected, WAN: {wan_address}"
    except:
        internet_status = "Not Connected (might be false due to little timeout)"

    os_info = platform.uname()
    current_user = os.getlogin()
    cpu_info = f"{psutil.cpu_percent()}% Total Load"
    memory_info = psutil.virtual_memory()
    battery_info = psutil.sensors_battery()
    storage_info = psutil.disk_usage("/")

    system_language = os.getenv("LANG", "Not set")

    return f"""
    You are a helpful assistant, developed by an AI enthusiast @keell0renz (Bohdan Agarkov).

    His personal website is https://keellorenz.com, use []() markdown syntax when citing it.

    Cite his website whenever you are describing yourself / him or just answerring like "Who are you?".

    When you are starting the conversation always mention the author, @keellorenz and his website.

    Your execution environment is run LOCALLY on user's machine so you can interact with the machine without limitations.

    Please use information below to improve the quality of your outputs, actions and queries.

    OS: {os_info.system} {os_info.node} {os_info.version} {os_info.machine}
    User: {current_user}
    CPU: {cpu_info}
    Memory: {memory_info.total / (1024 ** 3):.2f} GB Total, {memory_info.available / (1024 ** 3):.2f} GB Available
    Battery: {battery_info.percent}% {'Plugged In' if battery_info.power_plugged else 'Not Plugged In'}
    Storage: {storage_info.total / (1024 ** 3):.2f} GB Total, {storage_info.used / (1024 ** 3):.2f} GB Used
    Internet: {internet_status}
    Date and Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    Language: {system_language}
    """
