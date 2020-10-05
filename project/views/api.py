

# routes
@app.route('/')
def index():
    data = dict()
    todolists = TodoList.query.all()
    if len(todolists) > 0:
        data['todolists'] = todolists
        todolist = todolists[0]
        data['todolist'] = todolist
        data['todos'] = Todo.query.filter(Todo.list_id == todolist.id)
    return render_template('index.html', data=data)


@app.route('/api/todolist', methods=['POST'])
def get_todolist():
    error = False
    body = {}
    list_id = request.get_json().get('id')
    todolist = TodoList.query.get(list_id)

    print(f'sending todolist: {todolist}')
    print(f'todolist.dictionary: {todolist.dictionary}')

    if todolist:
        body['todolist'] = todolist.dictionary
    else:
        error = True

    if not error:
        return jsonify(body)
    else:
        return abort(400)


@app.route('/api/todolist/create', methods=['POST'])
def create_todolist():
    error = False
    body = {}
    try:
        name = request.get_json().get('name')
        if name:
            new_todolist = TodoList(name=name)
            db.session.add(new_todolist)
            db.session.commit()
            body = new_todolist.dictionary
        else:
            error = True
    except:
        error = True
        db.session.rollback()
        print(sys.exec_info())
    finally:
        db.session.close()
    if not error:
        return jsonify(body)
    else:
        return abort(400)


@app.route('/api/todo/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json().get('description')
        list_id = request.get_json().get('list_id')
        if description and list_id:
            new_todo = Todo(description=description, list_id=list_id)
            db.session.add(new_todo)
            db.session.commit()
            body['description'] = new_todo.description
            body['id'] = new_todo.id
            body['completed'] = new_todo.completed
        else:
            error = True
    except:
        error = True
        db.session.rollback()
        print(sys.exec_info())
    finally:
        db.session.close()
    if not error:
        return jsonify(body)
    else:
        return abort(400)


@app.route('/api/todo/delete', methods=['POST'])
def delete_todo():
    error = False
    body = {}
    try:
        _id = request.get_json().get('id')
        if _id:
            todo = Todo.query.get(_id)
            db.session.delete(todo)
            db.session.commit()
            body['id'] = todo.id
            body['success'] = True
        else:
            error = True
    except:
        error = True
        db.session.rollback()
        print(sys.exec_info())
    finally:
        db.session.close()
    if not error:
        return jsonify(body)
    else:
        return abort(400)


@app.route('/api/todo/completed', methods=['POST'])
def set_todo_completed():
    error = False
    body = {}
    try:
        completed = request.get_json().get('completed')
        _id = request.get_json().get('id')
        if _id and isinstance(completed, bool):
            todo = Todo.query.get(_id)
            todo.completed = completed
            db.session.commit()
            body['completed'] = todo.completed
            body['id'] = todo.id
        else:
            error = True
    except:
            error = True
            db.session.rollback()
            print(sys.exec_info())
    finally:
        db.session.close()
    if not error:
        return jsonify(body)
    else:
        return abort(400)