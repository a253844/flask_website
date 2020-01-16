from app_blog import app
from app_blog import db
from flask import render_template, flash, redirect, url_for, request , session
from app_blog.author.model import UserReister , Userlog , UserRelation , UserMessage
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
        flash('Your Account Register Success !!')
        return redirect(url_for('login'))
    return render_template('author/register.html', form=form)


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    users = UserReister.query.order_by(UserReister.username).all()
    user_lists = []
    for i in range(len(users)):
        relate_list = []
        if users[i].username != current_user.username:
            relate_list.append(users[i].username)
            relate = UserRelation.query.filter_by(user_A=current_user.id , user_B=users[i].id).first()
            invite = UserRelation.query.filter_by(user_A=users[i].id , user_B=current_user.id).first()
            if relate == None:
                relate_list.append("0")
                if invite == None:
                    relate_list.append("0")
                else:
                    relate_list.append(invite.relation)
            else:
                relate_list.append(relate.relation)
                if invite == None:
                    relate_list.append("0")
                else:
                    relate_list.append(invite.relation)
            user_lists.append(relate_list)

    user_friends = []
    User_notices = []
    for i in range(len(users)):
        notice_list = []
        if users[i].username != current_user.username:
            relate_1 = UserRelation.query.filter_by(user_A=current_user.id , user_B=users[i].id).first()
            relate_2 = UserRelation.query.filter_by(user_A=users[i].id , user_B=current_user.id).first()
            notice = UserMessage.query.filter_by(user_A=users[i].id , user_B=current_user.id).first()
            if relate_1 != None and relate_1.relation == '2' :
                user_friends.append(users[i].username)
            if relate_2 != None and relate_2.relation == '2' :
                user_friends.append(users[i].username)
            if notice != None :
                notice_list.append(users[i].username)
                notice_list.append(notice.message)
                User_notices.append(notice_list)
    return render_template('author/Home.html' , login_user_name=current_user.username , user_lists=user_lists , \
                            user_friends=user_friends , User_notices = User_notices)

@app.route('/get_invite', methods=['GET', 'POST'])
@login_required
def get_invite():
    user_chose = request.form.get("user_chose")
    users = UserReister.query.filter_by(username=user_chose ).first()
    retry = UserRelation.query.filter_by(user_A=current_user.id , user_B =users.id ).first()
    if retry == None:
        user = UserRelation(
            user_A=current_user.id,
            user_B=users.id,
            relation='1',
            time=datetime.now()
            )
        db.session.add(user)
        db.session.commit()
    else:
        retry.relation = '1'
        db.session.add(retry)
        db.session.commit()
    flash('Your invite already send !!')
    return redirect(url_for('index'))

@app.route('/get_response', methods=['GET', 'POST'])
@login_required
def get_response():
    user_invite = request.form.get("user_invite")
    get_response = request.form.get("response")
    users = UserReister.query.filter_by(username=user_invite).first()
    answer = UserRelation.query.filter_by(user_A=users.id , user_B =current_user.id ).first()
    if get_response == 'YES' :
        answer.relation = "2"
    elif get_response == 'NO' :
        answer.relation = "3"
    db.session.add(answer)
    db.session.commit()
    flash('Your response already send !!')
    return redirect(url_for('index'))

@app.route('/get_message', methods=['GET', 'POST'])
@login_required
def get_message():
    if request.method == "POST":
        user_message = request.form.get("usercomment")
        user_option = request.form.get("user_option")

        users = UserReister.query.filter_by(username=user_option ).first()
        if user_message != None :
            user = UserMessage(
                user_A=current_user.id,
                user_B=users.id,
                message=user_message,
                time=datetime.now()
                )
            db.session.add(user)
            db.session.commit()
            flash('Your message already send !!')
    return redirect(url_for('index'))

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
        db.session.add(user)
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
