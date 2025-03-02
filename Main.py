import requests
import tkinter as tk
from tkinter import scrolledtext
import re  # To detect formatting patterns

API_URL = "https://ritzy-admitted-responsibility.glitch.me/"  # Your API URL

def get_ai_response(prompt):
    """Send user input to AI and return the raw response."""
    data = {"prompt": prompt, "history": []}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(API_URL, json=data, headers=headers, timeout=10)
        return response.text  # Return raw text

    except requests.exceptions.RequestException:
        return "Error: Unable to connect"

def format_ai_response(prefix, response):
    """Formats AI/User response with bold names, code blocks (```), bold (**text**), italic (*text*), and lists (- item)."""
    chat_box.config(state=tk.NORMAL)  # Enable writing

    # Insert "You:" or "SkymeBot:" in **bold white**
    chat_box.insert(tk.END, f"{prefix}: ", "bold_name")

    # Detect code blocks (```code```)
    code_blocks = re.split(r"```", response)
    
    for i, block in enumerate(code_blocks):
        if i % 2 == 1:  # Odd index -> Code block
            chat_box.insert(tk.END, block.strip() + "\n", "code_block")
        else:  # Normal text
            lines = block.split("\n")  # Split non-code text into lines
            for line in lines:
                if re.match(r"^\*\*.*\*\*$", line.strip()):  # **Bold**
                    chat_box.insert(tk.END, line.strip("**") + "\n", "bold_text")
                elif re.match(r"^\*.*\*$", line.strip()):  # *Italic*
                    chat_box.insert(tk.END, line.strip("*") + "\n", "italic_text")
                elif re.match(r"^- .*", line.strip()):  # Bullet points (- item)
                    chat_box.insert(tk.END, "• " + line.lstrip("-") + "\n", "bullet_text")
                else:
                    chat_box.insert(tk.END, line + "\n")  # Default text
    
    chat_box.insert(tk.END, "\n")  # New line after response
    chat_box.config(state=tk.DISABLED)  # Lock chat box

def send_prompt():
    """Handles user input and displays formatted AI response."""
    user_text = entry.get().strip()
    if not user_text:
        return  # Ignore empty input

    format_ai_response("You", user_text)  # Format user message

    entry.delete(0, tk.END)  # Clear input field

    response = get_ai_response(user_text)
    format_ai_response("SkymeBot", response)  # Format AI response

# Create the Tkinter GUI
root = tk.Tk()
root.title("SkymeBot Chat")

# Set dark mode colors
bg_color = "#222"  # Dark gray background
fg_color = "#EEE"  # Light gray text
input_bg = "#333"  # Darker input box
button_color = "#444"  # Button background
button_fg = "#EEE"  # Button text color

root.configure(bg=bg_color)  # Set window background

# Use grid layout for scaling
root.grid_rowconfigure(0, weight=1)  # Allow chat box to expand vertically
root.grid_columnconfigure(0, weight=1)  # Allow chat box to expand horizontally

# Chat box for displaying messages (set to read-only after adding text)
chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg=input_bg, fg=fg_color, insertbackground="white")
chat_box.grid(row=0, column=0, columnspan=2, sticky="nsew")  # Stretch in both directions
chat_box.config(state=tk.DISABLED)  # Make it read-only

# Define text formatting tags
chat_box.tag_config("bold_name", font=("Arial", 10, "bold"), foreground="#FFF")  # White for "You" & "SkymeBot"
chat_box.tag_config("bold_text", font=("Arial", 10, "bold"))  # Bold text
chat_box.tag_config("italic_text", font=("Arial", 10, "italic"), foreground="lightblue")  # Italic text
chat_box.tag_config("bullet_text", foreground="green")  # Green bullet points
chat_box.tag_config("code_block", font=("Courier New", 10), background="#111", foreground="lightgreen")  # Code block styling

# Input field
entry = tk.Entry(root, bg=input_bg, fg=fg_color, insertbackground="white")
entry.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

# Send button
send_button = tk.Button(root, text="Send", command=send_prompt, bg=button_color, fg=button_fg)
send_button.grid(row=1, column=1, sticky="e", padx=10, pady=5)

# Allow input box and button to scale horizontally
root.grid_columnconfigure(0, weight=1)  # Stretch input field
root.grid_columnconfigure(1, weight=0)  # Keep button fixed size

root.mainloop()
