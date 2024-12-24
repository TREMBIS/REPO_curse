import motor.motor_asyncio
import string
from bson.objectid import ObjectId

#Инициализация базы данных
MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.curse
#получение таблиц из базы данных
student_collection = database.get_collection("students_collection")

password_collection = database.get_collection("passwords_collection")


# helpers

#Функция проверки строки на буквы
def isletter(name: str) -> bool:
    for n in name:
        if n.isdigit() or n in string.punctuation:
            return False
    return True

#Функции преобразования в формат записи в базе
def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "group": student["group"],
        "num": student["num"],
    }
    
def password_helper(password) -> dict:
    return {
        "id": str(password["_id"]),
        "group": password["group"],
        "num": password["num"],
        "password": password["password"],
    }

#Функция получения id записи студента из базы по номеру группы и номеру по списку   
async def get_student_id(group: str, num: int) -> str:
    student = await student_collection.find_one({"group": group, "num": num})
    try:    #проверяем что запись успешно найдена
        return student_helper(student)["id"]
    except:
        return None


#Функция получения всех записей о студентах из базы
async def retrieve_students() -> list():
    students = []
    async for student in student_collection.find():
        students.append(student_helper(student))
    return students


#Функция добавления записи студента в базу
async def add_student(student_data: dict) -> dict:
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)


#Функция получения записи студента из базы по ID
async def retrieve_student(id: str) -> dict:
    student = await student_collection.find_one({"_id": ObjectId(id)})
    try:    #проверяем что запись успешно найдена
        return student_helper(student)
    except:
        return None

"""
# Update a student with a matching ID
async def update_student(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        updated_student = await student_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_student:
            return True
        return False
"""

#Функция удаления записи студента из базы по ID
async def delete_student(id: str) -> bool:
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:     #Удаляем только если запись существует
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True
        
#Функция получения записи пароля из базы по номеру группы и номеру по списку         
async def retrieve_password(group: str, num: int) -> dict:
    password = await password_collection.find_one({"group": group, "num": num})
    try:    #проверяем что запись успешно найдена
        return password_helper(password)
    except:
        return None

#Функция добавления записи пароля в базу    
async def add_password(password_data: dict) -> dict:
    password = await password_collection.insert_one(password_data)
    new_password = await password_collection.find_one({"_id": password.inserted_id})
    return password_helper(new_password)
    
#Функция удаления записи пароля из базы по номеру группы и номеру по списку
async def delete_password(group: str, num: int) -> bool:
    password = await password_collection.find_one({"group": group, "num": num})
    if password:    #Удаляем только если запись существует
        await password_collection.delete_one({"group": group, "num": num})
        return True