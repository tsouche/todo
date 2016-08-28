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
        result.append([task['_id'], task['task']])
    output = template('make_table', rows=result)
    return output
    
@route('/new', method='GET')
def new_item():
    # connects to the DB
    todoDB = MongoClient().todoDB
    todoColl = todoDB.todo
    # collect the new task from the web: we cover here for the case where the 
    # remote client will not proactively send the 'task' information:
    #   - either the remote client sends 'task' via a GET method
    #   - or we issue a form asking for the client to fill it in and 'save' it:
    #     the form will then send the 'task' data via a GET method.
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

@route('/edit/<task_id>', method='GET')
def edit_item(task_id):
    # connects to the DB
    todoDB = MongoClient().todoDB
    todoColl = todoDB.todo
    # converts the task_id into a valid ObjectId, to be used with MongoDB
    task_id = ObjectId(task_id)
    # collect the id of the task to be edited, and the data to be edited
    if request.GET.save:
        task = request.GET.task.strip()
        status = request.GET.task.strip()
        if status == "open":
            status = 1
        else:
            status = 0     
        # Now, it connects to the DB and updates the task
        todoColl.find_one_and_update({'_id': task_id},
            {'$set': {'task': task, 'status': status}})
        msg = "<p>The task " + str(task_id) + " was successfully updated.</p>"
        return msg
    else:
        # the form will then send the 'task' data via a GET method.
        tt = todoColl.find_one({'_id': task_id})
        return template('edit_task.tpl', old = tt['task'], id = tt['_id'])

load_data()
# starts the server
debug(True)
run(reloader=True)
    