from flask_restful import Resource, abort
from data import db_session
from data.users import User
from api.parser.users_parser import parser


def abort_if_not_found(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        abort(404, message=f'User {user_id} not found')


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        return {'users': user.to_dict()}

    def delete(self, user_id):
        abort_if_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        db_sess.delete(user)
        db_sess.commit()
        return {404: 'OK'}


class UsersListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return {'users': [user.to_dict() for user in users]}

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        users = User(
            id=args['id'],
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
        )
        db_sess.add(users)
        db_sess.commit()
        return {404: 'OK'}
