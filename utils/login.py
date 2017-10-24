import sqlite3, hashlib
db = sqlite3.connect('database.db')
c = db.cursor()

def get_hashed_password(passw):
    return hashlib.sha256(passw + 'secret key').hexdigest()

def register( user, passw ):
    hashed = get_hashed_password(passw)
    c.execute('INSERT INTO users VALUES ( %s, %s );' % (user, hashed) )

def authenticate(user, passw):
    #temporary, use database later
    hashed = get_hashed_password(passw)
    user_info = c.execute('SELECT user, hashed_pass FROM users WHERE user = %s;' % ( user )).fetchall()
    if user in user_info and passw == user_info[0](1):
        return True
    else:
        return False
