import re
import os

print("=" * 40)
print("      EMAIL EXTRACTOR TOOL")
print("=" * 40)

filename = input("Enter text file name: ")

# Check if file exists
if not os.path.exists(filename):
    print("Error: File not found!")
    exit()

# Read file
with open(filename, "r", encoding="utf-8") as file:
    content = file.read()

# Extract emails
emails = re.findall(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    content
)

# Remove duplicates
unique_emails = list(set(emails))

print("\n----- RESULTS -----")
print("Total Emails Found:", len(emails))
print("Unique Emails:", len(unique_emails))

if unique_emails:
    print("\nEmail List:")
    for num, email in enumerate(unique_emails, start=1):
        print(f"{num}. {email}")

    # Save results
    with open("extracted_emails.txt", "w") as output:
        for email in unique_emails:
            output.write(email + "\n")

    print("\nEmails saved to 'extracted_emails.txt'")
else:
    print("No email addresses found.")

print("\nThank you for using Email Extractor Tool!")