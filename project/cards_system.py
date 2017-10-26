#配置数据库
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
 
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI‘] =\
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
#定义新的数据库仓库
class Post(db.Model):
	__tablename__ = 'post'
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datatime.utcnow)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	
class User(UserMixin, db.Model):
	# ...
	post = db.relationship('Post', backef= 'author', lazy='dynamic')
