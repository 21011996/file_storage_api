import unittest

from db_adapter import MongoDBAdapter


class MongoDBAdatperTest(unittest.TestCase):
    def setUp(self):
        self.adapter = MongoDBAdapter('test')
        self.adapter.delete_all_collections()
        for i in range(3):
            self.adapter.add_user('user' + str(i), '12345678')
            for j in range(2):
                self.adapter.add_directory('user' + str(i), 'dir' + str(j))
                for k in range(1):
                    self.adapter.add_file('user' + str(i), 'dir' + str(j), 'file' + str(k),
                                          {'test_file': str(i + j + k)})

    def test_add_user(self):
        answer, code = self.adapter.add_user('user', '1234')
        self.assertEqual(answer, 'Password is too short')
        self.assertEqual(code, 400)

        answer, code = self.adapter.add_user('user', '12345678')
        self.assertEqual(answer, 'User created')
        self.assertEqual(code, 201)

        answer, code = self.adapter.add_user('user', '12345678')
        self.assertEqual(code, 400)

    def test_get_username_list(self):
        answer, code = self.adapter.get_username_list()
        self.assertEqual(answer, ['user0', 'user1', 'user2'])
        self.assertEqual(code, 201)

    def test_get_password(self):
        self.assertIsNone(self.adapter.get_password('wrong_user'))
        for i in range(3):
            self.assertEqual(self.adapter.get_password('user' + str(i)), '12345678')

    def test_update_user(self):
        self.adapter.add_user('update_test', 'qwerasdf')
        answer, code = self.adapter.update_user('update_test', '1234')
        self.assertEqual(answer, 'Password is too short')

        answer, code = self.adapter.update_user('update_test', '12345678')
        self.assertTrue(answer.startswith('Updated user'))
        self.assertEqual(code, 201)

    def test_delete_user(self):
        self.adapter.add_user('update_test', 'qwerasdf')
        answer, code = self.adapter.delete_user('update_test')
        self.assertTrue(answer.startswith('Deleted user'))
        self.assertEqual(code, 201)

        answer, code = self.adapter.delete_user('update_test')
        self.assertEqual(code, 400)

    def test_add_directory(self):
        answer, code = self.adapter.add_directory('user0', 'dir1')
        self.assertEqual(answer, 'Directory \'dir1\' already exists')
        self.assertEqual(code, 400)

        answer, code = self.adapter.add_directory('user0', 'test_add_dir')
        self.assertEqual(answer, 'Created directory \'test_add_dir\'')
        self.assertEqual(code, 201)

    def test_update_dir(self):
        self.adapter.add_directory('user1', 'update_test')
        answer, code = self.adapter.update_directory('user1', 'update_test', 'updated_dir')
        self.assertEqual(answer, "Updated directory 'update_test'->'updated_dir'")
        self.assertTrue('updated_dir' in self.adapter.get_directory_list('user1')[0])

        answer, code = self.adapter.update_directory('wrong_user', 'update_test', 'updated_dir')
        self.assertEqual(code, 400)
        answer, code = self.adapter.update_directory('user1', 'update_test', 'updated_dir')
        self.assertEqual(code, 400)

    def test_delete_dir(self):
        self.adapter.add_directory('user1', 'updated_dir')
        answer, code = self.adapter.delete_directory('user1', 'updated_dir')
        self.assertTrue(answer.startswith('Deleted directory'))
        self.assertEqual(code, 201)

        answer, code = self.adapter.delete_directory('user1', 'updated_dir')
        self.assertEqual(code, 400)

    def test_get_directory_list(self):
        for i in range(3):
            self.assertEqual(self.adapter.get_directory_list('user' + str(i))[0], ['dir0', 'dir1'])

    def test_add_file(self):
        answer, code = self.adapter.add_file('user0', 'dir1', 'file0', {'content': 123})
        self.assertEqual(answer, "File 'file0' exists")
        self.assertEqual(code, 400)

        answer, code = self.adapter.add_file('user0', 'dir1', 'test_add_file', {'content': 123})
        self.assertEqual(answer, "File 'test_add_file' created")
        self.assertEqual(code, 201)

    def test_get_file(self):
        for i in range(3):
            for j in range(2):
                for k in range(1):
                    self.assertEqual(self.adapter.get_file('user' + str(i), 'dir' + str(j), 'file' + str(k))[0],
                                     {'test_file': str(i + j + k)})

    def test_update_file(self):
        self.adapter.add_file('user0', 'dir1', 'update_file', {'content': 123})
        answer, code = self.adapter.update_file('user0', 'dir1', 'update_file', {'content': 321})
        self.assertEqual(answer, "Updated file 'update_file'")
        self.assertEqual(self.adapter.get_file('user0', 'dir1', 'update_file')[0], {'content': 321})

        answer, code = self.adapter.update_file('wrong_user', 'dir1', 'update_file', {'content': 321})
        self.assertEqual(code, 400)
        answer, code = self.adapter.update_file('user0', 'wrong_dir', 'update_file', {'content': 321})
        self.assertEqual(code, 400)

    def test_delete_file(self):
        self.adapter.add_file('user0', 'dir1', 'update_file', {'content': 123})
        answer, code = self.adapter.delete_file('user0', 'dir1', 'update_file')
        self.assertTrue(answer.startswith('Deleted file'))
        self.assertEqual(code, 201)

        answer, code = self.adapter.delete_file('user0', 'dir1', 'update_file')
        self.assertEqual(code, 400)

    def test_get_file_list(self):
        for i in range(3):
            for j in range(2):
                self.assertEqual(self.adapter.get_file_list('user' + str(i), 'dir' + str(j))[0], ['file0'])


if __name__ == '__main__':
    unittest.main()
