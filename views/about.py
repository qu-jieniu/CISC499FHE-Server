from app import *

@app.route('/', methods=['GET', 'POST', 'DELETE'])
@app.route('/about')
def about():

    session['label_list'] = []
    
    return render_template('about.html',
                           page='About')
