''' BEGIN CONFIG '''
from flask import *
from flask_wtf import *
from wtforms import *
from wtforms.validators import *

from models.APP import forms


app = Flask(__name__,
            template_folder='template',
            static_folder='static' )

app.config.update(
    TEMPLATES_AUTO_RELOAD = True,
    SECRET_KEY = 'hard to guess string'
)


''' BEGIN ABOUT '''
@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html',
                            page='About')


''' BEGIN LOGIN '''
class IPForm(FlaskForm):
    ip = StringField('Server IP', validators=[IPAddress(), DataRequired()], render_kw={"placeholder": '192.168.1.1'})
    port = DecimalField('Port', validators=[DataRequired()], render_kw={"placeholder": '2830'})
    submit = SubmitField('Connect')

class SessionMgmt(FlaskForm):
    server_connected = False
    newSession = SubmitField('Create')
    oldSession = SubmitField('Upload')

def connect_server():
    return True

@app.route('/login', methods=['GET', 'POST'])
def login():
    ipform = IPForm()
    sessionmgmt = SessionMgmt()
    if request.method == "POST":
        if ipform.validate_on_submit():
            sessionmgmt.server_connected = connect_server()
        else:
            flash('Invalid IP Address or Port.', "error")
            return redirect(url_for('login'))
    return render_template('login.html',
                            page='Database Login',
                            ipform=ipform, sessionmgmt=sessionmgmt)


''' BEGIN SESSION '''
@app.route('/database/session/<page>')
def database(page):
    return render_template('database.html',
                            page=page)


''' BEGIN DEMO '''
@app.route('/demo',methods=['GET', 'POST'])
def demo():
    form = IPForm()
    if form.validate_on_submit():
        pass
    return render_template('demo.html',
                            page='Demo',
                            form=form)
