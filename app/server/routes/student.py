from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from ..database import (
    add_student,
    delete_student,
    retrieve_student,
    retrieve_students,
    #update_student,
    get_student_id,
    retrieve_password,
    add_password,
    delete_password,
    isletter,
)
from ..models.student import (
    #ErrorResponseModel,
    ResponseModel,
    StudentSchema,
    #UpdateStudentModel,
    PasswordSchema,
    GroupNumRequest,
)

router = APIRouter()

#Маршрутизация добавления студента
@router.post("/students/", response_description="Student data added into the database")
async def add_student_data(student: StudentSchema = Body(...)) -> dict:
    
    student = jsonable_encoder(student)
    student_chk = await get_student_id(student["group"], student["num"])
    if student_chk:     #Если запись о студенте существует возвращаем ошибку
        raise HTTPException(status_code=422, detail="Student already exists")
    else:
        if isletter(student["fullname"].strip(' ')):   #Имя должно состоять только из букв и пробелов
            if student["num"] > 0:                  #номер по списку должен быть натуральным числом
                student = jsonable_encoder(student)
                new_student = await add_student(student)
                return ResponseModel(new_student, "Student added successfully.")
            else:       #Сообщаем о некорректном номере
                raise HTTPException(status_code=422, detail="Student num should be natural")
        else:           #Сообщаем о некорректном имени
            raise HTTPException(status_code=422, detail="Student name should contain only letters")

#Маршрутизация получения списка студентов
@router.get("/students/", response_description="Students retrieved")
async def get_students() -> dict:
    students = await retrieve_students()
    if students:        #Если в базе есть запись возвращаем, иначе выдаем ошибку
        return ResponseModel(students, "Students data retrieved successfully")
    raise HTTPException(status_code=404, detail="Empty list returned")

"""
@router.get("/students/{id}", response_description="Student data retrieved")
async def get_student_data(id):
    student = await retrieve_student(id)
    if student:
        return ResponseModel(student, "Student data retrieved successfully")
    raise HTTPException(status_code=404, detail="Student doesn't exist")
"""
 
#Маршрутизация получения конкретного студента 
@router.get("/student/", response_description="Student data retrieved")
async def get_student_data(group_num: str) -> dict:
    group, num = group_num.split('/')
    id = await get_student_id(group, int(num))  #Получаем id записи студента
    student = await retrieve_student(id)
    if student:        #Если в базе есть запись возвращаем, иначе выдаем ошибку
        return ResponseModel(student, "Student data retrieved successfully")
    raise HTTPException(status_code=404, detail="Student doesn't exist")

    
"""    
@router.put("/{id}")
async def update_student_data(id: str, req: UpdateStudentModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_student = await update_student(id, req)
    if updated_student:
        return ResponseModel(
            "Student with ID: {} name update is successful".format(id),
            "Student name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )
    
@router.delete("/students/{id}", response_description="Student data deleted from the database")
async def delete_student_data(id: str):
    deleted_student = await delete_student(id)
    if deleted_student:
        return ResponseModel(
            "Student with ID: {} removed".format(id), "Student deleted successfully"
        )
    raise HTTPException(status_code=404, detail="Student doesn't exist")
"""

#Маршрутизация удаления студента    
@router.delete("/students/", response_description="Student data deleted from the database")
async def delete_student_data(group_num: GroupNumRequest) -> dict:
    group_num = group_num.groupNum
    group, num = group_num.split('/')
    id = await get_student_id(group, int(num))  #Получаем id записи студента
    deleted_password = await delete_password(group, int(num))   #Удаляем запись о пароле
    deleted_student = await delete_student(id)                  #Удаляем запись о студенте
    if deleted_student:         #Если удалили успешно сообщаем, иначе возвращаем ошибку
        return ResponseModel(
            "Student with ID: {} removed".format(id), "Student deleted successfully"
        )
    raise HTTPException(status_code=404, detail="Student doesn't exist")


#Маршрутизация добавления пароля студенту    
@router.post("/passwords/", response_description="Password data added into the database")
async def add_password_data(password: PasswordSchema = Body(...)) -> dict:
    password = jsonable_encoder(password)
    student_chk = await get_student_id(password["group"], password["num"])
    if student_chk:     #Если запись о студенте существует
        password_chk = await retrieve_password(password["group"], password["num"])
        if password_chk:    #Если запись о пароле существует возвращаем ошибку
            raise HTTPException(status_code=422, detail="Password already exists")
        else:
            if len(password["password"]) > 8:     #номер по списку должен быть натуральным числом
                new_password = await add_password(password)     #Добавляем запись о пароле в базу
                return ResponseModel(new_password, "Password added successfully.")
            else:       #Сообщаем о некорректном номере
                raise HTTPException(status_code=422, detail="Password shoulld be at least 8 symbols")
    else:               #Сообщаем об отсутствии записи о студенте
        raise HTTPException(status_code=404, detail="Student doesn't exist")

#Маршрутизация получения пароля студента
@router.get("/passwords/", response_description="Password data retrieved")
async def get_password_data(group_num: str) -> dict:
    group, num = group_num.split('/')
    password = await retrieve_password(group, int(num))
    if password:    #Если запись о пароле существует возвращаем, иначе выдаем ошибку
        return ResponseModel(password, "Password data retrieved successfully")
    raise HTTPException(status_code=404, detail="Password doesn't exist")

#Маршрутизация удаления пароля студента    
@router.delete("/passwords/", response_description="Password data deleted from the database")
async def delete_password_data(group_num: GroupNumRequest) -> dict:
    group_num = group_num.groupNum
    group, num = group_num.split('/')
    deleted_password = await delete_password(group, int(num))   #Удаляем запись о пароле
    if deleted_password:    #Если удалили успешно сообщаем, иначе возвращаем ошибку
        return ResponseModel(
            "Password removed", "Password deleted successfully"
        )       #Иначе выдаем ошибку
    raise HTTPException(status_code=404, detail="Password doesn't exist")
    
    