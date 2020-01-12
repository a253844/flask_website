from app_blog import app
from app_blog import db
from flask import render_template, flash, redirect, url_for, request , session
from app_blog.author.model import UserReister , Userlog
from app_blog.author.form import FormRegister, FormLogin , ChangeInfo
from flask_login import login_user, current_user, login_required , logout_user
from datetime import timedelta , datetime

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = FormRegister()

    if form.validate_on_submit():
        user = UserReister(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
            )
        db.session.add(user)
        db.session.commit()
        flash('Yor Account Register Success !!.')
        return redirect(url_for('login'))
    return render_template('author/register.html', form=form)


@app.route('/')
@login_required
def index():
    #flash('flash-1')
    #flash('flash-2')
    #flash('flash-3')
    return render_template('base.html' , login_user_name=current_user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        user = UserReister.query.filter_by(email=form.email.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user, form.remember_me.data)
                next = request.args.get('next')
                if not next_is_valid(next):
                    return 'Bad Boy!!'
                userlog = Userlog(
                    username=user.username,
                    time=datetime.now(),
                    state="login" ,
                    user_id = user.id
                    )
                db.session.add(userlog)
                db.session.commit()
                return redirect(next or url_for('index') )
            else:
                flash('Wrong Email or Password')
        else:
            flash('Wrong Email or Password')
    return render_template('author/login.html', form=form)

def next_is_valid(url):
    return True

@app.route('/logout')
@login_required
def logout():
    user = UserReister.query.filter_by(username=current_user.username).first()
    userlog = Userlog(
        username=user.username,
        time=datetime.now(),
        state="logout" ,
        user_id = user.id
        )
    db.session.add(userlog)
    db.session.commit()
    logout_user()
    flash('Log Out See You.')
    return redirect(url_for('index'))

@app.route('/userinfo', methods=['GET', 'POST'])
@login_required
def userinfo():
    user_name=current_user.username
    user_email=current_user.email

    form = ChangeInfo()
    if form.validate_on_submit():
        user = UserReister.query.filter_by(username=current_user.username).first()
        user.username = form.username.data
        db.session.commit()
        flash('Yor Account Change Infomation Success !!')
        return redirect(url_for('userinfo'))
    return render_template('author/userinfo.html' , login_user_name = user_name , \
                            login_user_email = user_email , form = form)

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)
    #flash('5 second not interact ! Auto Login Out !!!')
