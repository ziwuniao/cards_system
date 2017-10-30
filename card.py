from flask import render_template, session, redirect, url_for, Flask, current_app, request,flash
from datetime import datetime
# from flask_script import  Manager
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from flask_moment import Moment
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy.sql.expression import func
import os
# 为flask-WTF增加markdown功能支持
from flask_pagedown import PageDown
from flask_pagedown.fields import PageDownField
# 为markdown的显示支持
import markdown
from flaskext.markdown import Markdown


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config["SQLALCHEMY_DATABASE_URI"] =\
            'sqlite:///' + os.path.join(basedir, 'data.sqlite')

#有了这个，就不会忘记comit啦？
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['Debug'] = True

#各种初始化，不是特别理解
# manager = Manager (app)

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
pagedown = PageDown(app)
Markdown(app)

#创建卡片写作表单
class CardForm(Form):
    title = TextAreaField("卡片标题", validators = [Required()])
    body = PageDownField('卡片内容，支持Markdown', validators=[Required()])
    submit = SubmitField('Submit')

#创建卡片数据库对象模型
class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(60))
    body = db.Column(db.String(350))
    timestamp = db.Column(db.DateTime, index=True)
    #创建时得到Markdown的HTML代码缓存到数据库这个列中。
    body_html = db. Column(db.Text)
    # author_id = db. Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.timestamp = datetime.utcnow()
        #创建时得到Markdown的HTML代码缓存到数据库这个列中。
        self.body_html = markdown(self.body, output_format='html')
#这个好难,没有看懂，参考flask开发书P126
#     @staticmethod
#     def on_changed_body(target, value, oldvalue, initiator):
#         allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
#                         'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
#                         'h1', 'h2', 'h3', 'p']
#         target.body_html = bleach.linkify(bleach.clean(
#             markdown(value, output_format='html'),
#             tags=allowed_tags, strip=True))
#
# db.event.listen(Card.body, 'set', Card.on_changed_body)


@app.route("/", methods = ['GET', 'POST'])
def index():
    form = CardForm()
    if form.validate_on_submit():
        card = Card(body = form.body.data, title = form.title.data, body_html = form.body_html.data)
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
    #不知道为何需要用到request.args
    print(request.args.get("shuffle"))
    print(request)
    print(request.args)

    if request.args.get("shuffle") == "乱序拼接":
        #将数据库查询结果乱序

        cards = Card.query.order_by(func.random()).all()

    else:
        cards = Card.query.order_by(Card.timestamp.desc()).all()

    return render_template('show_all.html', cards =cards)


# 在程序运行时即初始化数据库
@app.before_first_request
def setupDatabase():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=1)
