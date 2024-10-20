from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

tasks = [
    {"id": 1, "task": "Cloud-app-dev: Assignment 3", "done": False},
    {"id": 2, "task": "Cloud-app-dev: Assignment 4", "done": False}
]

# def require_api_key(func):
#     def wrapper(*args, **kwargs):
#         api_key = request.headers.get('api-key')
#         if api_key != API_KEY:
#             return jsonify({"error": "Unauthorized: Invalid API Key"}), 401
#         return func(*args, **kwargs)
#     wrapper.__name__ = func.__name__
#     return wrapper

@app.route('/')
def index():
    return "To-DO list by Midterm tsk!"

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    new_task = request.json
    new_task['id'] = len(tasks) + 1
    tasks.append(new_task)
    return jsonify(new_task), 201
    # user_data = {'user_data': new_task}
    # requests.post('https://europe-west1-cloud-app-dev-yessimseit2.cloudfunctions.net/process_user_data', json=user_data)
    # return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        task['task'] = request.json.get('task', task['task'])
        task['done'] = request.json.get('done', task['done'])
        return jsonify(task)
    return jsonify({"error": "Задача не найдена"}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        tasks.remove(task)
        return jsonify({"message": "Задача удалена"})
    return jsonify({"error": "Задача не найдена"}), 404

@app.route('/send_notification', methods=['POST'])
def notify():
    message = request.json.get('message')
    requests.post('https://europe-west1-cloud-app-dev-yessimseit2.cloudfunctions.net/send_notification', json={'message': message})
    return jsonify({"message": "Notification sent."}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
