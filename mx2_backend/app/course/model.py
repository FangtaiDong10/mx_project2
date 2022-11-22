from mongoengine import (
    StringField,
    ReferenceField,
    ListField,
    CASCADE,
    DateTimeField,
    FloatField,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    EmbeddedDocumentField,
    UUIDField
)
from flask_mongoengine import Document
from datetime import datetime
import uuid
from ..utils import generate_s3_signed_url

class LectureAttachment(EmbeddedDocument):
    # store the files (using AWS S3 to store files)
    name = StringField()
    type = StringField()
    filename = StringField()
    bucket_url = StringField()

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "filename": self.filename,
            "signed_url": generate_s3_signed_url(self.bucket_url),
        }
    


class Lecture(EmbeddedDocument):
    id = UUIDField(required=True, binary=False, default=uuid.uuid4)
    title = StringField(defualt="Untitled")
    streaming_url = StringField()
    recording_url = StringField()
    attachments = EmbeddedDocumentListField(LectureAttachment)
    scheduled_time = DateTimeField()

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "streaming_url": self.streaming_url,
            "recording_url": self.recording_url,
            "attachments": [attachment.to_dict() for attachment in self.attachments],
            "scheduled_time": self.scheduled_time and self.scheduled_time.isoformat() or None,
        }    

class Course(Document):
    name = StringField(required=True, max_length=200)
    uni_course_code = StringField(required=True, max_length=200)
    description = StringField(required=True, max_length=200)
    teacher = ReferenceField("Teacher", reverse_delete_rule=CASCADE)
    campus = ReferenceField("Campus", reverse_delete_rule=CASCADE)
    created_time = DateTimeField(default=datetime.now)
    publish_time = DateTimeField(default=datetime.now)
    original_price = FloatField()
    cover_image = StringField()
    lectures = EmbeddedDocumentListField(Lecture)
    enrolled_students = ListField(ReferenceField("User"))

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "uni_course_code": self.uni_course_code,
            "description": self.description,
            "teacher": {
                "id": str(self.teacher.id),
                "display_name": self.teacher.display_name,
            },
            "campus": self.campus.to_dict(),
            "created_time": self.created_time.isoformat(),
            "publish_time": self.publish_time.isoformat(),
            "original_price": self.original_price,
            "cover_image": self.cover_image,
            "students_count": len(self.enrolled_students)
        }
