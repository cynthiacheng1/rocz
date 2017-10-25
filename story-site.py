from flask import Flask, render_template, request, session, redirect, url_for, flash
import os, sqlite3

users = { "user" : "password", "user2" : "password" } # replace with database

SUCCESS = 1
BAD_LOGIN = -1

story_site = Flask(__name__)
story_site.secret_key = os.urandom(64)

def authenticate(user, passw):
    #temporary, use database later
    if user in users and passw == users[user]:
        return  SUCCESS
    else:
        return BAD_LOGIN

@story_site.route('/')
def root():
    if 'user' not in session:
        return render_template('login.html', title="Login")
    else:
        return redirect( url_for('welcome') )

@story_site.route('/auth', methods=['POST'])
def auth():
    user = request.form['user']
    passw = request.form['pw']
    
    result = authenticate(user, passw)

    if result == SUCCESS:
        session['user'] = user
        flash('Successful Login!')
        return redirect( url_for('welcome') )
    elif result == BAD_LOGIN:
        flash("Invalid username or password. Try Again.")
    return redirect(url_for('root'))

@story_site.route('/welcome')
def welcome():
    if 'user' not in session:
        return redirect( url_for('root') )
    else:
        return render_template('main.html', user=session['user'], title='Welcome')

@story_site.route('/logout', methods=['POST'])
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect( url_for('root') )
                               

if __name__ == '__main__':
    db = "database.db" #Starts as string becomes db object
    tables_exist = os.path.isfile(db)
    db = sqlite3.connect(db)
    c = db.cursor()
    if not tables_exist:
        c.execute("CREATE TABLE users (username TEXT PRIMARY KEY, hashed_pass TEXT, edited_stories TEXT);")
        c.execute("CREATE TABLE stories (id INTEGER PRIMARY KEY, title TEXT, CONTENT TEXT, revision TEXT);")

    story_site.debug = True
    story_site.run()

    db.commit()
    db.close()
    
