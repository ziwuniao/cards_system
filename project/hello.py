from flask import Flask, render_template
# from flask_script import  Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_moment import Moment
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

# manager = Manager (app)
bootstrap = Bootstrap(app)
moment = Moment(app)

class CardForm(FlaskForm):
    name = StringField('最小行动，记张卡片！', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    card = None
    form = CardForm()
    if form.validate_on_submit():
        card = form.card.data
        #不清空会如何？
        form.card.data = ''
    return render_template('index.html', form=form, card=card)

@app.route("/user/<name>")
def user(name):
    return render_template('user.html', name=name)

if __name__ == "__main__":
    app.run(debug=1)