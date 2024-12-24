from typing import Optional

from pydantic import BaseModel, Field, validator

#модель для студентов
class StudentSchema(BaseModel):
    fullname: str = Field(...)  #Имя
    group: str = Field(...)     #Номер группы
    num: int = Field(...)       #Номер по списку группы

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "group": "М7О-105С-24",
                "num": "9",
            }
        }
        """
    @validator('surname')
    def check_surname(cls, v):
        if not v.isalpha():
            raise ValueError('Surname must contain only letters')
        return v
    @validator('num')
    def check_num(cls, v):
        if not v.isnumeric():
            raise ValueError('Number must contain only digits')
        return v
        """

"""
class UpdateStudentModel(BaseModel):
    fullname: Optional[str]
    group: Optional[str]
    num: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "group": "М7О-105С-24",
                "num": "9",
            }
        }
"""        
      
# Модель для паролей
class PasswordSchema(BaseModel):
    group: str      #Номер группы
    num: int        #Номер по списку группы
    password: str   #Пароль
    
"""    
    class Config:
        schema_extra = {
            "example": {
                "group": "М7О-105С-24",
                "num": "9",
                "password": "John Doe",
            }
        }
"""
#модель для композитных данных group/num        
class GroupNumRequest(BaseModel):
    groupNum: str
"""
    @validator('num')
    def check_num(cls, v):
        if not v.isnumeric():
            raise ValueError('Number must contain only digits')
        return v
    @validator('password')
    def check_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 symbols long')
        return v
"""
#Функция формирования ответа на запрос
def ResponseModel(data, message) -> dict:
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

"""
def ErrorResponseModel(error, code, message) -> dict:
    return {"error": error, "code": code, "message": message}
"""