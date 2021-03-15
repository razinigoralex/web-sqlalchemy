from flask import Flask, redirect, render_template
from flask_login import LoginManager, login_user, logout_user, login_required
from data import db_session
from data.users import User
from forms.user import RegisterForm
from forms.login import LoginForm


def get_app(namespace):
    app = Flask(namespace)
    app.config['SECRET_KEY'] = 'pizza_mozzarella'

    @app.route('/')
    def main():
        return 'Привет!'

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
                return redirect('/')

            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)

        return render_template('login.html',
                               title='Авторизация',
                               form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect('/')

    return app


if __name__ == '__main__':
    app = get_app(__name__)
    db_session.global_init('db/users.db')

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        db_sess = db_session.create_session()
        return db_sess.query(User).get(user_id)

    app.run()
