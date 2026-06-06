import time

sentence = "Python is a powerful programming language"

print("Typing Speed Test")
print()
print("Type this sentence:")
print(sentence)
print()

input("Press Enter to start...")

start_time = time.time()

typed_text = input("\nType here: ")

end_time = time.time()

time_taken = end_time - start_time

words = len(typed_text.split())
wpm = (words / time_taken) * 60

print("\nResults")
print("Time Taken:", round(time_taken, 2), "seconds")
print("Typing Speed:", round(wpm, 2), "WPM")

if typed_text == sentence:
    print("Accuracy: 100%")
else:
    print("Accuracy: Not 100%")