#Main configuration file for the complete flask application

from flask import Config

""" Common config can go here """



class DevelopmentConfig(Config):
    """ Angel API details"""
    CLIENT_ID = 	'136079482590b3aaefd3150b85c3394f'
    CLIENT_SECRET =	'3f3866fbaaa73c59e4f026279dcd0005'

    """MySql configurations"""
    """
    DB_HOST	= 'localhost'
    DB_PORT	= '3306'
    DB_USER	= 'root'
    DB_PASSWORD	= 'vijay02'
    DB_NAME = 'angelapp'
    """

    """
    Started using psycopg2 for postgres db
    """
    
    DB_HOST	= 'ec2-54-225-182-133.compute-1.amazonaws.com'
    DB_PORT	= '5432'
    DB_USER	= 'jbwomvcwpdjdnt'
    DB_PASSWORD	= 'b4cXjBtGSP2vY-PqMCUHbIU_le'
    DB_NAME = 'dbf8eru677d3pb'
    
    """
    DB_HOST	= 'localhost'
    DB_PORT	= '5432'
    DB_USER	= 'vijay'
    DB_PASSWORD	= 'vijay02'
    DB_NAME = 'deep'
    """ 
    
    #SQLALCHEMY_DATABASE_URI = "postgresql://vijay:vijay02@localhost/deep"    
