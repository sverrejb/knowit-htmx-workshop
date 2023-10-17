from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
import os
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = "this is my secret key"


def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


database = load_json_file("static/fixtures.json")


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    year_of_birth = IntegerField('Year of birth', validators=[DataRequired()])
    job = StringField('Job', validators=[DataRequired()])
    submit = SubmitField('Register')


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


@app.route('/registration', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        year_of_birth = form.year_of_birth.data
        job = form.job.data
        database.append(
            {"name": name, "year_of_birth": year_of_birth, "job": job})
        print(database)
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
