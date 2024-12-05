# gui_chatbot.py
import tkinter as tk
from tkinter import scrolledtext
import requests

# Function to send message to the chatbot server
def send_message():
    user_message = user_input.get()
    user_input.set("")  # Clear the input field

    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, f"You: {user_message}\n")

    # Send the message to the Flask server
    response = requests.post(
        "http://127.0.0.1:5000/chat",
        json={"message": user_message}
    )

    if response.status_code == 200:
        bot_response = response.json().get("response")
        chat_window.insert(tk.END, f"Bot: {bot_response}\n")
    else:
        chat_window.insert(tk.END, "Bot: Error receiving response from the server.\n")

    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)

# Create the main window
root = tk.Tk()
root.title("Health Science Chatbot")

# Create the chat window
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
chat_window.pack(pady=10)

# Create the user input field
user_input = tk.StringVar()
entry_field = tk.Entry(root, textvariable=user_input, width=50)
entry_field.pack(pady=5)

# Create the send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

# Start the Tkinter event loop
root.mainloop()
