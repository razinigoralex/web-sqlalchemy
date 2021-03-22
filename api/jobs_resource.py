from flask_restful import Resource, abort
from data import db_session
from data.jobs import Jobs
from api.parser.jobs_parser import parser


def abort_if_not_found(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f'Job {job_id} not found')


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_not_found(job_id)
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).get(job_id)
        return {'jobs': job.to_dict()}

    def delete(self, job_id):
        abort_if_not_found(job_id)
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).get(job_id)
        db_sess.delete(job)
        db_sess.commit()
        return {404: 'OK'}


class JobsListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).all()
        return {'jobs': [job.to_dict() for job in jobs]}

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        job = Jobs(
            id=args['id'],
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            start_date=args['start_date'],
            end_date=args['end_date'],
            is_finished=args['is_finished']
        )
        db_sess.add(job)
        db_sess.commit()
        return {404: 'OK'}
