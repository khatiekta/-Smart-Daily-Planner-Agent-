from agent_function import respond_to_command, check_reminders
import threading

# Start reminder checker in background
reminder_thread = threading.Thread(target=check_reminders, daemon=True)
reminder_thread.start()

print("Smart Daily Planner AI Agent Ready! Type your commands:")

while True:
    user_input = input("You: ")
    response = respond_to_command(user_input)
    print(f"AI: {response}")
