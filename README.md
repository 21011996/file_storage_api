# File storage API

this is server app, which allows to store users, folders and files using API

### Installing

Before using you will need to install following:
1. MongoDB, execute ```mongod``` before running app
2. Python, ver. 2 or 3
3. Execute ```pip install unittest requests mongoengine flask flask_httpauth```, in order to resolve dependencies.

### Running

To launch server use ```python src/server.py```

To run tests use ```python -m unittest discover src/tests```

### API documentation
Method|URL|JSON attachment|Requires login|Description
:---|:---|:---:|:---:|:---
POST|http://localhost:5000/file_storage/api/v1.0/user/|{'username':username, 'password':password}|[ ]|Add user
DELETE|http://localhost:5000/file_storage/api/v1.0/user/[username]|-|[X]|Deletes specified user
PUT|http://localhost:5000/file_storage/api/v1.0/user/[username]|{'password':new_password}|[X]|Changes password to ```new_password```
GET|http://localhost:5000/file_storage/api/v1.0/user/|-|[ ]|Returns list of users' names
GET|http://localhost:5000/file_storage/api/v1.0/root/|-|[X]|Returns list of user's directories names
POST|http://localhost:5000/file_storage/api/v1.0/root/|{'directory_name':dir_name}|[X]|Add directory
PUT|http://localhost:5000/file_storage/api/v1.0/root/[dir_name]|{'directory_name':new_dir_name}|[X]|Change directory name to ```new_dir_name```
DELETE|http://localhost:5000/file_storage/api/v1.0/root/[dir_name]|-|[X]|Delete directory
GET|http://localhost:5000/file_storage/api/v1.0/root/[dir_name]|-|[X]|Returns list of file names in this directory
POST|http://localhost:5000/file_storage/api/v1.0/root/[dir_name]|{'filename':file_name,'filecontent':filecontent}|[X]|Add file to specified directory
PUT|http://localhost:5000/file_storage/api/v1.0/root/[dir_name]/[file_name]|{'filecontent':filecontent}|[X]|Update file with ```filecontent```
DELETE|http://localhost:5000/file_storage/api/v1.0/root/[dir_name]/[file_name]|-|[X]|Delete file
GET|http://localhost:5000/file_storage/api/v1.0/root/[dir_name]/[file_name]|-|[X]|Returns file content 