import sqlite3

## Returns a list of n tuples, each tuple being a story entry in the db
def getStories(db, n):
    c = db.cursor()
    L = []
    for each in c.execute("SELECT * FROM stories"):
        L.append(each)
    L = L[len(L)-n:]
    return L[::-1]


if __name__ == '__main__':
    db = sqlite3.connect('../database.db')
    c=db.cursor()
    for i in xrange(10):
        c.execute("INSERT INTO stories VALUES (%d, \"%s\", \"%s\", \"%s\");"%(i, 'no title', 'test', 'test'))
    print getStories(db, 5)
    print getStories(db, 0)
    print getStories(db, -2)
    print getStories(db, 10)
    
