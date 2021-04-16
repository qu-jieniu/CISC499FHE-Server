from app import *

@app.route('/usage', methods=['GET', 'POST'])
def usage():
    session['label_list'] = []
    return jsonify({'msg': 'hello'})
