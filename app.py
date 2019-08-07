import json
import os
import random
import uuid
from datetime import datetime

import yaml
from bottle import get, post, run, abort, template, request, redirect, default_app, static_file

DEBUG = os.environ.get('DEBUG', False)


@get('/')
def index():
    return template('template/index.html')


@get('/poll/<poll_id>')
def poll(poll_id):
    try:
        file = open(f'data/{poll_id}.yml')
    except FileNotFoundError:
        return abort(404, 'Not Found')
    load = yaml.safe_load(file)
    print(load)
    response = template('template/poll.html', yml_file=load)
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
    poll_id = body.pop('poll-id')

    try:
        poll_file = open(f"data/{poll_id}.yml")
    except FileNotFoundError:
        return abort(404, 'Not Found')

    yml_obj = yaml.safe_load(poll_file)
    poll_file.close()
    print(body)
    for line_name, values in body.items():
        default_values = [None] * len(yml_obj['columns'])

        for i, v in enumerate(values):
            default_values[i] = v

        yml_obj['lines'].update({line_name: default_values})
    with open(f"data/{poll_id}.yml", 'w') as file:
        file.write(yaml.safe_dump(yml_obj))

    return 'ok'


@get('/favicon.ico')
def get_favicon():
    return static_file('favicon.ico', root='static')


if DEBUG:
    run(host='localhost', port=8080, debug=DEBUG)
else:
    app = default_app()
