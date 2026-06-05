# Poll Voting App

votes = {
    "Python": 0,
    "Java": 0,
    "C++": 0
}

while True:
    print("\nVote for your favorite language:")
    print("1. Python")
    print("2. Java")
    print("3. C++")
    print("4. Show Results and Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        votes["Python"] += 1
        print("Vote recorded for Python!")
    elif choice == "2":
        votes["Java"] += 1
        print("Vote recorded for Java!")
    elif choice == "3":
        votes["C++"] += 1
        print("Vote recorded for C++!")
    elif choice == "4":
        print("\nVoting Results")
        print("----------------")
        for option, count in votes.items():
            print(f"{option}: {count} votes")
        break
    else:
        print("Invalid choice!")