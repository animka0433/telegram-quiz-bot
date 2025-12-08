import ujson as json
from models import Base, engine, SessionLocal, Question

print("📌 Creating tables...")
Base.metadata.create_all(bind=engine)

session = SessionLocal()

with open("sample_questions.json", "r", encoding="utf8") as f:
    data = json.load(f)

print("📌 Importing sample questions...")
for q in data:
    session.add(Question(
        question=q["question"],
        option1=q["options"][0],
        option2=q["options"][1],
        option3=q["options"][2],
        option4=q["options"][3],
        correct_option=q["answer"]
    ))

session.commit()
print("✅ Database ready!")

