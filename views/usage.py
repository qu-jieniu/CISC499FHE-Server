from app import *


@app.route('/demo', methods=['GET', 'POST'])
def demo():
    return jsonify({'msg': 'hello'})
