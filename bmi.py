from tkinter import *

def calculate_bmi():
    weight = float(weight_entry.get())
    height = float(height_entry.get())

    bmi = weight / (height ** 2)

    result_label.config(text=f"BMI: {bmi:.2f}")

root = Tk()
root.title("BMI Calculator")
root.geometry("300x250")

Label(root, text="Weight (kg)").pack()
weight_entry = Entry(root)
weight_entry.pack()

Label(root, text="Height (m)").pack()
height_entry = Entry(root)
height_entry.pack()

Button(root, text="Calculate BMI", command=calculate_bmi).pack(pady=10)

result_label = Label(root, text="", font=("Arial", 14))
result_label.pack()

root.mainloop()