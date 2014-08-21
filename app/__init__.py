from flask import Flask
import os

from angelList.controllers import angelListregister
import app
import MySQLdb
from flask import g


""" Load the basic config for the application
    - Includes the application start
    - Logger setup
    - Environment setup
    - Database setup
"""

s_app = Flask(__name__)
environment = os.environ.get('prod_env','development')

if environment == 'production':
    s_app.config.from_object('conf.mainconf.ProductionConfig') 
else:
    s_app.config.from_object('conf.mainconf.DevelopmentConfig')


    
""" Initiating the logger"""

logger = s_app.logger 
logger.setLevel('DEBUG')



""" Regsitering the blueprints for all the other controllers """
s_app.register_blueprint(angelListregister)


"""Set the app secret to use sessions """
s_app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


""" Initiating the database """

@s_app.before_request
def db_connect():
    g.db = MySQLdb.connect(host=s_app.config['DB_HOST'],
                            user=s_app.config['DB_USER'],
                            passwd=s_app.config['DB_PASSWORD'],
                            db=s_app.config['DB_NAME'])


    
@s_app.teardown_request
def db_disconnect(exception=None):
    g.db.close()
