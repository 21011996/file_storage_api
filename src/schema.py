from mongoengine import *

from src.constants import Constants


class User(Document):
    user_name = StringField(required=True, unique=True)
    user_password = StringField(required=True, min_length=Constants.min_password_length)


class Directory(Document):
    dir_name = StringField(required=True)
    dir_owner = ReferenceField(User, required=True, unique_with='dir_name')


class File(Document):
    file_name = StringField(required=True)
    file_home_dir = ReferenceField(Directory, required=True)
    file_owner = ReferenceField(User, required=True, unique_with=['file_name', 'file_home_dir'])
    file_content = DictField(required=True)
