import ujson as json
from models import SessionLocal, Question

session = SessionLocal()

file = "sample_questions.json"
data = json.load(open(file))

for q in data:
    session.add(Question(
        question=q["question"],
        option1=q["options"][0],
        option2=q["options"][1],
        option3=q["options"][2],
        option4=q["options"][3],
        correct_option=q["answer"],
        explanation=q["explanation"]  # 🆕
    ))

session.commit()
print("Imported", len(data), "questions with explanations!")

