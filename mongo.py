from pymongo import MongoClient
import pprint

class Student:
    def __init__(self, name, age, studies):
        self.name = name
        self.age = age
        self.studies = studies

    def connection(self):
        # Mongodb connection
        self.conn = MongoClient('mongodb://root:root@127.0.0.1:27017')
        # Mongodb database and repository
        db = self.conn.Estudiantes
        # Collections
        self.students = db.alumno  # Platforms

    def insert_student(self):
        # En este caso "insert_one" SIEMPRE con la estructura de diccionario
        self.students.insert_one({"Name": student.name, "Age": student.age, "Studies": student.studies})

    def presentation(self):
        # recoger los valores
        valores = self.students.find()

        # recorrer los valores del objeto "pymongo"
        for stu in valores:
            print(pprint.pformat(stu, indent=3))

    # def update_student(self):
    # self.students.update_one({"Name": "Nadeem"}, {"$set": {"Age": 22}})


if __name__ == "__main__":
    student = Student("Nadeem", 22, "CFGS")
    student.connection()
    student.insert_student()
    student.presentation()
