import sqlite3, hashlib
f = 'database.db'

def get_hashed_password(passw):
    return hashlib.sha256(passw + 'secret key').hexdigest()

def register( user, passw ):
    hashed = get_hashed_password(passw)
    db = sqlite3.connect(f)
    user_info = db.cursor().execute('SELECT username FROM users WHERE username = "%s";' % ( user )).fetchall()
    if len(user_info) != 0:
        return False
    db.cursor().execute('INSERT INTO users VALUES ( "%s", "%s", "[]" );' % (user, hashed) )
    db.commit()
    db.close()
    return True

def authenticate(user, passw):
    hashed = get_hashed_password(passw)
    db = sqlite3.connect(f)
    user_info = db.cursor().execute('SELECT username, hashed_pass FROM users WHERE username = "%s";' % ( user )).fetchall()
    db.close()
    if len(user_info) != 0 and hashed == user_info[0][1]:
        return True
    else:
        return False
