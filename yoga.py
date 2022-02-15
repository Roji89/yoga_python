from werkzeug.exceptions import abort
from typing import Counter
from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from flask import current_app, g
from flask.cli import with_appcontext
import click


app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            "yoga.db",
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def init_db():
    db = get_db()

    with current_app.open_resource('yoga.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

app.teardown_appcontext(close_db)
app.cli.add_command(init_db_command)
app.secret_key ='_5#y2L"192b9bdd22ab9\n\xec]/'    

@app.route('/', methods=('GET', 'POST')) 
def welcome():
    return render_template("index.html")

#-------------Home---------------#
@app.route('/home', methods=('GET', 'POST')) 
def home():
    return render_template("home.html")
#-------------Login---------------#
@app.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone() 
        
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
            
        if user:
            session['username'] = user['username']
            session['password'] = user['password']
            return render_template('index.html')

        flash(error)

    return render_template('./other/login.html')

#-------------Register---------------#
@app.route('/register/', methods=('GET', 'POST'))
def register():
    """Register function"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, '
                + 'password)'
                + 'VALUES (?, ?)',
                (username,generate_password_hash(password)))
            db.commit()
            return render_template('home.html')
            
        flash(error)

    return render_template('./other/register.html')
#-------------Logout---------------#
def logout():
    """deconnection and clear session"""
    session.clear()
    return redirect(url_for('login'))

#-------------Courses---------------#

@app.route('/courses', methods=('GET', 'POST'))
def courses():
    db = get_db()
    courses = db.execute('SELECT * FROM cours;').fetchall()
    return render_template('./other/courses.html', courses=courses)

#-------------get one cours---------------#

@app.route('/cours/<int:cours_id>', methods=('GET', 'POST'))
def cours(cours_id):
    db = get_db()
    cours = db.execute('SELECT * FROM cours WHERE id = ?',(cours_id,)).fetchone()
    if cours is None:
        abort(404, f"cours id {cours_id} doesn't exist.")
    print(cours)
    return render_template('./other/cours.html', cours=cours)

#-------------Delete cours---------------#

@app.route('/delete/<int:cours_id>')
def delete(cours_id):
    db = get_db()
    cours = db.execute('DELETE FROM cours WHERE id = ?',(cours_id,))
    if not cours:
        return redirect('./other/courses.html')
    db.commit()

    return redirect('/')