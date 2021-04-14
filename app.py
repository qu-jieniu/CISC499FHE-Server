''' BEGIN CONFIG '''
from externalLib import *

app = Flask(__name__,
            template_folder='template',
            static_folder='static'
)

app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
    SECRET_KEY='CISC499-FHE-Client-Key'
)


from views.about import *
from views.database_connect import *
from views.database_login import *
from views.database_session import *
from views.usage import *


# if __name__ == "__main__":
    # app.run()
    # FlaskUI(app).run()
