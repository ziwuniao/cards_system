from flask import render_template, session, redirect, url_for, Flask, current_app, request,flash
from datetime import datetime
# from flask_script import  Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_moment import Moment
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
import os


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config["SQLALCHEMY_DATABASE_URI"] =\
            'sqlite:///' + os.path.join(basedir, 'data.sqlite')

#有了这个，就不会忘记comit啦？
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['Debug'] = True


# manager = Manager (app)

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

#创建卡片写作表单
class CardForm(FlaskForm):
    title = TextAreaField("卡片标题", validators = [Required()])
    body = TextAreaField('最小行动，记张卡片！', validators=[Required()])
    submit = SubmitField('Submit')

#创建卡片数据库对象模型
class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(60))
    body = db.Column(db.String(350))
    timestamp = db.Column(db.DateTime, index=True)
    # author_id = db. Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.timestamp = datetime.utcnow()


@app.route("/", methods = ['GET', 'POST'])
def index():
    form = CardForm()
    if form.validate_on_submit():
        card = Card(body = form.body.data, title = form.title.data)
        db.session.add(card)
        return redirect(url_for('.index'))
    cards = Card.query.order_by(Card.timestamp.desc()).all()
    return render_template('index.html', form = form, cards = cards)


@app.route('/new', methods=['GET', 'POST'])
def new():
    form = CardForm()
    if form.validate_on_submit():
        print(form.body.data, form.title.data)
        card = Card(body = form.body.data, title = form.title.data)
        db.session.add(card)
        return redirect(url_for('.index'))
    return render_template('index.html', form = form)

#新功能测试页面
@app.route('/test', methods = ['GET', 'POST'])
def test():
    return render_template('test.html')

@app.route('/test_card', methods = ['GET', 'POST'])
def test_card():
    cards = Card.query.order_by(Card.timestamp.desc()).all()
    return render_template('test_card.html', cards=cards)

@app.route('/show_all', methods=['GET', 'POST'])
def show_all():
    cards = Card.query.order_by(Card.timestamp.desc()).all()
    return render_template('show_all.html', cards=cards)


# 在程序运行时即初始化数据库
@app.before_first_request
def setupDatabase():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=1)
