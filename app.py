from flask import Flask, request, jsonify
import MySQLdb

app = Flask(__name__)

# MySQL connection settings
DB_HOST = 'db'  # This will be set in docker-compose
DB_USER = 'root'
DB_PASSWORD = 'example'
DB_NAME = 'todo_db'

# Function to establish a MySQL connection
def get_db_connection():
    return MySQLdb.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)

# Endpoint to add a new todo item
@app.route('/todo', methods=['POST'])
def add_todo():
    data = request.get_json()
    title = data['title']
    description = data.get('description', '')

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO todo (title, description) VALUES (%s, %s)", (title, description))
    connection.commit()

    return jsonify({'status': 'success'}), 201

# Endpoint to get all todo items
@app.route('/todo', methods=['GET'])
def get_todos():
    connection = get_db_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM todo")
    todos = cursor.fetchall()

    return jsonify(todos)

# Endpoint to update a todo item
@app.route('/todo/<int:id>', methods=['PUT'])
def update_todo(id):
    data = request.get_json()
    title = data['title']
    description = data.get('description', '')

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE todo SET title = %s, description = %s WHERE id = %s", (title, description, id))
    connection.commit()

    return jsonify({'status': 'success'})

# Endpoint to delete a todo item
@app.route('/todo/<int:id>', methods=['DELETE'])
def delete_todo(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM todo WHERE id = %s", (id,))
    connection.commit()

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
