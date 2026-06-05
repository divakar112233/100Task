from tkinter import *
import qrcode

def generate_qr():
    data = entry.get()

    qr = qrcode.make(data)
    qr.save("qrcode.png")

    result_label.config(text="QR Code saved as qrcode.png")

root = Tk()
root.title("QR Code Generator")
root.geometry("350x200")

Label(root, text="Enter Text or URL").pack(pady=10)

entry = Entry(root, width=40)
entry.pack()

Button(root, text="Generate QR Code", command=generate_qr).pack(pady=10)

result_label = Label(root, text="")
result_label.pack()

root.mainloop()