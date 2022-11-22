from flask_mongoengine import Document
from mongoengine import StringField, ReferenceField, ListField
import bcrypt
import base64
import hashlib

# encrypt method


def get_hash_password(plain_text_password):

    # utf-8 is the default encoding to binary string
    # digest is the hash function which is used to generate the hash
    return bcrypt.hashpw(base64.b64encode(hashlib.sha256(plain_text_password.encode("utf-8")).digest()),
                         bcrypt.gensalt()).decode('utf-8')


# compare method plain_text_password and hashed_password(stored in db)
def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(base64.b64encode(hashlib.sha256(plain_text_password.encode("utf-8")).digest()),
                          hashed_password.encode('utf-8'))


class User(Document):
    username = StringField(required=True, unique=True, max_length=36)
    password = StringField(required=True)
    display_name = StringField()
    telephone = StringField()
    campus = ReferenceField('Campus', reverse_delete_rule='CASCADE')

    # allow to derive from this class
    meta = {"allow_inheritance": True}

    def to_dict(self):
        return {
            'id': str(self.id),
            'username': self.username,
            'display_name': self.display_name,
            'campus': self.campus.name,
            'telephone': self.telephone,

            # print class name
            'user_type': str(self._cls)
        }


class Student(User):
    wx = StringField()
    uni = StringField()
    enrolled_courses = ListField(ReferenceField('Course'))

    def to_dict(self):
        return super().to_dict() | {"wx": self.wx, "uni": self.uni, "enrolled_courses":[
            { 
                "id": str(course.id),
                "name": course.name,
                "uni_course_code": course.uni_course_code,
            } for course in self.enrolled_courses
        ]}


class Admin(User):
    permissions = ListField(StringField(), required=True, default=[])

    def to_dict(self):
        return super().to_dict() | {"permissions": self.permissions}


class Teacher(User):
    abn = StringField(max_length=20)

    def to_dict(self):
        return super().to_dict() | {"abn": self.abn}
