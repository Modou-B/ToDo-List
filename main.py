import uuid
import os

from flask import Flask, request, jsonify, abort, session
# initialisiere Flask-Server
app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(32)


# create unique id for lists, entries
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = uuid.uuid4()
todo_2_id = uuid.uuid4()
todo_3_id = uuid.uuid4()
todo_4_id = uuid.uuid4()




todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list': todo_list_1_id},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': todo_list_2_id},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list': todo_list_3_id},
    {'id': todo_3_id, 'name': 'Eier', 'description': '', 'list': todo_list_1_id},
]



# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.before_request
def buildSession():
    if not session.permanent:
        session['todo_lists'] = todo_lists
        session['todos'] = todos
        session.permanent = True

# definiere Route für Hauptseite
@app.route('/')
def index():
 # gebe Antwort an aufrufenden Client zurück
 return 'Hello World!'


# /todo-list/{list_id}
@app.route('/todo-list/<list_id>', methods = ['GET'])
def getToDoList(list_id):
    list_item = None
    for i in session:
        if i['id'] == list_id:
            list_item = i
            break
        if not list_item:
            abort(404)
        if request.method == 'GET':
            print('Returning todo list...')
            return jsonify([i for i in todos if i['list'] == list_id])

@app.route('/todo-list/<list_id>', methods = ['DELETE'])
def deleteToDoList(list_id):
    list_item = None
    for i in todo_lists:
        if i['id'] == list_id:
            list_item = i
            break
        if not list_item:
            abort(404)
        if request.method == 'DELETE':
            print('Deleting todo list...')
            todo_lists.remove(list_item)
            return '', 200

@app.route('/todo-list/<list_id>', methods = ['PATCH'])
def updateToDoList(list_id):
    list_item = None
    # for i in todo_lists:
    #     if i['id'] == list_id:
    #         list_item = i
    #         break
    #     if not list_item:
    #         abort(404)
    #     if request.method == 'PATCH':
    #         print('Updating todo list...')
    #         todo_lists.
            


# /todo-list/
@app.route('/todo-list/', methods = ['GET'])
def getAllToDoLists():
    if todo_lists != '':
        return todo_lists
    else :
        abort(404)

@app.route('/todo-list/', methods = ['POST'])
def postNewList():
    todo_list = {'id': uuid.uuid4(), 'name': request.json['name']}
    
    session['todo_lists'].append(todo_list)
    return todo_list
    


# /todo-list/{list_id}/entry
@app.route('/todo-list/<list_id>/entry', methods = ['POST'])
def postNewListEntry(list_id):
    list_item = None
    for i in todo_lists:
        if i['id'] == list_id:
            list_item = i
            break
        if not list_item:
            abort(404)
        if request.method == 'GET':
            print('Returning todo list...')
            return jsonify([i for i in todos if i['list'] == list_id])

# /entry/{entry_id}
@app.route('/entry/<entry_id>', methods = ['PATCH'])
def updateListEntry():
    return request.args 

@app.route('/entry/<entry_id>', methods = ['DELETE'])
def deleteListEntry():
    return request.args 




# @app.route('/post', methods = ['Post'])
# def post():
#     return request.args

if __name__ == '__main__':
 # starte Flask-Server
 app.run(host='0.0.0.0', port=5001)