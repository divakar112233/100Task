from tkinter import *

running = False
seconds = 0

def update():
    global seconds
    if running:
        seconds += 1

        mins = seconds // 60
        secs = seconds % 60

        time_label.config(text=f"{mins:02}:{secs:02}")
        root.after(1000, update)

def start():
    global running
    if not running:
        running = True
        update()

def stop():
    global running
    running = False

def reset():
    global running, seconds
    running = False
    seconds = 0
    time_label.config(text="00:00")

# Window
root = Tk()
root.title("Stopwatch")
root.geometry("300x200")

# Time Display
time_label = Label(root, text="00:00", font=("Arial", 40))
time_label.pack(pady=20)

# Buttons
Button(root, text="Start", command=start, width=10).pack(pady=5)
Button(root, text="Stop", command=stop, width=10).pack(pady=5)
Button(root, text="Reset", command=reset, width=10).pack(pady=5)

root.mainloop()