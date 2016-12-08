import logging
from flask import Flask, request, abort, jsonify, make_response
from flask.ext.sqlalchemy import SQLAlchemy, DeclarativeMeta
from json import JSONEncoder

log = logging.getLogger(__name__)


class ProductJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            return obj.to_dict()
        return super(ProductJSONEncoder, self).default(obj)


app = Flask(__name__)
app.json_encoder = ProductJSONEncoder

user = 'ubuntu'
password = 'password'
host = 'localhost'
port = '5432'
db = 'ubuntu' 
url = 'postgresql://{}:{}@{}:{}/{}'
url = url.format(user, password, host, port, db)
app.config['SQLALCHEMY_DATABASE_URI'] = url # 'sqlite:////tmp/tasks.db'
db = SQLAlchemy(app)


class TimeSeriesModel(db.Model):
    __tablename__ = 'timeseries'

    tid = db.Column(db.Integer, primary_key=True)
    mean = db.Column(db.Float, nullable=False)
    std = db.Column(db.Float, nullable=False)
    blarg = db.Column(db.Float, nullable=False)
    level = db.Column(db.Enum('A', 'B', 'C', 'D', 'E', 'F'), nullable=False)

    def __repr__(self):
        return '<Timeseries %r>' % self.tid

    def to_dict(self):
        return dict(tid=self.tid, mean=self.mean, std=self.std, blarg=self.blarg, level=self.level)


class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action = db.Column(db.String(80), nullable=False)


    def __repr__(self):
        return '<User %r>' % self.task_id

    def to_dict(self):
        return dict(action=self.action, task_id=self.task_id)

"""
Timeseries code
"""

@app.route('/timeseries', methods=['GET'])
def get_timeseries_metadata():
    # First check if there are queries
    # Extra credit? Support multiple queries at a time
    
    # Continuous variables only support in
    mean_in = request.args.get('mean_in')
    std_in = request.args.get('std_in')
    blarg_in = request.args.get('blarg_in')

    # Discrete variables support in and equals
    level_in = request.args.get('level_in')
    level = request.args.get('level')
    # If both provided, choose level as it is a stronger option

    # Write SQL statements to get from DB
    
    # Send json of all meta data if no range
    return jsonify({'tid': 'metadata'}), 200

@app.route('/timeseries', methods=['POST'])
def create_timeseries():
    # Request must be a JSON object that has the keys: tid and timeseries
    if (not request.json or not 'id' in request.json or not 'timeseries' in request.json):
        abort(400)
    tid = request.json['id']
    # Timeseries is dictionary/JSON of the format of {'key': value}
    timeseries = request.json['timeseries']
    if not isinstance(timeseries, dict):
        abort(400)
    # TODO: Store it in DBs
    return jsonify(timeseries), 201

@app.route('/timeseries/<int:tid>', methods=['GET'])
def get_timeseries_by_key(tid):
    # Send back metadata and time series data in a JSON
    return 'Return timeseries %d\n' % tid, 200

@app.route('/simquery', methods=['GET'])
def get_topk_similar_ids():
    '''
    Get top k similar time series with respect to the input id in the query string
    '''
    tid = request.args.get('id')
    topk = request.args.get('k')
    if topk is None or not isinstance(topk, int):
        # If k not provided, default to finding top 5 similar timeseries to tid
        topk = 5

    return 'Return timeseries %d\n' % tid, 200

@app.route('/simquery', methods=['POST'])
def get_topk_similar_ids_from_json():
    '''
    Get top k similar time series with respect to the input time series in JSON form in 
    the POST body.
    '''
    if (not request.json or not 'timeseries' in request.json):
        abort(400)
    # Timeseries is dictionary/JSON of the format of {'key': value}
    timeseries = request.json['timeseries']
    if not isinstance(timeseries, dict):
        abort(400)
    topk = request.json['k']
    if topk is None or not isinstance(topk, int):
        # If k not provided, default to finding top 5 similar timeseries to tid
        topk = 5
    return 'Return top %d time series\n' % topk, 200


"""
Deprecated code for tasks
"""

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    log.info('Getting all Tasks')
    return jsonify(dict(tasks=Task.query.all()))


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    task = Task.query.filter_by(task_id=task_id).first()
    if task is None:
        log.info('Failed to get Task with task_id=%s', task_id)
        abort(404)
    log.info('Getting Task with task_id=%s', task_id)
    return jsonify({'task': task})


@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'action' not in request.json:
        abort(400)
    log.info('Creating Task with action=%s', request.json['action'])
    prod = Task(action=request.json['action'])
    db.session.add(prod)
    db.session.commit()
    return jsonify({'op': 'OK', 'task': prod}), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if not request.json or 'action' not in request.json:
        log.info('Could not update. Invalid params')
        abort(400)

    task = Task.query.filter_by(task_id=task_id).first()
    if task is None:
        log.info('Could not find Task id=%s to update', task_id)
        abort(404)

    action = request.json['action']
    log.info('Updating Task id=%s with action %s', task_id, action)
    task.action = action
    db.session.commit()
    return jsonify({'op': 'OK', 'task': task}), 201


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def remove_task(task_id):
    task = Task.query.filter_by(task_id=task_id).first()
    if task is None:
        abort(404)

    log.info('Deleting Task with id=%s', task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'op': 'OK'})


@app.route('/tasks', methods=['DELETE'])
def remove_all_tasks():
    tasks = Task.query.all()
    for task in tasks:
        db.session.delete(task)

    log.info('Deleted all Tasks!')
    db.session.commit()
    return jsonify({'op': 'OK'})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    db.create_all()
    app.run(port=5001)
