import sqlite3

m = 'database.db'

## Returns list of id's of all edited stories
def view_edit_history(user):
    db = sqlite3.connect(m)
    c = db.cursor()
    edit_history = c.execute('SELECT edited_stories FROM users WHERE username="%s"'%(user)).fetchall()
    history = eval(edit_history[0][0])
    db.commit()
    db.close()
    return history

## Updates edit history of user to add recently edited story
def update_edit_history(user, id_num):
    db = sqlite3.connect(m)
    c = db.cursor()

    history = view_edit_history(user)
    history.append(id_num)
    updated_history = repr(history)
    c.execute('UPDATE users SET edited_stories = "%s" WHERE username="%s"'%(updated_history, user))
    
    db.commit()
    db.close()

## Create a new story and update edit history of user
def create_story(user, id_num, title, content):
    db = sqlite3.connect(m)
    c = db.cursor()

    update_edit_history(user, id_num)
    
    c.execute('INSERT INTO stories VALUES(%d, "%s", "%s", "%s")'%(id_num, title, content, content))
    db.commit()
    db.close()

## Add new content to a new story and update edit history of user
## Return False if user has already edited this story, True otherwise
def edit_story(user, id_num, new_cont):
    db = sqlite3.connect(m)
    c = db.cursor()

    history = view_edit_history(user)
    if id_num in history:
        return False
    
    update_edit_history(user, id_num)
    
    content = c.execute('SELECT CONTENT FROM stories WHERE id=%d'%(id_num)).fetchall()
    updated_cont = content[0][0]
    updated_cont += '\n' + new_cont
    c.execute('UPDATE stories SET CONTENT = "%s" WHERE id=%d'%(updated_cont, id_num))
    c.execute('UPDATE stories SET revision = "%s" WHERE id=%d'%(new_cont, id_num))
    db.commit()
    db.close()
        
    return True

def get_revision(id_num):
    db = sqlite3.connect(m)
    c = db.cursor()
    return c.execute('SELECT revision FROM stories WHERE id=%s' % (id_num)).fetchall()[0][0]

def get_content(id_num):
    db = sqlite3.connect(m)
    c = db.cursor()
    return c.execute('SELECT content FROM stories WHERE id=%s' % (id_num)).fetchall()[0][0]


if __name__ == '__main__':
    db = sqlite3.connect('../database.db')
    c=db.cursor()

    create_story("user2", 0, "oy", "ayyyyy")
    create_story("user2", 2, "ummmm", "i dunno")
    create_story("user2", 1, "yep", "same")
    create_story("user", 4, "testing", "123 123")
    create_story("user2", 5, "ughhh", "are you good")

    edit_story("user" , 1, "muy interesante")
    edit_story("user" , 2, "pulsh")
    edit_story("user2" , 5, "~~~~~~jnkhbjh~~~~~~~~fdvdfvdfv")
