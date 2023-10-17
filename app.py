from flask import Flask, request, render_template, url_for
import json

app = Flask(__name__)


def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


database = load_json_file("static/fixtures.json")


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/employees')
def employees():
    page = request.args.get('page', 1, type=int)
    start = (page-1)*20
    end = start + 20
    next_page = url_for('employees', page=page+1)
    return render_template('employees.html', employees=database[start:end], next_page=next_page)


@app.route('/registration')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
