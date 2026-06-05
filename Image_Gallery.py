from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title("Image Gallery")

images = ["image1.jpg", "image2.jpg", "image3.jpg"]
index = 0

def show_image():
    global photo
    img = Image.open(images[index])
    img = img.resize((400, 300))
    photo = ImageTk.PhotoImage(img)
    label.config(image=photo)

def next_image():
    global index
    index = (index + 1) % len(images)
    show_image()

label = Label(root)
label.pack()

Button(root, text="Next", command=next_image).pack()

show_image()

root.mainloop()