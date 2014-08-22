""" Register Blue Print for Gunicorn """

print "It will Import this"

from app import s_app
import controllers as c


""" Register BluePrint here"""
s_app.register_blueprint(c.angelListregister)
