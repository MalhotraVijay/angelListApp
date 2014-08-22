#!/usr/bin/env python

from app import s_app
import app.angelList.controllers as c


""" Register BluePrint here"""
s_app.register_blueprint(c.angelListregister)

    
s_app.run(host='0.0.0.0', debug=True, port=6468, threaded=True)  # Start the server
