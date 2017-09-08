from mongoengine import *

from adapter import Adapter
from constants import Constants
from schema import User, Directory, File


def find_user_ref(func):
    def func_wrapper(self, user_name, *args, **kwargs):
        user = User.objects(user_name=user_name).first()
        if user is not None:
            return func(self, user, *args, **kwargs)
        else:
            return "User '{}' is not present".format(user_name), 400

    return func_wrapper


def find_dir_ref(func):
    def func_wrapper(self, owner_ref, dir_name, *args, **kwargs):
        dir_ref = Directory.objects(dir_name=dir_name, dir_owner=owner_ref).first()
        if dir_ref is None:
            return "Directory '{}' is not present".format(dir_name), 400
        return func(self, owner_ref, dir_ref, *args, **kwargs)

    return func_wrapper


def find_file_ref(func):
    def func_wrapper(self, owner, directory, file_name, *args, **kwargs):
        file = File.objects(file_name=file_name, file_home_dir=directory, file_owner=owner).first()
        if file is not None:
            return func(self, owner, directory, file, *args, **kwargs)
        else:
            return "File '{}' is not present".format(file_name), 400

    return func_wrapper


class MongoDBAdapter(Adapter):
    def __init__(self, db_name):
        connect(db_name)

    def delete_all_collections(self):
        self.delete_all_files()
        self.delete_all_dirs()
        self.delete_all_users()

    def delete_all_users(self):
        User.drop_collection()

    def delete_all_dirs(self):
        Directory.drop_collection()

    def delete_all_files(self):
        File.drop_collection()

    def get_username_list(self):
        answer = []
        for user in User.objects().only('user_name'):
            answer.append(user.user_name)
        return answer, 201

    def add_user(self, username, password):
        if User.objects(user_name=username).count() != 0:
            return "User '{}' already exists".format(username), 400
        if len(password) < Constants.min_password_length:
            return "Password is too short", 400
        new_user = User(username, password)
        new_user.save()
        return "User created", 201

    def get_password(self, username):
        query = User.objects(user_name=username)
        if query.count() != 1:
            return None
        else:
            return query.first().user_password

    @find_user_ref
    def delete_user(self, username):
        username.delete()
        username.save()
        return "Deleted user '{}'".format(username.user_name), 201

    @find_user_ref
    def update_user(self, username, password):
        if len(password) < Constants.min_password_length:
            return "Password is too short", 400
        username.user_password = password
        username.save()
        return "Updated user '{}'".format(username.user_name), 201

    @find_user_ref
    def add_directory(self, owner_name, dir_name):
        dir_count = Directory.objects(dir_name=dir_name, dir_owner=owner_name).count()
        if dir_count == 0:
            directory = Directory(dir_name, owner_name)
            directory.save()
            return "Created directory '{}'".format(dir_name), 201
        else:
            return "Directory '{}' already exists".format(dir_name), 400

    @find_user_ref
    @find_dir_ref
    def delete_directory(self, owner_name, dir_name):
        dir_name.delete()
        dir_name.save()
        return "Deleted directory '{}'".format(dir_name.dir_name), 201

    @find_user_ref
    @find_dir_ref
    def update_directory(self, owner_name, dir_name, new_dir_name):
        dir_count = Directory.objects(dir_name=new_dir_name, dir_owner=owner_name).count()
        if dir_count == 0:
            prev_dir_name = dir_name.dir_name
            dir_name.dir_name = new_dir_name
            dir_name.save()
            return "Updated directory '{}'->'{}'".format(prev_dir_name, new_dir_name), 201
        else:
            return "Can not rename directory into '{}', name already exists".format(new_dir_name), 400

    @find_user_ref
    def get_directory_list(self, username):
        answer = []
        for directory in Directory.objects(dir_owner=username):
            answer.append(directory.dir_name)
        return answer, 201

    @find_user_ref
    @find_dir_ref
    def add_file(self, owner_name, dir_name, filename, content):
        if File.objects(file_name=filename, file_home_dir=dir_name, file_owner=owner_name).count() == 0:
            file = File(filename, dir_name, owner_name, content)
            file.save()
            return "File '{}' created".format(filename), 201
        else:
            return "File '{}' exists".format(filename), 400

    @find_user_ref
    @find_dir_ref
    @find_file_ref
    def delete_file(self, owner_name, dir_name, filename):
        filename.delete()
        filename.save()
        return "Deleted file '{}'".format(filename.file_name), 201

    @find_user_ref
    @find_dir_ref
    @find_file_ref
    def update_file(self, owner_name, dir_name, filename, content):
        filename.file_content = content
        filename.save()
        return "Updated file '{}'".format(filename.file_name), 201

    def get_file(self, owner_name, dir_name, filename):
        owner = User.objects(user_name=owner_name).first()
        if owner is None:
            return {}, 400

        directory = Directory.objects(dir_name=dir_name, dir_owner=owner).first()
        if directory is not None:
            file = File.objects(file_name=filename, file_home_dir=directory, file_owner=owner).first()
            if file is not None:
                return file.file_content, 201
        return {}, 400

    def get_file_list(self, owner_name, dir_name):
        owner = User.objects(user_name=owner_name).first()
        if owner is None:
            return [], 400

        directory = Directory.objects(dir_name=dir_name, dir_owner=owner).first()
        if directory is not None:
            answer = []
            for file in File.objects(file_home_dir=directory, file_owner=owner):
                answer.append(file.file_name), 201
            return answer, 201
        return [], 400
