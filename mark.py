from tkinter import *
import markdown

def preview():
    result.delete("1.0", END)
    result.insert(END, markdown.markdown(text.get("1.0", END)))

root = Tk()
root.title("Simple Markdown Previewer")

text = Text(root, height=5, width=40)
text.pack()

Button(root, text="Preview", command=preview).pack()

result = Text(root, height=5, width=40)
result.pack()

root.mainloop()