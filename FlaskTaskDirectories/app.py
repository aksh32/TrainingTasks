import os

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename, redirect

app = Flask(__name__)
app.secret_key = 'secret key'


@app.route('/')
def index():
    directories = list_files('/home')
    return render_template('/searchDir', direct=directories)


@app.route('/searchDir', methods=['GET'])
def search_directories():
    search_dir = request.form.get('txt1')
    dir_info = list_files(search_dir)

    return jsonify(directory_info=dir_info)


def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        dir_content = []
        for dir in dirs:
            go_inside = os.path.join(startpath, dir)
            if list_files(go_inside):
                dir_content.append(list_files(go_inside))
            else:
                pass
        files_lst = []
        for f in files:
            files_lst.append(f)
        return {'name': os.path.basename(root), 'files': files_lst, 'dirs': dir_content}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
