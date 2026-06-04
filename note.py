notes = []

while True:
    print("\n===== NOTES APP =====")
    print("1. View Notes")
    print("2. Add Note")
    print("3. Delete Note")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        if not notes:
            print("No notes available.")
        else:
            print("\nYour Notes:")
            for i, note in enumerate(notes, start=1):
                print(f"{i}. {note}")

    elif choice == "2":
        note = input("Enter your note: ")
        notes.append(note)
        print("Note added successfully!")

    elif choice == "3":
        if not notes:
            print("No notes to delete.")
        else:
            for i, note in enumerate(notes, start=1):
                print(f"{i}. {note}")

            try:
                num = int(input("Enter note number to delete: "))
                removed = notes.pop(num - 1)
                print(f"Deleted: {removed}")
            except:
                print("Invalid note number!")

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid choice!")