import unittest

import requests


def get_response(response, prefix='response'):
    return response.json()[prefix]


def generate_user(username, password):
    return {"username": username, "password": password}


class ServerTest(unittest.TestCase):
    def assert_result(self, response, expected_code, expected_content):
        self.assertEqual(response.status_code, expected_code)
        self.assertEqual(get_response(response), expected_content)

    def setUp(self):
        self.user_prefix = "http://localhost:5000/file_storage/api/v1.0/user"
        self.file_prefix = "http://localhost:5000/file_storage/api/v1.0/root"

    def test_post_user(self):
        for i in range(3):
            requests.delete(self.user_prefix + "/user" + str(i), auth=('user' + str(i), '12345678'))
            json = {"username": "user" + str(i), "password": '12345678'}
            response = requests.post("http://127.0.0.1:5000/file_storage/api/v1.0/user", json=json)
            self.assert_result(response, 201, "User created")
        for i in range(3):
            requests.delete(self.user_prefix + "/user" + str(i), auth=('user' + str(i), '12345678'))

    def test_get_users(self):
        for i in range(3):
            requests.post(self.user_prefix, json={'username': 'user' + str(i), 'password': '12345678'})

        response = requests.get(self.user_prefix)
        self.assertEqual(response.status_code, 201)
        self.assertListEqual(get_response(response), ['user0', 'user1', 'user2'])

        for i in range(3):
            requests.delete(self.user_prefix + "/user" + str(i), auth=('user' + str(i), '12345678'))

    def test_delete_user(self):
        user = {"username": "delete_test", "password": "12345678"}
        requests.post(self.user_prefix, json=user)

        response = requests.delete(self.user_prefix + "/delete_test")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(get_response(response, 'error'), 'Unauthorized access')

        response = requests.delete(self.user_prefix + "/delete_test", auth=('delete_test', '12345678'))
        self.assert_result(response, 201, "Deleted user 'delete_test'")

        response = requests.delete(self.user_prefix + "/delete_test", auth=('delete_test', '12345678'))
        self.assertEqual(response.status_code, 403)

    def test_update_user(self):
        user = generate_user("update_user", "12345678")
        requests.post(self.user_prefix, json=user)

        update_info = {"password": "test_pass"}
        response = requests.put(self.user_prefix + "/update_user", json=update_info, auth=("update_user", "12345678"))
        self.assert_result(response, 201, "Updated user 'update_user'")

        response = requests.put(self.user_prefix + "/update_user", json=update_info, auth=("update_user", "12345678"))
        self.assertEqual(response.status_code, 403)

        response = requests.delete(self.user_prefix + "/update_user", auth=('update_user', 'test_pass'))
        self.assertEqual(response.status_code, 201)

    def test_add_directory(self):
        user = generate_user("dir_test_user", "12345678")
        requests.post(self.user_prefix, json=user)

        for i in range(3):
            response = requests.post(self.file_prefix, json={'directory_name': 'dir' + str(i)},
                                     auth=("dir_test_user", "12345678"))
            self.assert_result(response, 201, "Created directory 'dir" + str(i) + "'")

        for i in range(3):
            requests.delete(self.file_prefix + "/dir" + str(i), auth=("dir_test_user", "12345678"))

        requests.delete(self.user_prefix + "/dir_test_user", auth=("dir_test_user", "12345678"))

    def test_delete_directory(self):
        user = generate_user("dir_test_user", "12345678")
        requests.post(self.user_prefix, json=user)

        requests.post(self.file_prefix, json={'directory_name': 'dir'}, auth=("dir_test_user", "12345678"))

        response = requests.delete(self.file_prefix + "/dir", auth=("dir_test_user", "12345678"))
        self.assert_result(response, 201, "Deleted directory 'dir'")

        response = requests.delete(self.file_prefix + "/dir", auth=("dir_test_user", "12345678"))
        self.assert_result(response, 400, "Directory 'dir' is not present")

        requests.delete(self.user_prefix + "/dir_test_user", auth=("dir_test_user", "12345678"))

    def test_update_directory(self):
        user = generate_user("dir_test_user", "12345678")
        requests.post(self.user_prefix, json=user)

        requests.post(self.file_prefix, json={'directory_name': 'dir'}, auth=("dir_test_user", "12345678"))

        response = requests.put(self.file_prefix + "/dir", json={"directory_name": "1234"},
                                auth=("dir_test_user", "12345678"))
        self.assert_result(response, 201, "Updated directory 'dir'->'1234'")

        response = requests.delete(self.file_prefix + "/dir", auth=("dir_test_user", "12345678"))
        self.assertEqual(response.status_code, 400)

        response = requests.delete(self.file_prefix + "/1234", auth=("dir_test_user", "12345678"))
        self.assertEqual(response.status_code, 201)

        requests.delete(self.user_prefix + "/dir_test_user", auth=("dir_test_user", "12345678"))

    def test_get_directories(self):
        user = generate_user("dir_test_user", "12345678")
        requests.post(self.user_prefix, json=user)

        for i in range(3):
            requests.post(self.file_prefix, json={'directory_name': 'dir' + str(i)},
                          auth=("dir_test_user", "12345678"))

        response = requests.get(self.file_prefix, auth=("dir_test_user", "12345678"))
        self.assert_result(response, 201, ['dir0', 'dir1', 'dir2'])

        for i in range(3):
            requests.delete(self.file_prefix + "/dir" + str(i), auth=("dir_test_user", "12345678"))

        requests.delete(self.user_prefix + "/dir_test_user", auth=("dir_test_user", "12345678"))

    def test_get_files_in_dir(self):
        user = generate_user("file_test_user", "12345678")
        requests.post(self.user_prefix, json=user)
        requests.post(self.file_prefix, json={'directory_name': 'test_dir'}, auth=("file_test_user", "12345678"))

        for i in range(3):
            requests.post(self.file_prefix + "/test_dir", json={'filename': 'file' + str(i), 'filecontent': {"1": "1"}},
                          auth=("file_test_user", "12345678"))

        response = requests.get(self.file_prefix + "/test_dir", auth=("file_test_user", "12345678"))
        self.assert_result(response, 201, ['file0', 'file1', 'file2'])

        for i in range(3):
            requests.delete(self.file_prefix + "/test_dir/file" + str(i),
                            auth=("file_test_user", "12345678"))

        requests.delete(self.file_prefix + "/test_dir", auth=("file_test_user", "12345678"))
        requests.delete(self.user_prefix + "/file_test_user", auth=("file_test_user", "12345678"))

    def test_add_file(self):
        user = generate_user("file_test_user", "12345678")
        requests.post(self.user_prefix, json=user)
        requests.post(self.file_prefix, json={'directory_name': 'test_dir'}, auth=("file_test_user", "12345678"))

        for i in range(3):
            response = requests.post(self.file_prefix + "/test_dir",
                                     json={'filename': 'file' + str(i), 'filecontent': {"1": "1"}},
                                     auth=("file_test_user", "12345678"))
            self.assert_result(response, 201, "File 'file" + str(i) + "' created")

        for i in range(3):
            response = requests.delete(self.file_prefix + "/test_dir/file" + str(i),
                                       auth=("file_test_user", "12345678"))
            self.assertEqual(response.status_code, 201)

        requests.delete(self.file_prefix + "/test_dir", auth=("file_test_user", "12345678"))
        requests.delete(self.user_prefix + "/file_test_user", auth=("file_test_user", "12345678"))

    def test_update_file(self):
        user = generate_user("file_test_user", "12345678")
        requests.post(self.user_prefix, json=user)
        requests.post(self.file_prefix, json={'directory_name': 'test_dir'}, auth=("file_test_user", "12345678"))
        requests.post(self.file_prefix + "/test_dir",
                      json={'filename': 'update_file', 'filecontent': {"1": "1"}},
                      auth=("file_test_user", "12345678"))

        new_file_content = {"filecontent": {"test": "passed"}}
        response = requests.put(self.file_prefix + "/test_dir/update_file", json=new_file_content,
                                auth=("file_test_user", "12345678"))
        self.assert_result(response, 201, "Updated file 'update_file'")

        response = requests.get(self.file_prefix + "/test_dir/update_file",
                                auth=("file_test_user", "12345678"))
        self.assertEqual(get_response(response), {"test": "passed"})

        requests.delete(self.file_prefix + "/test_dir/update_file",
                        auth=("file_test_user", "12345678"))
        requests.delete(self.file_prefix + "/test_dir", auth=("file_test_user", "12345678"))
        requests.delete(self.user_prefix + "/file_test_user", auth=("file_test_user", "12345678"))

    def test_delete_file(self):
        user = generate_user("file_test_user", "12345678")
        requests.post(self.user_prefix, json=user)
        requests.post(self.file_prefix, json={'directory_name': 'test_dir'}, auth=("file_test_user", "12345678"))
        requests.post(self.file_prefix + "/test_dir",
                      json={'filename': 'delete_file', 'filecontent': {"1": "1"}},
                      auth=("file_test_user", "12345678"))

        response = requests.delete(self.file_prefix + "/test_dir/delete_file",
                                   auth=("file_test_user", "12345678"))
        self.assert_result(response, 201, "Deleted file 'delete_file'")

        response = requests.delete(self.file_prefix + "/test_dir/delete_file",
                                   auth=("file_test_user", "12345678"))
        self.assert_result(response, 400, "File 'delete_file' is not present")

        requests.delete(self.file_prefix + "/test_dir", auth=("file_test_user", "12345678"))
        requests.delete(self.user_prefix + "/file_test_user", auth=("file_test_user", "12345678"))

    def test_get_file(self):
        user = generate_user("file_test_user", "12345678")
        requests.post(self.user_prefix, json=user)
        requests.post(self.file_prefix, json={'directory_name': 'test_dir'}, auth=("file_test_user", "12345678"))
        requests.post(self.file_prefix + "/test_dir",
                      json={'filename': 'get_file', 'filecontent': {"1": "1"}},
                      auth=("file_test_user", "12345678"))

        response = requests.get(self.file_prefix + "/test_dir/get_file", auth=("file_test_user", "12345678"))
        self.assert_result(response, 201, {"1": "1"})

        requests.delete(self.file_prefix + "/test_dir/get_file",
                        auth=("file_test_user", "12345678"))
        requests.delete(self.file_prefix + "/test_dir", auth=("file_test_user", "12345678"))
        requests.delete(self.user_prefix + "/file_test_user", auth=("file_test_user", "12345678"))


if __name__ == '__main__':
    unittest.main()
