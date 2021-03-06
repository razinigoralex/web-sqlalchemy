from flask import Flask, redirect, render_template
from flask_login import LoginManager, login_user, logout_user, login_required

from data import db_session
from data.users import User
from data.jobs import Jobs
from data.planet_info import planet_info

from forms.user import RegisterForm
from forms.login import LoginForm
from forms.job import MakeJobForm

from flask_restful import Api

from api.jobs_api import blueprint as jobs_blueprint
from api.users_resource import UsersResource, UsersListResource
from api.jobs_resource import JobsResource, JobsListResource


def get_app(namespace):
    app = Flask(namespace)
    app.config['SECRET_KEY'] = 'pizza_mozzarella'

    login_manager = LoginManager()
    login_manager.init_app(app)
    
    app.register_blueprint(jobs_blueprint)
    
    @login_manager.user_loader
    def load_user(user_id):
        db_sess = db_session.create_session()
        return db_sess.query(User).get(user_id)

    @app.route('/')
    def main():
        return render_template('base.html')
    
    @app.route('/choice/<string:planet_name>', methods=['GET'])
    def choice(planet_name):
        content = planet_info[planet_name]
        return render_template('choice.html', title='Варианты выбора', planet_name=planet_name, content=content)

    @app.route('/job_list', methods=['GET'])
    def job_list():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).all()
        return render_template('job_list.html', title='Список работ', jobs=jobs)

    @app.route('/register', methods=['POST', 'GET'])
    def register():
        form = RegisterForm()

        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                surname=form.surname.data,
                name=form.name.data,
                age=form.age.data,
                position=form.position.data,
                speciality=form.speciality.data,
                address=form.address.data,
                email=form.email.data,
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
        return render_template('register.html', title='Регистрация', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        return render_template('login.html', title='Авторизация', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect('/')

    @app.route('/make_job', methods=["POST", "GET"])
    def make_job():
        form = MakeJobForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            job = Jobs(
                team_leader=form.team_leader.data,
                job=form.job.data,
                work_size=form.work_size.data,
                collaborators=form.collaborators.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                is_finished=False
            )
            print(form.start_date.data)
            db_sess.add(job)
            db_sess.commit()
            return redirect('/')
        return render_template('make_job.html', title='Создать работу', form=form)

    return app


def make_api(api):
    api.add_resource(UsersResource, '/api/v2/users/<int:user_id>')
    api.add_resource(UsersListResource, '/api/v2/users')
    api.add_resource(JobsResource, '/api/v2/jobs/<int:job_id>')
    api.add_resource(JobsListResource, '/api/v2/jobs')


if __name__ == '__main__':
    app = get_app(__name__)
    db_session.global_init('db/users.db')
    api = Api(app)
    make_api(api)
    app.run()
