import tkinter as tk
from tkinter import messagebox
import pywhatkit

def send_message():
    number = phone_entry.get()
    message = msg_box.get("1.0", tk.END)

    try:
        pywhatkit.sendwhatmsg_instantly(
            number,
            message,
            wait_time=15,
            tab_close=True
        )
        messagebox.showinfo("Success", "Message Sent!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Window
root = tk.Tk()
root.title("WhatsApp Sender")
root.geometry("400x350")
root.resizable(False, False)

# Title
title = tk.Label(
    root,
    text="WhatsApp Sender",
    font=("Arial", 18, "bold")
)
title.pack(pady=10)

# Phone Number
tk.Label(root, text="Phone Number (+Country Code):").pack()
phone_entry = tk.Entry(root, width=35)
phone_entry.pack(pady=5)

# Message
tk.Label(root, text="Message:").pack()
msg_box = tk.Text(root, height=8, width=35)
msg_box.pack(pady=5)

# Send Button
send_btn = tk.Button(
    root,
    text="Send Message",
    font=("Arial", 12, "bold"),
    command=send_message
)
send_btn.pack(pady=15)

root.mainloop()