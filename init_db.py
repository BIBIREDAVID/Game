from app import db
from models import User, Quiz, Question

# Initialize the database
db.create_all()

# Add a sample quiz with questions
quiz = Quiz(title="General Knowledge Quiz")
db.session.add(quiz)
db.session.commit()

# Add sample questions to the quiz
q1 = Question(text="What is the capital of France?", choices="Paris,London,Berlin,Madrid", correct_answer="Paris", quiz_id=quiz.id)
q2 = Question(text="What is 2 + 2?", choices="3,4,5,6", correct_answer="4", quiz_id=quiz.id)

db.session.add(q1)
db.session.add(q2)
db.session.commit()

print("Database initialized and sample quiz added!")
