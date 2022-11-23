from webbrowser import get
from app import create_app
from app.campus.model import Campus
from app.user.model import User, Admin, Student, Teacher, get_hash_password

print("Loading ... ")

create_app()

# drop all collections
Campus.objects().delete()
User.objects().delete()

c = Campus(name="Unimelb")
c.save()  # save the campus to the database

admin = Admin(username="admin",
              password=get_hash_password("password"),
              telephone="1234567",
              permissions=["system_owner", "campus_admin"],
              campus=c)

admin.save()

student = Student(username="student_1",
                  display_name="Tom",
                  password=get_hash_password("password"),
                  telephone="1234567",
                  wx="wechat123",
                  campus=c)
student.save()

teacher = Teacher(username="teacher_1",
                  display_name="Teacher",
                  password=get_hash_password("password"),
                  telephone="1234567",
                  abn="xxxxxxxxxxxxxxxxx!",
                  campus=c)
teacher.save()
