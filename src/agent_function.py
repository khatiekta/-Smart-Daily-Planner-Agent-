from datetime import datetime, timedelta
import time
from plyer import notification
import json
import re

# Load existing tasks
try:
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
except FileNotFoundError:
    tasks = []

def save_tasks():
    with open("tasks.json", "w") as f:
        json.dump(tasks, f)

def add_task(task_name, due_time=None):
    tasks.append({"task": task_name, "due_time": due_time.isoformat() if due_time else None})
    save_tasks()
    print(f"Task added: {task_name}" + (f" at {due_time}" if due_time else ""))

def check_reminders():
    while True:
        now = datetime.now()
        for t in tasks:
            if t["due_time"]:
                due_time = datetime.fromisoformat(t["due_time"])
                if now >= due_time:
                    notification.notify(
                        title="Reminder",
                        message=f"Task: {t['task']}",
                        timeout=10
                    )
                    t["due_time"] = None
                    save_tasks()
        time.sleep(30)

def respond_to_command(command):
    command = command.lower()

    if "tasks" in command or "what are my tasks" in command:
        if not tasks:
            return "No tasks set."
        return "\n".join([f"- {t['task']}" + (f" (Due: {t['due_time']})" if t['due_time'] else "") for t in tasks])

    elif "remind me" in command:
        time_match = re.search(r"tomorrow at (\d{1,2})\s*(am|pm)", command)
        if time_match:
            hour = int(time_match.group(1))
            if time_match.group(2) == "pm" and hour != 12:
                hour += 12
            remind_time = datetime.now() + timedelta(days=1)
            remind_time = remind_time.replace(hour=hour, minute=0, second=0, microsecond=0)
            task_name = re.sub(r"remind me tomorrow at \d{1,2}\s*(am|pm)", "", command).strip()
            task_name = task_name if task_name else "Reminder"
            add_task(task_name, due_time=remind_time)
            return f"Reminder set for tomorrow at {hour % 12} PM for: {task_name}"
        return "Could not parse time. Please use 'Remind me tomorrow at [hour] AM/PM [task]' format."

    else:
        return "I didn't understand that command. You can ask for tasks or set reminders."
