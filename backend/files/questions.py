from models.models import Questions
from databases.database import SessionLocal
import json

# with open("questions.json", "r") as file:
#     questions_data= json.load(file)
#     for item in questions_data:
#         for key, value in item.items():
#             if isinstance(value, list):
#                 print(f"{key}: {', '.join(value)}")
#             else:    
#                 print(f"{key}: {value}")
#         print("-" * 20)
# ------------------------------------------------------------------

# So we are writing a normal Python program (not an API) that:
# Reads a JSON file
# Converts each JSON item into a SQLAlchemy model
# Saves it into the database
# Closes the database connection safely
# This is called data seeding or bulk loading.

db = SessionLocal()
try:
    with open("C:\\Users\\AA\\Desktop\\FastAPI\\files\\questions.json", "r") as file:
        questions_data= json.load(file)
    objects = []
    for data in questions_data:    
        question= Questions(
                    question_text= data["question"],
                    option_a= data["options"][0],
                    option_b= data["options"][1],
                    option_c= data["options"][2],
                    option_d= data["options"][3],
                    correct_option= data["answer"]        
                )
        db.add(question)
    db.commit()
    print("questions inserted successfully")
except Exception as e:
    print("error", e)
    db.rollback()   
