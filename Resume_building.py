

name = input("Enter your name: ")
email = input("Enter your email: ")
phone = input("Enter your phone number: ")
skills = input("Enter your skills (comma separated): ")
education = input("Enter your education: ")

resume = f"""
=========================
        RESUME
=========================

Name: {name}
Email: {email}
Phone: {phone}

Education:
{education}

Skills:
{skills}
"""

with open("resume.txt", "w") as file:
    file.write(resume)

print("Resume created successfully!")
print("Saved as resume.txt")