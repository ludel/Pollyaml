import json
import os
import random
import uuid
from datetime import datetime

import yaml
from bottle import get, post, run, abort, static_file, template, request, redirect

DEBUG = os.environ.get('DEBUG', False)


@get('/')
def index():
    return template('template/index.html')


@get('/poll/<poll_id>')
def poll(poll_id):
    try:
        file = open(f'data/{poll_id}.yml')
    except FileNotFoundError:
        return abort(404)
    else:
        response = template('template/poll.html', yml_file=yaml.safe_load(file))
        file.close()

    return response


@post('/table')
def table():
    try:
        yml_obj = yaml.safe_load(request.body.read())
        columns = yml_obj['columns']
    except (yaml.YAMLError, KeyError):
        return abort(400, 'YAML parse error')

    lines = {
        'Andrey': [random.choice((True, False, None)) for _ in columns],
        'Julie': [random.choice((True, False, None)) for _ in columns],
        'Joe': [random.choice((True, False, None)) for _ in columns],
    }

    return template(
        'template/table.html',
        columns=columns,
        lines=lines
    )


@post('/export')
def export():
    try:
        form = request.forms['yml']
        yml_obj = yaml.safe_load(form)
    except yaml.YAMLError:
        return abort(400, 'YAML parse error')
    except KeyError:
        return abort(400, 'No file provider')

    poll_id = uuid.uuid4().hex[:10]

    yml_obj['datetime'] = datetime.now()
    yml_obj['poll-id'] = poll_id
    yml_obj['lines'] = {}
    yml_obj['comments'] = None
    yml_obj['title'] = yml_obj.get('title', 'Unnamed poll')
    yml_obj['author'] = yml_obj.get('author', 'Anonymous')
    yml_obj['columns'] = yml_obj.get('columns', {'Unnamed column'})

    with open(f'data/{poll_id}.yml', 'w') as file:
        file.write(yaml.safe_dump(yml_obj))

    return redirect(f'poll/{poll_id}')


@post('/line')
def line():
    body = json.loads(request.body.read())

    try:
        read_file = open(f"data/{body['poll-id']}.yml")
    except FileNotFoundError:
        return abort(404)

    yml_obj = yaml.safe_load(read_file)
    read_file.close()

    values = []
    for i in range(len(yml_obj['columns'])):
        values.append(body.get(str(i), None))

    yml_obj['lines'].update({body['name']: values})

    with open(f"data/{body['poll-id']}.yml", 'w') as file:
        file.write(yaml.safe_dump(yml_obj))

    return 'ok'


@get('/static/<path:path>')
def static(path):
    return static_file(path, root='static')


run(host='localhost', port=8080, debug=DEBUG)
