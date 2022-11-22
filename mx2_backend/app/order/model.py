from flask_mongoengine import Document

from mongoengine import (
    StringField,
    ReferenceField,
    CASCADE,
    DateTimeField,
    BooleanField,
    FloatField)

from ..user.model import Student
from ..course.model import Course
from ..campus.model import Campus
from datetime import datetime


class Order(Document):
  student = ReferenceField(Student, reverse_delete_rule=CASCADE)
  course = ReferenceField(Course,reverse_delete_rule=CASCADE)
  created_time = DateTimeField(default=datetime.now)
  original_price = FloatField()
  paid = BooleanField(default=False)
  paid_time = DateTimeField()
  paid_comment = StringField(default="No comment")
  paid_price = FloatField()
  
  def to_dict(self):
    return {
      "id": str(self.id),
      "student": {
        "id": str(self.student.id),
        "username": self.student.username,
        "display_name": self.student.display_name,
      },
      "course": {
        "id": str(self.course.id),
        "name": self.course.name,
        "uni_course_code": self.course.uni_course_code,
      },
      "campus":self.course.campus.to_dict(),
      "created_time": self.created_time.isoformat(),
      "original_price": self.original_price,
      "paid": self.paid,
      "paid_time": self.paid_time and self.paid_time.isoformat() or None,
      "paid_comment": self.paid_comment,
      "paid_price": self.paid_price,
    }