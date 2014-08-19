from flask import Flask

import os




""" Load the basic config for the application """


s_app = Flask('app')
environment = os.environ.get('prod_env','development')
if environment == 'production':
    s_app.config.from_object('conf.mainconf.ProductionConfig') 
else:
    s_app.config.from_object('conf.mainconf.DevelopmentConfig')
