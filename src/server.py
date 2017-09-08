from flask import Flask, jsonify, make_response, request, abort
from flask_httpauth import HTTPBasicAuth

from src.constants import Constants
from src.db_adapter import MongoDBAdapter

app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()
adapter = MongoDBAdapter(Constants.db_name)


def mk_answer(content, name='response'):
    return jsonify({name: content})


@auth.get_password
def get_password(username):
    return adapter.get_password(username)


@auth.error_handler
def unauthorized():
    return make_response(mk_answer('Unauthorized access', 'error'), 403)


@app.errorhandler(400)
def not_found():
    return make_response(mk_answer('Bad request', 'error'), 400)


@app.errorhandler(404)
def not_found():
    return make_response(mk_answer('Not found', 'error'), 404)


@app.route(Constants.api_prefix + 'user', methods=['POST'])
def post_user():
    if not request.json or ('username' not in request.json) or ('password' not in request.json):
        abort(400)
    answer, code = adapter.add_user(request.json['username'], request.json['password'])
    return mk_answer(answer), code


@app.route(Constants.api_prefix + 'user/<string:user_name>', methods=['DELETE'])
@auth.login_required
def delete_user(user_name):
    if request.authorization.username == user_name:
        answer, code = adapter.delete_user(user_name)
        return mk_answer(answer), code
    else:
        abort(403)


@app.route(Constants.api_prefix + 'user/<string:user_name>', methods=['PUT'])
@auth.login_required
def update_user(user_name):
    if request.authorization.username == user_name and request.json and 'password' in request.json:
        answer, code = adapter.update_user(user_name, request.json['password'])
        return mk_answer(answer), code
    else:
        abort(403)


@app.route(Constants.api_prefix + 'user', methods=['GET'])
def get_users():
    answer, code = adapter.get_username_list()
    return mk_answer(answer), code


@app.route(Constants.api_prefix + 'root', methods=['GET'])
@auth.login_required
def get_directories():
    answer, code = adapter.get_directory_list(request.authorization.username)
    return mk_answer(answer), code


@app.route(Constants.api_prefix + 'root', methods=['POST'])
@auth.login_required
def add_directory():
    if request.json and 'directory_name' in request.json:
        answer, code = adapter.add_directory(request.authorization.username, request.json['directory_name'])
        return mk_answer(answer), code
    else:
        abort(400)


@app.route(Constants.api_prefix + 'root/<string:dir_name>', methods=['PUT'])
@auth.login_required
def update_directory(dir_name):
    if request.json and 'directory_name' in request.json:
        answer, code = adapter.update_directory(request.authorization.username, dir_name,
                                                request.json['directory_name'])
        return mk_answer(answer), code
    else:
        abort(400)


@app.route(Constants.api_prefix + 'root/<string:dir_name>', methods=['DELETE'])
@auth.login_required
def delete_directory(dir_name):
    answer, code = adapter.delete_directory(request.authorization.username, dir_name)
    return mk_answer(answer), code


@app.route(Constants.api_prefix + 'root/<string:dir_name>', methods=['GET'])
@auth.login_required
def get_files_in_dir(dir_name):
    answer, code = adapter.get_file_list(request.authorization.username, dir_name)
    return mk_answer(answer), code


@app.route(Constants.api_prefix + 'root/<string:dir_name>', methods=['POST'])
@auth.login_required
def add_file(dir_name):
    if request.json and 'filename' in request.json and 'filecontent' in request.json:
        answer, code = adapter.add_file(request.authorization.username, dir_name, request.json['filename'],
                                        request.json['filecontent'])
        return mk_answer(answer), code
    else:
        abort(400)


@app.route(Constants.api_prefix + 'root/<string:dir_name>/<string:file_name>', methods=['PUT'])
@auth.login_required
def update_file(dir_name, file_name):
    if request.json and 'filecontent' in request.json:
        answer, code = adapter.update_file(request.authorization.username, dir_name, file_name,
                                           request.json['filecontent'])
        return mk_answer(answer), code
    else:
        abort(400)


@app.route(Constants.api_prefix + 'root/<string:dir_name>/<string:file_name>', methods=['DELETE'])
@auth.login_required
def delete_file(dir_name, file_name):
    answer, code = adapter.delete_file(request.authorization.username, dir_name, file_name)
    return mk_answer(answer), code


@app.route(Constants.api_prefix + 'root/<string:dir_name>/<string:file_name>', methods=['GET'])
@auth.login_required
def get_file(dir_name, file_name):
    answer, code = adapter.get_file(request.authorization.username, dir_name, file_name)
    return mk_answer(answer), code


if __name__ == '__main__':
    app.run(debug=True)
