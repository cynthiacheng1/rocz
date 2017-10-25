import sqlite3

db = sqlite3.connect('database.db')
c = db.cursor()

def getStories(n):
    for each in c.execute("SELECT * FROM stories"):
        print each



if __name__ == '__main__':
    getStories(5)
