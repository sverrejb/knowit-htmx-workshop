from flask import Flask, render_template
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
    return render_template('employees.html', employees = database)

@app.route('/registration')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
