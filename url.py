from tkinter import *
import pyshorteners

def shorten_url():
    long_url = url_entry.get()

    shortener = pyshorteners.Shortener()
    short_url = shortener.tinyurl.short(long_url)

    result_label.config(text=short_url)

root = Tk()
root.title("URL Shortener")
root.geometry("500x250")

Label(root, text="Enter Long URL").pack(pady=10)

url_entry = Entry(root, width=50)
url_entry.pack()

Button(root, text="Shorten URL", command=shorten_url).pack(pady=10)

result_label = Label(root, text="", wraplength=450)
result_label.pack()

root.mainloop()