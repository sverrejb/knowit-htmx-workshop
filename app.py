from flask import Flask, redirect, request, render_template, render_template_string, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
import json
import random

app = Flask(__name__)

app.config['SECRET_KEY'] = "this is my secret key"
PAGE_SIZE = 20


def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


database = load_json_file("static/fixtures.json")
quotes = [line.strip() for line in open('static/quotes.txt', 'r')]


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    year_of_birth = IntegerField('Year of birth', validators=[DataRequired()])
    job = StringField('Job', validators=[DataRequired()])
    submit = SubmitField('Register')


class EditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    job = StringField('Job', validators=[DataRequired()])
    submit = SubmitField('Save')


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/quote')
def quote():
    quote = random.choice(quotes)
    return render_template('quote.html', quote=quote)


@app.route('/employees', methods=['POST'])
def register_employee():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        year_of_birth = form.year_of_birth.data
        job = form.job.data
        database.insert(0,
                        {"id": random.randint(len(database), 9999), "name": name, "year_of_birth": year_of_birth, "job": job})
    return render_template('employee_registred.html', name=name)


@app.route('/employees')
def get_employees():
    employees = database
    search_query = request.args.get('q', type=str)
    if search_query:
        employees = [employee for employee in employees if search_query.lower() in employee['name'].lower()]

    page = request.args.get('page', 1, type=int)
    start = (page-1)*PAGE_SIZE
    end = start + PAGE_SIZE

    next_page = url_for('get_employees', q=search_query, page=page+1)
    if end >= len(employees):
        next_page = None

    return render_template('employees.html', employees=employees[start:end], query=search_query, next_page=next_page, number_of_employees=len(employees))


@app.route('/employees/<int:id>')
def get_employee(id):
    form = EditForm()
    for employee in database:
        if employee['id'] == id:
            return render_template('employee.html', employee=employee, form=form)
    return render_template_string('PageNotFound {{ errorCode }}', errorCode='404'), 404


@app.route('/employees/<int:id>', methods=["POST"])
def update_employee(id):
    form = EditForm()

    if form.validate_on_submit():
        for employee in database:
            if employee['id'] == id:
                employee["name"] = form.name.data
                employee["job"] = form.job.data
                return redirect(url_for("get_employees"))

    return render_template_string('PageNotFound {{ errorCode }}', errorCode='404'), 404


@app.route('/employees/<int:id>', methods=["DELETE"])
def delete_employee(id):
    # TODO: refactor this horrible mess
    employees = database
    search_query = request.args.get('q', type=str)
    if search_query:
        employees = [employee for employee in employees if search_query.lower(
        ) in employee['name'].lower()]

    page = request.args.get('page', 1, type=int)
    start = (page-1)*PAGE_SIZE
    end = start + PAGE_SIZE

    next_page = url_for('get_employees', q=search_query, page=page+1)
    if end >= len(employees):
        next_page = None

    for employee in database:
        if employee["id"] == id:
            database.remove(employee)
            return render_template('employees.html', employees=employees[start:end], query=search_query, next_page=next_page, number_of_employees=len(employees))
    return ('', 500)


@app.route('/registration', methods=['GET'])
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
