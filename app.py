''' BEGIN CONFIG '''
from flask import *
from flask_wtf import *
from wtforms import *
from wtforms.validators import *
# from flaskwebgui import *

import os
import jsonpickle
import requests
from py_expression_eval import *

from models.APP import forms, users, apis
from models.FHE.FHE_Integer import FHE_Integer

app = Flask(__name__,
            template_folder='template',
            static_folder='static'
)

app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
    SECRET_KEY='secret'
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
    fileForm = forms.fileForm()
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
                           ipform=ipform, fileForm=fileForm)


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
    if request.method == "POST":
        # If clicked on new session submit
        if newSessionConfig.validate_on_submit():
            # Check if session of same name under one public ip exists
            checkExist = apis.exist_session(newSessionConfig.session_name.data)
            if type(checkExist) == bool and checkExist == True:
                session.pop('_flashes', None)
                flash("This session name is used. Please upload the file or enter a new name.", 'error')
                return redirect(url_for('login'))
            else:
                new_session = users.Session()
                new_session.setName(newSessionConfig.session_name.data)
                new_session.setKeySize(newSessionConfig.key_size.data)
                new_session.setServerId(checkExist)

                # session cookie for other views
                session['session_obj'] = new_session.freeze()
                session['session_name'] = newSessionConfig.session_name.data
                session['key_size'] = newSessionConfig.key_size.data
                session['data_type'] = newSessionConfig.data_type.data


                session.pop('_flashes', None)
                flash("New Session created.", "success")
                return redirect(url_for('on_session', page=session['session_name']))
        if not newSessionConfig.validate_on_submit():
            session.pop('_flashes', None)
            flash("You have entered a invalid session name. Name should only contain letters and numbers.", "error")
            return redirect(url_for('login'))
    return render_template('login.html', newSessionConfig=newSessionConfig, page="Database Login")


''' BEGIN SESSION '''

@app.route('/database/session/<page>', methods=['GET', 'POST'])
def on_session(page):
    dataEntry_int = forms.dataEntry_int()
    dataEntry_poly = forms.dataEntry_poly()
    dataEval = forms.dataEval()
    dataDecrypt = forms.dataDecrypt()

    if request.method == "POST":

        session['decrypted'] = None

        # validates data entry form
        if dataEntry_int.validate_on_submit() or dataEntry_poly.validate_on_submit():

            session_obj = jsonpickle.decode(session['session_obj'])

            if dataEntry_int.data_label_int.data in session_obj.set:
                session.pop('_flashes', None)
                flash("Label exists in this session. Try another label.", "error")

            else:
                x = FHE_Integer(dataEntry_int.data_field_int.data, int(session_obj.key_size))
                encrypted = x.encrypt()
                server_set_id = apis.create_data(x, encrypted[0], encrypted[2])
                session_obj.set[dataEntry_int.data_label_int.data] = [encrypted[1], encrypted[3], None, server_set_id]
                encrypted = None


                session.pop('_flashes', None)
                flash("Data created", "success")

            session['session_obj'] = session_obj.freeze()
            return redirect(url_for('on_session', page=page))


        elif dataEntry_int.submit_int.data and dataEntry_int.validate_on_submit() == False:
            session.pop('_flashes', None)
            flash("Invalid Label (AlphaDash) or Data (Integer). Please try again.", "error")

        if dataEval.validate_on_submit():

            session_obj = jsonpickle.decode(session['session_obj'])
            print(session_obj.set)

            if dataEval.data_label_eval.data in session_obj.set:
                session.pop('_flashes', None)
                flash("Label exists in this session. Try another label.", "error")
            else:
                parser = Parser()
                try:
                    expr = parser.parse(dataEval.data_field_eval.data).simplify({})
                    expr_str = expr.toString()
                    var = expr.variables()
                    if len(var) > 2:
                        session.pop('_flashes', None)
                        flash("Expression can have Max of 2 variables. Please try another expression", "error")
                    else:
                        for i in var:
                            expr_str = expr_str.replace(i, "")
                        if any(c not in '(+-*)1234567890' for c in expr_str):
                            session.pop('_flashes', None)
                            flash("Only +/-/*/() are allowed. Please consult the Usage Guide.", "error")
                        elif any(l not in session_obj.set for l in var):
                            session.pop('_flashes', None)
                            flash("Label(s) in the expression doesn't exist. Please try again.", "error")
                        else:
                            id_str = expr.toString()
                            for i in var:
                                id_str = id_str.replace(i, session_obj.set[i][3])
                            server_eval_id = apis.create_eval(id_str)
                            session_obj.set[dataEval.data_label_eval.data] = [None, None, expr.toString(), server_eval_id]
                            session.pop('_flashes', None)
                            flash("Expression created", "success")
                except:
                    session.pop('_flashes', None)
                    flash("Illegal expression. Please consult the Usage Guide.", "error")

                session['session_obj'] = session_obj.freeze()
                return redirect(url_for('on_session', page=page))

        elif dataEval.submit_eval.data and dataEval.validate_on_submit() == False:
            session.pop('_flashes', None)
            flash("Invalid Label (AlphaDash) or Expression. Please try again.", "error")

        if dataDecrypt.validate_on_submit():
            session_obj = jsonpickle.decode(session['session_obj'])

            if dataDecrypt.data_label_decrypt.data not in session_obj.set:
                session.pop('_flashes', None)
                flash("Label does not exist in this session. Try another label.", "error")

            else:
                id = session_obj.set[dataDecrypt.data_label_decrypt.data][3]
                session['decrypted'] = [dataDecrypt.data_label_decrypt.data, apis.decrypt(id)]

            session['session_obj'] = session_obj.freeze()
            return redirect(url_for('on_session', page=page))


        elif dataDecrypt.submit_decrypt.data and dataDecrypt.validate_on_submit() == False:
            session.pop('_flashes', None)
            flash("Invalid Label (AlphaDash). Please try again.", "error")


    return render_template('session.html', page=page, dataEntry_int=dataEntry_int, dataEntry_poly=dataEntry_poly, dataEval=dataEval, dataDecrypt=dataDecrypt)


''' BEGIN DEMO '''


@app.route('/demo', methods=['GET', 'POST'])
def demo():
    return jsonify({'msg': 'hello'})


# if __name__ == "__main__":
#     FlaskUI(app).run()
