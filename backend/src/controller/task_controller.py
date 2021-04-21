"""
Controller/View methods and operations
"""
from flask import jsonify, request
from datetime import datetime
from src import app
from src.repository import task_repository

repository = task_repository.TaskRepository(app)


class Task:
    def __init__(self, dict_object, task_id, description, status):
        if dict_object is None:
            self._id = task_id
            self.description = description.strip()
            self.status = status
        else:
            self._id = dict_object['_id']
            self.description = dict_object['description']
            self.status = dict_object['status']

    def serialize(self):
        return {"_id": self._id,
                "description": self.description,
                "status": self.status}


@app.route('/', methods=['GET'])
def ping():
    return jsonify({'message': 'The backend is working!'}), 200


@app.route('/api/v1/task', methods=['GET'])
def find_all():
    tasks = repository.find_all()
    return jsonify(tasks), 200


@app.route('/api/v1/task/<int:task_id>', methods=['GET'])
def find_by_id(task_id):
    query_result = repository.find_by_id(task_id=task_id)
    if query_result is None:
        return generate_exception(404, "Objeto não encontrado",
                                  "Não foi encontrado nenhum objeto com o "
                                  "Id = " + str(task_id),
                                  request.base_url)
    return jsonify(query_result), 200


@app.route('/api/v1/task', methods=['POST'])
def insert():
    request_body = validate_request_body(request_object=request)
    if request.get_json() != request_body:
        return request_body

    task = Task(None, repository.find_available_id(),
                request_body['description'],
                request_body['status'])

    task_serialized = task.serialize()
    repository.insert(task_serialized=task_serialized)
    return task_serialized, 201


@app.route('/api/v1/task/<int:task_id>', methods=['PUT'])
def update_by_id(task_id):
    query_result = repository.find_by_id(task_id=task_id)
    if query_result is None:
        return generate_exception(404, "Objeto não encontrado",
                                  "Não foi encontrado nenhum objeto com o "
                                  "Id = " + str(task_id),
                                  request.base_url)
    task = Task(query_result, None,  None, None)
    request_body = validate_request_body(request_object=request)
    if request.get_json() != request_body:
        return request_body

    task.description = request_body['description']
    task.status = request_body['status']

    task_serialized = task.serialize()
    repository.update_by_id(task_id=task_id, task_serialized=task_serialized)
    return task_serialized, 200


@app.route('/api/v1/task/<int:task_id>', methods=['DELETE'])
def delete_by_id(task_id):
    task = repository.find_by_id(task_id=task_id)
    if task is None:
        return generate_exception(404, "Objeto não encontrado",
                                  "Não foi encontrado nenhum objeto com o "
                                  "Id = " + str(task_id),
                                  request.base_url)
    query_result = repository.delete_by_id(task_id=task_id)
    if query_result is not None and query_result.acknowledged:
        return task, 200
    else:
        return generate_exception(500, "Erro genérico",
                                  "Ocorreu um erro durante a operacão",
                                  request.base_url)


def validate_request_body(request_object):
    request_body = request_object.get_json()

    errors = []
    if "description" not in request_body:
        errors.append({"property": "description",
                       "message": "Propriedade obrigatória não informada."})
    if "status" not in request_body:
        errors.append({"property": "status",
                       "message": "Propriedade obrigatória não informada."})

    if len(errors) > 0:
        return generate_exception(422, "Erro de validacão do corpo da "
                                       "requisicão",
                                  errors,
                                  request_object.base_url)
    return request_body


def generate_exception(status, error, message, path):
    response = jsonify({"timestamp": datetime.now().timestamp(),
                        "status": status,
                        "error": error,
                        "message": message,
                        "path": path})
    response.status_code = status
    return response
