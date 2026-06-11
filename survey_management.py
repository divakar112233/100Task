import sqlite3
import datetime
import json

conn = sqlite3.connect('surveys.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS surveys (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    created_date TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY,
    survey_id INTEGER,
    question_text TEXT NOT NULL,
    question_type TEXT,  -- text, rating, multiple_choice
    options TEXT,        -- JSON for multiple choice options
    FOREIGN KEY (survey_id) REFERENCES surveys(id)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY,
    survey_id INTEGER,
    respondent_name TEXT,
    response_date TEXT,
    answers TEXT,        -- JSON of question_id: answer
    FOREIGN KEY (survey_id) REFERENCES surveys(id)
)''')

conn.commit()

def clear_screen():
    print("\n" * 40)

def create_survey():
    clear_screen()
    print("=== Create New Survey ===")
    title = input("Survey Title: ").strip()
    description = input("Description: ").strip()
    date = datetime.date.today().isoformat()
    
    cursor.execute("INSERT INTO surveys (title, description, created_date) VALUES (?, ?, ?)",
                   (title, description, date))
    survey_id = cursor.lastrowid
    conn.commit()
    print(f"✅ Survey created successfully! ID: {survey_id}")
    
    # Add questions
    while True:
        add_more = input("Add a question? (y/n): ").strip().lower()
        if add_more != 'y':
            break
        add_question(survey_id)
    return survey_id

def add_question(survey_id):
    print("\n--- Add Question ---")
    q_text = input("Question Text: ").strip()
    print("Types: text, rating (1-5), multiple_choice")
    q_type = input("Question Type: ").strip().lower()
    
    options = None
    if q_type == "multiple_choice":
        opts = []
        while True:
            opt = input("Add option (or press Enter to finish): ").strip()
            if not opt:
                break
            opts.append(opt)
        options = json.dumps(opts)
    
    cursor.execute("""INSERT INTO questions 
        (survey_id, question_text, question_type, options) 
        VALUES (?, ?, ?, ?)""", 
        (survey_id, q_text, q_type, options))
    conn.commit()
    print("✅ Question added!")

def take_survey():
    clear_screen()
    print("=== Take Survey ===")
    cursor.execute("SELECT id, title FROM surveys")
    surveys = cursor.fetchall()
    if not surveys:
        print("No surveys available.")
        input("Press Enter...")
        return
    
    print("Available Surveys:")
    for s in surveys:
        print(f"{s[0]}. {s[1]}")
    
    try:
        survey_id = int(input("\nEnter Survey ID: "))
    except:
        print("Invalid ID!")
        return
    
    # Get questions
    cursor.execute("SELECT id, question_text, question_type, options FROM questions WHERE survey_id=?", (survey_id,))
    questions = cursor.fetchall()
    if not questions:
        print("No questions in this survey.")
        return
    
    respondent = input("Your Name: ").strip()
    answers = {}
    
    for q in questions:
        q_id, q_text, q_type, opts = q
        print(f"\nQuestion: {q_text}")
        
        if q_type == "rating":
            while True:
                try:
                    ans = int(input("Rating (1-5): "))
                    if 1 <= ans <= 5:
                        answers[q_id] = ans
                        break
                    else:
                        print("Enter 1-5")
                except:
                    print("Invalid input")
        elif q_type == "multiple_choice":
            if opts:
                options = json.loads(opts)
                for i, opt in enumerate(options, 1):
                    print(f"{i}. {opt}")
                while True:
                    try:
                        choice = int(input("Choose option: "))
                        if 1 <= choice <= len(options):
                            answers[q_id] = options[choice-1]
                            break
                    except:
                        print("Invalid choice")
        else:  # text
            answers[q_id] = input("Answer: ").strip()
    
    answers_json = json.dumps(answers)
    date = datetime.date.today().isoformat()
    
    cursor.execute("""INSERT INTO responses 
        (survey_id, respondent_name, response_date, answers) 
        VALUES (?, ?, ?, ?)""", 
        (survey_id, respondent, date, answers_json))
    conn.commit()
    print("✅ Survey submitted successfully!")

def view_responses():
    clear_screen()
    print("=== Survey Responses ===")
    cursor.execute("""SELECT s.title, r.respondent_name, r.response_date, r.answers 
                      FROM responses r 
                      JOIN surveys s ON r.survey_id = s.id 
                      ORDER BY r.response_date DESC""")
    responses = cursor.fetchall()
    
    if not responses:
        print("No responses yet.")
    else:
        for resp in responses:
            print(f"Survey: {resp[0]} | Respondent: {resp[1]} | Date: {resp[2]}")
            try:
                answers = json.loads(resp[3])
                for qid, ans in answers.items():
                    print(f"  Q{qid}: {ans}")
            except:
                print("  Answers: ", resp[3])
            print("-" * 60)
    
    input("\nPress Enter to continue...")

def dashboard():
    clear_screen()
    print("=== Survey Management Dashboard ===")
    
    cursor.execute("SELECT COUNT(*) FROM surveys")
    total_surveys = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM responses")
    total_responses = cursor.fetchone()[0]
    
    print(f"Total Surveys     : {total_surveys}")
    print(f"Total Responses   : {total_responses}")
    
    cursor.execute("SELECT title, created_date FROM surveys ORDER BY created_date DESC LIMIT 5")
    recent = cursor.fetchall()
    print("\nRecent Surveys:")
    for r in recent:
        print(f"• {r[0]} ({r[1]})")
    
    input("\nPress Enter to continue...")

def main():
    while True:
        clear_screen()
        print("=== Survey Management System ===")
        print("1. Create New Survey (+ Questions)")
        print("2. Take / Submit Survey")
        print("3. View All Responses")
        print("4. Dashboard")
        print("5. Exit")
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            create_survey()
        elif choice == '2':
            take_survey()
        elif choice == '3':
            view_responses()
        elif choice == '4':
            dashboard()
        elif choice == '5':
            print("Thank you for using Survey Management System!")
            break
        else:
            print("Invalid choice!")
        
        if choice != '5':
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    print("Welcome to Survey Management System!")
    main()
    conn.close()
