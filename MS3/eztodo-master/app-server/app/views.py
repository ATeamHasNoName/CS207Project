import os
import logging
from app import app
from app.service import APIService
from flask import render_template, send_from_directory
from flask import Flask, request, abort, redirect, url_for, jsonify, make_response

log = logging.getLogger(__name__)
service = APIService()

@app.route('/')
def home():
    # tasks = service.all_tasks()
    timeseries = service.timeseries_metadata
    return render_template('index.html', timeseries=timeseries)

@app.route('/remove_task', methods=['POST'])
def remove_task():
    service.remove_task()
    return jsonify({'op': True}), 201

@app.route('/update_task', methods=['POST'])
def update_task():
    service.update_task()
    return jsonify({'op': True}), 201

@app.route('/taskop', methods=['POST'])
def task_operation():
    if (not request.json 
            or 'op' not in request.json
            or 'action' not in request.json):
        abort(400)

    log.debug('Task Operation %s', request.json)
    op = request.json['op']
    if op == 'ADD':
        action = request.json['action']
        json_response = service.add_task(action)
        log.debug('Response: %s', json_response)
        return jsonify(json_response), 201
    elif op == 'DELETE':
        task_id = request.json['task_id']
        json_response = service.delete_task(task_id)
        log.debug('Response: %s', json_response)
        return jsonify(json_response), 201
    elif op == 'UPDATE':
        task_id = request.json['task_id']
        action = request.json['action']
        json_response = service.update_task(task_id, action)
        log.debug('Response: %s', json_response)
        return jsonify(json_response), 201
    else:
        log.info('Unsupported OP %s', op)
    return jsonify({'op': True}), 201

@app.route('/static/<string:directory>/<path:path>')
def send_static(directory, path):
    log.info('Static File Dir:%s, Path:%s', directory, path)
    return send_from_directory('static', os.path.join(directory, path))
