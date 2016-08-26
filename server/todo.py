'''
Created on Aug 26, 2016

@author: thierry
'''

from bson.objectid import ObjectId
from pymongo import MongoClient
from bottle import route, request, template, run, debug

"""
Links with the MongoDB server and connects to the 'todoDB' database.
Then links with the 'todo' collection via 'todoColl'
    todoDB = MongoClient().todoDB
    todoColl = todoDB.todo
Every document in the 'todo' collection should look like:
        { '_id': PbjectId, 'task': string, 'status': 1 or 0 }
"""


def load_data():
    # connects to the DB
    todoDB = MongoClient().todoDB
    todoColl = todoDB.todo
    # load some basic data
    todoColl.drop()
    todoColl.insert_one({'_id': ObjectId('57c0b1bb124e9b387d9ebe14'), 'task': "aller manger", 'status': 1})
    todoColl.insert_one({'_id': ObjectId('57c0b1bb124e9b387d9ebe15'), 'task': "aller dormir", 'status': 1})
    todoColl.insert_one({'_id': ObjectId('57c0b257124e9b38f24e014f'), 'task': "apprendre Pyhton", 'status': 0})

@route('/todo')        
def todo_list():
    """
    This method returns the list of all active tasks.
    """
    # connects to the DB
    todoDB = MongoClient().todoDB
    todoColl = todoDB.todo
    # initiates the players collections
    result = []
    for task in todoColl.find({'status': 1}):
        result.append(["X", task['task']])
    output = template('make_table', rows=result)
    return output
    
@route('/new', method='GET')
def new_item():
    # connects to the DB
    todoDB = MongoClient().todoDB
    todoColl = todoDB.todo
    # collect the new task from the web
    if request.GET.get('save','').strip():
        # this  corresponds to the case when the client proactively pushes data 
        # to the server via a GET method.
        task = request.GET.get('task', '').strip()
        # load the new task in the DB
        task_id = todoColl.insert_one({'task': task, 'status': 1}).inserted_id
        msg = "<p>The new task was inserted into the database, the ID is "
        msg += str(task_id) + ".<p>"
        return msg
    else:
        return template('new_task.tpl')

load_data()
# starts the server
debug(True)
run(reloader=True)
    