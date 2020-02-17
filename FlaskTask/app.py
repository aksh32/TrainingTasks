import csv
import json
import os

from flask import Flask, request, render_template, flash, jsonify, session
from werkzeug.utils import secure_filename, redirect

app = Flask(__name__)
app.config['upload_folder'] = '/home/akshay/TrainingTasks/TrainingTasks/FlaskTask/InputFiles'
app.config['allowed_file_extensions'] = ['JSON']
app.secret_key = 'secret key'


@app.route('/')
def get_json_file():
    return render_template('index.html')


def allowed_files(filename):
    if not '.' in filename:
        return False

    extension = filename.rsplit('.', 1)[1]

    if extension.upper() in app.config['allowed_file_extensions']:
        return True
    else:
        return False


@app.route('/uploader', methods=['GET', 'POST'])
def upload_json_file():
    response = {}

    if request.method == 'POST':
        if request.files:
            file = request.files['file']
            if file.filename is None:
                flash('No file selected for uploading')
                response['message'] = 'No file selected for uploading'
            if allowed_files(file.filename):
                file.save(os.path.join(app.config['upload_folder'], secure_filename(file.filename)))
                json_file_path = './InputFiles/data.json'
                convert_to_csv(json_file_path)
                flash('file successfully uploaded')
                response['message'] = 'file successfully uploaded'
            else:
                flash('file extension not allowed')
                response['message'] = 'file extension not allowed'
    return jsonify(response)


def convert_to_csv(inputpath):
    try:
        with open(inputpath, 'r') as file:
            json_output = json.load(file)
        with open('./OutputFile/outputCsv.csv', 'w+') as csv_output:
            print('in file open')
            wtr = csv.writer(csv_output, delimiter=',')
            for key, value in json_output.items():
                count = 0
                if len(value) >= 2:
                    for item in value:
                        count += 1
                        wtr.writerow([key, item, count])
                elif type(value) == str:
                    wtr.writerow([key, value, count])
                else:
                    wtr.writerow([key, value, 1])
        flash('file converted successfully!!!!')
        return redirect('/')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    session.clear()
