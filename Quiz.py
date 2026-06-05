# Quiz Application

score = 0

questions = [
    {
        "question": "What is the capital of India?",
        "answer": "delhi"
    },
    {
        "question": "Which language is used for Python programming?",
        "answer": "python"
    },
    {
        "question": "How many days are there in a week?",
        "answer": "7"
    },
    {
        "question": "What is 5 + 5?",
        "answer": "10"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "answer": "mars"
    }
]

print("=== Welcome to the Quiz Application ===\n")

for q in questions:
    user_answer = input(q["question"] + " ").lower()

    if user_answer == q["answer"]:
        print("Correct!\n")
        score += 1
    else:
        print("Wrong Answer!\n")

print("Quiz Completed!")
print("Your Score:", score, "/", len(questions))