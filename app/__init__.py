from flask import Flask
import os

from angelList.controllers import angelListregister
import app


""" Load the basic config for the application
    - Includes the application start
    - Logger setup
    - Environment setup

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
print app.s_app

print angelListregister

""" Regsitering the blueprints for all the other controllers """
s_app.register_blueprint(angelListregister)

