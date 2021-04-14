from app import *

@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html',
                           page='About')
