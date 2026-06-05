from tkinter import *
from time import strftime

# Create window
root = Tk()
root.title("Digital Clock")
root.geometry("400x200")

# Function to update time
def update_time():
    current_time = strftime("%H:%M:%S %p")
    label.config(text=current_time)
    label.after(1000, update_time)

# Clock label
label = Label(
    root,
    font=("Arial", 40, "bold"),
    bg="black",
    fg="lime"
)
label.pack(expand=True, fill="both")

update_time()

root.mainloop()