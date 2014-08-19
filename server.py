#!/usr/bin/env python

from app import s_app
s_app.run(host='0.0.0.0', debug=True, port=6468, threaded=True)  # Start the server
