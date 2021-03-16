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
    return flask.jsonify(
        {
            'jobs': [item.to_dict() for item in jobs]
        }
    )


@blueprint.route('/api/news/<int:job_id>', methods=['GET'])
def get_asked_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)

    if not job:
        return flask.jsonify({'error': 'Ничего не найдено'})

    return flask.jsonify(
        {
            'job': job.to_dict()
        }
    )
