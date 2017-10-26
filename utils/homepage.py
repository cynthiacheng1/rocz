import sqlite3

data = 'database.db'

## Returns a list of tuples, each tuple being a story entry in the db
def get_stories():
    db = sqlite3.connect(data)
    c = db.cursor()
    L = c.execute("SELECT * FROM stories;").fetchall()
    return L[::-1]

## Helper function
def find_edits(user):
    db = sqlite3.connect(data)
    c = db.cursor()
    return eval(c.execute('SELECT edited_stories FROM users WHERE username="%s";'%(user)).fetchall()[0][0])

def get_edited_stories(user):
    db = sqlite3.connect(data)
    c = db.cursor()
    edited = find_edits(user)
    L = c.execute("SELECT * FROM stories;").fetchall()
    for each in L:
        if not each[0] in edited:
            L.remove(each)
    return L[::-1]

def get_unedited_stories(user):
    db = sqlite3.connect(data)
    c = db.cursor()
    edited = find_edits(user)
    L = c.execute("SELECT * FROM stories;").fetchall()
    for each in L:
        if each[0] in edited:
            L.remove(each)
    return L[::-1]


if __name__ == '__main__':
    data = '../database.db'
    f = sqlite3.connect(data)
    c = f.cursor()
    for i in xrange(10, 20):
        c.execute("INSERT INTO stories VALUES (%d, \"%s\", \"%s\", \"%s\");"%(i, 'no title', 'test', 'test'))
    print get_stories()
    print ''+''%()*4**8 #Print an empty line
    print find_edits('user')
    print get_edited_stories('user')
    print get_unedited_stories('user')
    
