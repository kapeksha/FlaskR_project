from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='TodoMVC API',
    description='A simple TodoMVC API',
)

ns = api.namespace('todos', description='TODO operations')

todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')
})


class TodoDAO(object):
    """
    Data Access Object for managing the Todo list.
    """
    def __init__(self):
        """
        Initializes the DAO with a counter and an empty list of todos.
        """
        self.counter = 0
        self.todos = []

    def get(self, id):
        """
        Retrieves a todo by its ID.
        
        :param id: The ID of the todo to retrieve.
        :return: The todo item with the given ID.
        :raises: 404 error if the todo is not found.
        """
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        """
        Creates a new todo item.
        
        :param data: The data for the new todo.
        :return: The created todo item.
        :raises: 400 error if the 'task' field is not provided.
        """
        if 'task' not in data:  # Manual check for the 'task' field
            api.abort(400, "The 'task' field is required.")
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id, data):
        """
        Updates an existing todo item.
        
        :param id: The ID of the todo to update.
        :param data: The updated data for the todo.
        :return: The updated todo item.
        :raises: 400 error if the 'task' field is not provided.
        """
        if 'task' not in data:  # Manual check for the 'task' field
            api.abort(400, "The 'task' field is required.")
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        """
        Deletes a todo item by its ID.
        
        :param id: The ID of the todo to delete.
        :raises: 404 error if the todo is not found.
        """
        todo = self.get(id)
        self.todos.remove(todo)


DAO = TodoDAO()
DAO.create({'task': 'Build an API'})
DAO.create({'task': '?????'})
DAO.create({'task': 'profit!'})


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.todos

    @ns.doc('create_todo')
    @ns.expect(todo, validate=True)  # Ensure this is present
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(todo, validate=True)  # Ensure this is present
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(debug=True)
