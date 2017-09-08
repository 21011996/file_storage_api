class Adapter:
    def get_username_list(self):
        pass

    def add_user(self, username, password):
        pass

    def get_password(self, username):
        pass

    def delete_user(self, username):
        pass

    def update_user(self, username, password):
        pass

    def add_directory(self, owner_name, dir_name):
        pass

    def delete_directory(self, owner_name, dir_name):
        pass

    def update_directory(self, owner_name, dir_name, new_dir_name):
        pass

    def get_directory_list(self, username):
        pass

    def add_file(self, owner_name, dir_name, filename, content):
        pass

    def update_file(self, owner_name, dir_name, filename, content):
        pass

    def delete_file(self, owner_name, dir_name, filename):
        pass

    def get_file(self, owner_name, dir_name, filename):
        pass

    def get_file_list(self, owner_name, dir_name):
        pass
