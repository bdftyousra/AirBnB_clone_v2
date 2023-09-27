#!/usr/bin/python3
"""starts a Flask web application
"""
from flask import Flask, render_template


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello():
    """prints "Hello HBNB!"
    """
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    """prints “HBNB”
    """
    return 'HBNB'


@app.route('/c/<text>')
def c_is_fun(text):
    """prints "C" followed by the value of the text variable
    """
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python')
@app.route('/python/<text>')
def python_is_magic(text='is cool'):
    """prints “Python ”, followed by the value of the text
    """
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>')
def number(n):
    """prints "n is a number” only if n is an integer
    """
    return '{:d} is a number'.format(n)


@app.route('/number_template/<int:n>')
def number_template(n):
    """prints a HTML page only if n is an integer
    """
    return render_template("5-number.html", n=n)


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
