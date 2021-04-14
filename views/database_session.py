from app import *
from models.FHE import FHE_Client, FHE_Integer

@app.route('/database/session/<page>', methods=['GET', 'POST'])
def on_session(page):
    dataEntry_int = forms.dataEntry_int()
    dataEntry_poly = forms.dataEntry_poly()
    dataEval = forms.dataEval()
    dataDecrypt = forms.dataDecrypt()

    if request.method == "POST":

        session['decrypted'] = None

        # validates data entry form
        if dataEntry_int.validate_on_submit():

            session_obj = jsonpickle.decode(session['session_obj'])
            fhe_obj = jsonpickle.decode(session['fhe_obj'])

            # TODO ... Overwrite
            if dataEntry_int.data_label_int.data in session_obj.set:
                session.pop('_flashes', None)
                flash("Label exists in this session. Try another label.", "error")

            else:

                x = FHE_Integer.FHE_Integer(dataEntry_int.data_field_int.data, fhe_obj.m, fhe_obj.p)
                encrypted = x.encrypt()
                set_id = apis.create_data(encrypted.x_prime, encrypted.q)
                session_obj.set[dataEntry_int.data_label_int.data] = {"x_prime": encrypted.x_prime,
                                                                      "q": encrypted.q,
                                                                      "set_id": set_id}
                encrypted = None
                session.pop('_flashes', None)
                flash("Data created", "success")

            session['session_obj'] = jsonpickle.encode(session_obj)
            session['fhe_obj'] = jsonpickle.encode(fhe_obj)
            return redirect(url_for('on_session', page=page))


        elif dataEntry_int.submit_int.data and dataEntry_int.validate_on_submit() == False:
            session.pop('_flashes', None)
            flash("Invalid Label (AlphaDash) or Data (Integer). Please try again.", "error")

        if dataEval.validate_on_submit():

            session_obj = jsonpickle.decode(session['session_obj'])
            fhe_obj = jsonpickle.decode(session['fhe_obj'])


            # TODO ... Overwrite
            if dataEval.data_label_eval.data in session_obj.set:
                session.pop('_flashes', None)
                flash("Label exists in this session. Try another label.", "error")
            else:
                parser = Parser()
                try:
                    expr = parser.parse(dataEval.data_field_eval.data).simplify({})
                    expr_str = expr.toString()
                    var = expr.variables()
                    if len(var) < 1:
                        session.pop('_flashes', None)
                        flash("Expression needs to have at least one variable. Please try another expression", "error")
                    else:
                        for i in var:
                            expr_str = expr_str.replace(i, "")
                        if any(c not in '(+-*)1234567890' for c in expr_str):
                            session.pop('_flashes', None)
                            flash("Only +,-,*,() are allowed. Please consult the Usage Guide.", "error")
                        elif any(l not in session_obj.set for l in var):
                            session.pop('_flashes', None)
                            flash("Label(s) in the expression doesn't exist. Please try again.", "error")
                        else:
                            expr_str = expr.toString()
                            expr_obj = expr.toString()
                            # print(expr_str)
                            for i in var:
                                curr_int = session_obj.set[i]
                                expr_str = re.sub(r'\b'+i+r'\b', curr_int['set_id'], expr_str) # translates labels to ids
                                enc_str  = 'FHE_Integer.FHE_Integer_Enc(' +  str(curr_int['x_prime']) + ',' + str(curr_int['q']) + ',' +  str(fhe_obj.m) + ',' + str(fhe_obj.p) + ')'
                                expr_obj = re.sub(r'\b'+i+r'\b', enc_str, expr_obj)
                            server_eval_id = apis.create_eval(expr.toString())
                            session_obj.set[dataEval.data_label_eval.data] = {"x_prime": None,
                                                                              "q": eval(expr_obj).q,
                                                                              "set_id": server_eval_id}
                            session.pop('_flashes', None)
                            flash("Expression created", "success")
                except Exception as e:
                    print(e)
                    session.pop('_flashes', None)
                    flash("Illegal expression. Please consult the Usage Guide.", "error")

                session['session_obj'] = jsonpickle.encode(session_obj)
                session['fhe_obj'] = jsonpickle.encode(fhe_obj)
                return redirect(url_for('on_session', page=page))

        elif dataEval.submit_eval.data and dataEval.validate_on_submit() == False:
            session.pop('_flashes', None)
            flash("Invalid Label (AlphaDash) or Expression. Please try again.", "error")

        if dataDecrypt.validate_on_submit():
            session_obj = jsonpickle.decode(session['session_obj'])
            fhe_obj = jsonpickle.decode(session['fhe_obj'])

            if dataDecrypt.data_label_decrypt.data not in session_obj.set:
                session.pop('_flashes', None)
                flash("Label does not exist in this session. Use another label.", "error")

            else:
                int_obj = session_obj.set[dataDecrypt.data_label_decrypt.data]
                server_id = int_obj['set_id']
                x_prime = apis.decrypt(server_id)
                q = int_obj['q']
                # TODO ... overlay window for decrypt
                session['decrypted'] = [dataDecrypt.data_label_decrypt.data, fhe_obj.decrypt_int(x_prime, q)]
                session.pop('_flashes', None)
                flash("Decrypted", "success")

            session['session_obj'] = jsonpickle.encode(session_obj)
            session['fhe_obj'] = jsonpickle.encode(fhe_obj)
            return redirect(url_for('on_session', page=page))


        elif dataDecrypt.submit_decrypt.data and dataDecrypt.validate_on_submit() == False:
            session.pop('_flashes', None)
            flash("Invalid Label (AlphaDash). Please try again.", "error")


    return render_template('session.html', page=page, dataEntry_int=dataEntry_int, dataEntry_poly=dataEntry_poly, dataEval=dataEval, dataDecrypt=dataDecrypt)
