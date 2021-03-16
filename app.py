''' BEGIN CONFIG '''
from flask import *
from flask_wtf import *
from wtforms import *
from wtforms.validators import *

import os
import jsonpickle

from models.APP import forms, users, apis

app = Flask(__name__,
            template_folder='template',
            static_folder='static' )

app.config.update(
    TEMPLATES_AUTO_RELOAD = True,
    SECRET_KEY = 'secret'
)


''' BEGIN ABOUT '''
@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html',
                            page='About')


''' BEGIN LOGIN '''
@app.route('/database/connect', methods=['GET', 'POST'])
def connect():
    # if current session is still saves in cookies, return to that session
    # if session['session_obj']:
    #     flash('Returned to the previous unsaved session.', 'info')
    #     session_obj = jsonpickle.decode(session['session_obj'])
    #     return redirect(url_for('on_session', page=session_obj.getName()))

    ipform = forms.IPForm()
    server_connected = False
    if request.method == "POST":
        if ipform.validate_on_submit():
            # try server connection and if responding
            try:
                server_connected = apis.connect_server(ipform.ip.data, ipform.port.data)
                if server_connected:
                    session['ip'], session['port'] = ipform.ip.data, ipform.port.data
                    flash('Successfully connected to the server.', 'success')
                    return redirect(url_for('login'))
            except:
                flash('Unable to reach the server. Please check if you have FHE_Server setup properly.', "error")
        if not ipform.validate_on_submit():
            flash('Invalid IP Address or Port. Please try again.', "error")
            return redirect(url_for('connect'))

    return render_template('connect.html',
                            page='Database Connect',
                            ipform=ipform)


@app.route('/database/login', methods=['GET', 'POST'])
def login():
    # if user closed broswer window or cookie expired
    if session.get('ip') is None:
        flash('Session expired. Please reconnect to the server.', "info")
        return redirect(url_for('connect'))
    # if current session is still saves in cookies, return to that session
    # if session['session_obj']:
    #     flash('Returned to the previous unsaved session.', 'info')
    #     session_obj = jsonpickle.decode(session['session_obj'])
    #     return redirect(url_for('on_session', page=session_obj.getName()))

    newSessionConfig = forms.configNewSession()
    oldSessionConfig = forms.configOldSession()
    if request.method == "POST":
        # If clicked on new session submit
        if newSessionConfig.validate_on_submit():
            # Check if session of same name under one public ip exists
            if apis.check_exist_session(session['ip'], session['port'], newSessionConfig.session_name.data):
                session.pop('_flashes', None)
                flash("This session name is used. Please upload the file or enter a new name.", 'error')
                return redirect(url_for('login'))
            else:
                new_session = users.Session()
                new_session.setName(newSessionConfig.session_name.data)
                new_session.setKey(newSessionConfig.key_size.data)
                session['session_obj'] = new_session.toJson() # session cookie for other views
                session['session_name'] = newSessionConfig.session_name.data
                session['key_size'] = newSessionConfig.key_size.data
                session['data_type'] = newSessionConfig.data_type.data
                session.pop('_flashes', None)
                flash("New Session created.", "success")
                return redirect(url_for('on_session',page=newSessionConfig.session_name.data))
        if not newSessionConfig.validate_on_submit():
            session.pop('_flashes', None)
            flash("You have entered a invalid session name. Name should only contain letters and numbers.", "error")
            return redirect(url_for('login'))
    return render_template('login.html', newSessionConfig=newSessionConfig, oldSessionConfig=oldSessionConfig, page="Database Login")


''' BEGIN SESSION '''
@app.route('/database/session/<page>', methods=['GET', 'POST'])
def on_session(page):
    dataEntry_int = forms.dataEntry_int()
    dataEntry_poly = forms.dataEntry_poly()
    if request.method == "POST":
        # validates data entry form
        if dataEntry_int.validate_on_submit() or dataEntry_poly.validate_on_submit():
            session.pop('_flashes', None)
            flash("Data Created", "success")
            return redirect(url_for('on_session',page=page))
        elif dataEntry_poly.submit_poly.data and dataEntry_poly.validate_on_submit()==False:
            session.pop('_flashes', None)
            flash("Invalid Label (AlphaNumeric) or Data (x-Var Polynomial). Please try again.", "error")
        elif dataEntry_int.submit_int.data and dataEntry_int.validate_on_submit()==False:
            session.pop('_flashes', None)
            flash("Invalid Label (AlphaNumeric) or Data (Integer). Please try again.", "error")


    return render_template('session.html', page=page, dataEntry_int=dataEntry_int, dataEntry_poly=dataEntry_poly)


''' BEGIN DEMO '''
@app.route('/demo',methods=['GET', 'POST'])
def demo():
    return jsonify({'msg':'hello'})
