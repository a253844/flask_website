from app_blog import db, bcrypt , login
from flask_login import UserMixin

class UserReister(UserMixin , db.Model):

    __tablename__ = 'UserRgeisters'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(50), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf8')


    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return 'username:%s, email:%s' % (self.username, self.email)

    @login.user_loader
    def load_user(user_id):
        return UserReister.query.get(int(user_id))

class Userlog(db.Model):

    __tablename__ = 'Userlogs'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30) , nullable=False)
    time = db.Column(db.DateTime(timezone=True), nullable=False)
    state = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('UserRgeisters.id'))

    def __repr__(self):
        return 'username:%s, time:%s , state:%s' % \
            (self.username, self.time , self.state)

class UserRelation(db.Model):

    __tablename__ = 'UserRelation'
    id = db.Column(db.Integer, primary_key=True)
    user_A = db.Column(db.Integer, db.ForeignKey('UserRgeisters.id'))
    user_B = db.Column(db.Integer, db.ForeignKey('UserRgeisters.id'))
    relation = db.Column(db.String(30), nullable=False)
    time = db.Column(db.DateTime(timezone=True), nullable=False)

    def __repr__(self):
        return 'user_A:%s, user_B:%s , relation:%s , time:%s' % \
            (self.user_A, self.user_B, self.relation , self.time)

class UserMessage(db.Model):

    __tablename__ = 'UserMessage'
    id = db.Column(db.Integer, primary_key=True)
    user_A = db.Column(db.Integer, db.ForeignKey('UserRgeisters.id'))
    user_B = db.Column(db.Integer, db.ForeignKey('UserRgeisters.id'))
    message = db.Column(db.String(250), nullable=False)
    time = db.Column(db.DateTime(timezone=True), nullable=False)

    def __repr__(self):
        return 'user_A:%s, user_B:%s , messagepython:%s , time:%s' % \
            (self.user_A, self.user_B, self.message , self.time)
