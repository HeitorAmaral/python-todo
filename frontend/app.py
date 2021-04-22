import requests
from flask import Flask, render_template, request, jsonify, url_for, redirect

app = Flask(__name__)
api_url = "http://localhost:5000/api/v1/task"


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    """
    Returns the initial HTML page of application.

    :return: Renders the index.html file.
    :rtype: html
    """
    app.logger.info("Executing at TaskController - index()")
    return render_template('index.html')


@app.route('/find-all', methods=['GET'])
def find_all():
    """
    Method that query all the registers in the database and returns all
    the data.

    :return: Renders the page with the list of all Tasks stored in the
    database.
    :rtype: html
    """
    response = requests.get(api_url)
    tasks = []
    if response.status_code == 200:
        tasks = response.json()
    return render_template('list.html', tasks=tasks)


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    """
    Method that creates a new Task, or update it if the Description
    already exists and returns or redirect the HTML page.

    :return: If a POST HTTP request called it, and no validation error
    happens, returns the page with all registers. If not, renders the
    page of insert a new Task.
    :rtype: html
    """
    if request.method == 'POST':
        description = request.form.get('description')
        status = request.form.get('status')

        if status is None or status == 'False':
            status = False
        elif status == 'on' or status == 'True':
            status = True

        if description:
            requests.post(api_url,
                          json={"description": description,
                                "status": status})
        else:
            return render_template('insert.html',
                                   message='É necessário preencher a Descrição'
                                           ' da Tarefa. Preencha o campo'
                                           ' Descrição.')
        return redirect(url_for('find_all'))
    else:
        return render_template('insert.html')


@app.route('/delete-by-id/<int:task_id>', methods=['GET', 'DELETE'])
def delete_by_id(task_id):
    """
    Method that deletes a register of Task by identifier, and returns a
    HTML page with the list of all Tasks.

    :param task_id: Identifier of the Task.
    :type task_id: int
    :return: HTML page with the list all Tasks.
    :rtype: html
    """
    response = requests.delete(api_url + "/" + str(task_id))
    return redirect(url_for('find_all'))


@app.route('/update-by-id/<int:task_id>', methods=['GET', 'POST', 'PUT'])
def update_by_id(task_id):
    """
    Method that updates a Task by Identifier and returns or redirect
    the HTML page.

    :param task_id: Identifier of the Task.
    :type task_id: int
    :return: If a POST or PUT HTTP method request called the method,
    and the process is executed with success, renders the HTML page
    with the list of all Tasks. If not, returns the HTML page with
    the form to update, with validation messages or not.
    :rtype: html
    """
    task = requests.get(api_url + "/" + str(task_id))
    description = request.form.get('description')

    if request.method == 'POST' or request.method == 'PUT':
        if description:
            requests.put(api_url + "/" + str(task_id),
                         json={"description": description,
                               "status": task.json()["status"]})
        else:
            return render_template('update.html', task=task,
                                   message='É necessário preencher a'
                                           ' Descrição da Tarefa.'
                                           ' Preencha o campo'
                                           ' Descrição.')
        return redirect(url_for('find_all'))
    return render_template('update.html', task=task.json())


@app.route('/change-status-by-id/<int:task_id>', methods=['GET', 'PUT'])
def change_status_by_id(task_id):
    """
    Method that change the status of a Task by Identifier, and returns
    a HTML page with the list of all Tasks.

    :param task_id: Identifier of the Task
    :type task_id: int
    :return: Renders the HTML page with the list of all Tasks.
    :rtype: html
    """
    task = requests.get(api_url + "/" + str(task_id))
    json_task = task.json()
    print(json_task)
    task_id = json_task['_id']
    task_status = json_task['status']

    if task_status:
        task_status = False
    else:
        task_status = True

    requests.put(api_url + "/" + str(task_id),
                 json={"description": json_task["description"],
                       "status": task_status})

    return redirect(url_for('find_all'))


if __name__ == '__main__':
    app.run()
