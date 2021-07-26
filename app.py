from random import shuffle

from flask import Flask, render_template, redirect, jsonify, make_response
from flask_login import LoginManager, logout_user, current_user, login_user
from sqlalchemy import exc

from data import db_session
from data.user import User
from forms.login_form import LoginForm
from forms.signup_form import AuthorizeForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '38bb5726c679e925be0d38b4f15502eb'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        return db_sess.query(User).get(user_id)
    except exc.InvalidRequestError:
        redirect('/')


def get_random_words(n):
    shuffle(accents)
    return accents[:n]


@app.route('/accents')
def play():
    print(get_random_words(20))
    return render_template('accent.html', accents=get_random_words(20))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """login page"""
    if current_user.is_authenticated:
        return redirect(f'/id{current_user.id}')
    form = LoginForm()
    if form.validate_on_submit():  # sign in form
        # if password and user are correct, login the user
        user = db_sess.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильное имя пользователя или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form, message="")


@app.route('/')
def simple_page():
    """main page"""
    return render_template('base.html', user=current_user)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """signup page"""
    if current_user.is_authenticated:
        return redirect(f'/id{current_user.id}')
    form = AuthorizeForm()
    if form.validate_on_submit():
        # if password and control password are equal
        # and username are not taken, add the user to data base
        if form.password.data == form.password_control.data:
            if not db_sess.query(User).filter(User.username == form.username.data).first():
                user = User()
                user.username = form.username.data
                user.create_password_hash(form.password.data)
                db_sess.add(user)
                db_sess.commit()
                return redirect('/login')
            return render_template('signup.html', form=form, message="Такое имя пользователя уже занято")
        return render_template('signup.html', form=form, message="Пароли не совпадают")
    return render_template('signup.html', form=form, message="")  # do not remove 'message' argument here


@app.route('/logout')
def logout():
    """log out from current user account"""
    if current_user.is_authenticated:
        logout_user()
    return redirect('/login')


@app.route('/id<int:profile_id>')
def profile(profile_id):
    """get profile of user with id == :param profile id"""
    profile_data = db_sess.query(User).filter(User.id == profile_id).first()
    if profile_data:
        return render_template('profile.html', user=profile_data)
    return render_template('profile.html', user='Пользователь не найден')


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template('profile.html', user='Вы не можете пока ничего настроить')


@app.errorhandler(404)
def not_found(error):
    """handling errors"""
    return make_response(jsonify({'error': 'Page is not found'}), 404)


accents = open('accent.txt', encoding='UTF_8').readlines()
db_session.global_init("db/web_project.db")
db_sess = db_session.create_session()
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
