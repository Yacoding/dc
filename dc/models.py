from mongoengine import *

class TestModel(Document):
    test_key = StringField(required=True)
    test_value = StringField(max_length=50)