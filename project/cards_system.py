#创建新的数据库仓库
from flask import Flask, render_template
# from flask_script import  Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_moment import Moment
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class Post(db.Model):
	__tablename__ = 'post'
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datatime.utcnow)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	
class User(UserMixin, db.Model):
	# ...
	post = db.relationship('Post', backef= 'author', lazy='dynamic')