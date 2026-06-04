students = []

while True:
    print("\n===== STUDENT RECORD SYSTEM =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter student name: ")
        age = input("Enter age: ")
        students.append({"name": name, "age": age})
        print("Student added successfully!")

    elif choice == "2":
        if not students:
            print("No student records found.")
        else:
            print("\nStudent Records:")
            for i, student in enumerate(students, start=1):
                print(f"{i}. Name: {student['name']}, Age: {student['age']}")

    elif choice == "3":
        if not students:
            print("No student records found.")
        else:
            for i, student in enumerate(students, start=1):
                print(f"{i}. {student['name']}")

            try:
                num = int(input("Enter student number to update: "))
                students[num - 1]["name"] = input("New name: ")
                students[num - 1]["age"] = input("New age: ")
                print("Student updated successfully!")
            except:
                print("Invalid student number!")

    elif choice == "4":
        if not students:
            print("No student records found.")
        else:
            for i, student in enumerate(students, start=1):
                print(f"{i}. {student['name']}")

            try:
                num = int(input("Enter student number to delete: "))
                removed = students.pop(num - 1)
                print(f"Deleted: {removed['name']}")
            except:
                print("Invalid student number!")

    elif choice == "5":
        print("Exiting program...")
        break

    else:
        print("Invalid choice. Try again.")