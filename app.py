from flask import Flask, render_template
import time

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/members')
def members():
    return render_template('members.html')

@app.route('/registration')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
