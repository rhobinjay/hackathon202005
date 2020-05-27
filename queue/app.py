from flask import Flask
from flask_restplus import Resource, Api, fields
import json
import pdb

app = Flask(__name__)
api = Api(app, version='1.0', title='Queue Service API',
          description='A simple queueing service.')

ns = api.namespace('todos', description='TODO operations')

todo = api.model('Todo', {
    'taskId': fields.Integer(readonly=True, description='The task unique identifier'),
    'command': fields.String(required=True, description='The task details')
})


class TodoData:
    def __init__(self):
        self.count = 0
        self.todos = []

    def add_todo(self, todo):
        self.count += 1
        todo['taskId'] = self.count
        self.todos.append(todo)


tododata = TodoData()
tododata.add_todo({'command': "echo 'task 1'"})
tododata.add_todo({'command': "echo 'task 2'"})
tododata.add_todo({'command': "echo 'task 3'"})


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return tododata.todos

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        try:
            todo = json.loads(api.payload)
        except Exception:
            todo = api.payload
        tododata.add_todo(todo)
        return tododata.todos, 201


@ns.route('/request')
class TodoRequest(Resource):
    def get(self):
        '''Get a task from Todo List'''
        try:
            return tododata.todos.pop(0)
        except IndexError:
            return {}
        except Exception:
            return {'message': 'Something is wrong.'}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5002')
