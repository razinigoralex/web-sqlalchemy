import flask

from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint('jobs_api',
                            __name__,
                            template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return {'jobs': [item.to_dict() for item in jobs]}


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_asked_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)

    if not job:
        return flask.jsonify({'error': 'Ничего не найдено'})

    return {'job': job.to_dict()}


@blueprint.route('/api/jobs', methods=['POST'])
def make_job():
    if not flask.request.json:
        return {'error': 'Empty request'}

    if not all(key in flask.request.json for key in ['team_leader', 'job', 'work_size', 'id']):
        return {'error': 'Not enough parameters'}

    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == flask.request.json['id']).first()

    if not jobs:
        job = Jobs(
            id=flask.request.json['id'],
            team_leader=flask.request.json['team_leader'],
            job=flask.request.json['job'],
            work_size=flask.request.json['work_size'],
        )

        db_sess.add(job)
        db_sess.commit()
        return {'200': 'OK'}
    else:
        return {'error': 'Id already exists'}


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)

    if not job:
        return {'error': 'Not found'}

    db_sess.delete(job)
    db_sess.commit()
    return {'200': 'OK'}
