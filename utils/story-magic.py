import sqlite3

m = '../database.db'

## Returns list of id's of all edited stories
def view_edit_history(user):
    db = sqlite3.connect(m)
    c = db.cursor()
    edit_history = c.execute('SELECT edited_stories FROM users WHERE username="%s"'%(user))
    history = []
    for story_string in edit_history:
        history = eval(story_string[0])
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
def createStory(user, id_num, title, content):
    db = sqlite3.connect(m)
    c = db.cursor()

    update_edit_history(user, id_num)
    
    c.execute('INSERT INTO stories VALUES(%d, "%s", "%s", "%s")'%(id_num, title, content, content))
    db.commit()
    db.close()

## Add new content to a new story and update edit history of user
## Return False if user has already edited this story, True otherwise
def editStory(user, id_num, new_cont):
    db = sqlite3.connect(m)
    c = db.cursor()

    history = view_edit_history(user)
    if id_num in history:
        return False
    
    update_edit_history(user, id_num)
    
    content = c.execute('SELECT CONTENT FROM stories WHERE id=%d'%(id_num))
    updated_cont = ''
    for old_content in content:
        updated_cont = old_content[0]
        updated_cont += '\n' + new_cont
    c.execute('UPDATE stories SET CONTENT = "%s" WHERE id=%d'%(updated_cont, id_num))
    c.execute('UPDATE stories SET revision = "%s" WHERE id=%d'%(new_cont, id_num))
    db.commit()
    db.close()
        
    return True



if __name__ == '__main__':
    db = sqlite3.connect('../database.db')
    c=db.cursor()

    createStory("user2", 0, "oy", "ayyyyy")
    createStory("user2", 2, "ummmm", "i dunno")
    createStory("user2", 1, "yep", "same")
    createStory("user", 4, "testing", "123 123")
    createStory("user2", 5, "ughhh", "are you good")

    editStory("user" , 1, "muy interesante")
    editStory("user" , 2, "pulsh")
    editStory("user2" , 5, "~~~~~~jnkhbjh~~~~~~~~fdvdfvdfv")
