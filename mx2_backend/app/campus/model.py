from flask_mongoengine import Document
from mongoengine import StringField

class Campus(Document):
    name = StringField(required=True, max_length=200)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name
        }
