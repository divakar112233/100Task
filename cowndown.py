import time

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
    print("Time's up! ⏰")

# Main program
print("=== Countdown Timer ===")
try:
    seconds = int(input("Enter time in seconds: "))
    if seconds <= 0:
        print("Please enter a positive number!")
    else:
        countdown(seconds)
except ValueError:
    print("Invalid input! Please enter a number.")