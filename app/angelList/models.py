"""The AngleList model to store the application information """


import app, psycopg2
import json
import hashlib
import urllib, urllib2
from werkzeug.urls import *
from flask import g
from app import s_app



class AngelListModel():
    def __init__(self):
        #oauth credentails
        self.URI_SCHEME = "https"
        self.API_ENDPOINT      = "%s://api.angel.co" % self.URI_SCHEME
        self.OAUTH_ENDPOINT    = "%s://angel.co/api" % self.URI_SCHEME
        self.ACCESS_TOKEN_URL  = "/oauth/token"
        self.AUTHORIZATION_URL = "/oauth/authorize"
        self.client_id = None
        self.client_secret = None
        self.access_token = None
        

    def getAuthentication(self,client_id):
        self.client_id = client_id or self.client_id
        if self.client_id is None:
            app.logger.info("client_id is none. Aborting")
            return {
                'error':'Client Id missing !'
                }
        else:
            return {
                'error':None,
                'response':"%s%s?client_id=%s&response_type=code" % (self.OAUTH_ENDPOINT, self.AUTHORIZATION_URL, self.client_id)
                }



    def getAccessToken(self, client_id = None, client_secret = None, code = None):
        self.client_id = client_id and client_id or self.client_id
        if self.client_id is None:
            app.logger.info("Client Id None")
            return ''

        self.client_secret = client_secret and client_secret or self.client_secret
        if self.client_secret is None:
            app.logger.info("Client Secret None")
            return ''


        if code is None:
            app.logger.info("Code is None")
            return ''
            

        url = "%s%s?client_id=%s&client_secret=%s&code=%s&grant_type=authorization_code" % (self.OAUTH_ENDPOINT, self.ACCESS_TOKEN_URL, self.client_id, self.client_secret, code)

        print url
        
        try:
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
            params = urllib.urlencode({})
            response = urllib2.urlopen(urllib2.Request(url, params, headers))
            json_data = json.loads(response.read())

            access_token = json_data['access_token']
        except:
            # access token failed to fetch (for any reason); so we'll just return blank
            app.logger.info("Something wrong in try")
            access_token = ''

        self.access_token = access_token
        return access_token


    '''
    Helper Methods
    '''
    def doGet(self, url):
      """
      perform a GET request to the supplied url
      """
      response = urllib2.urlopen(url)
      return json.loads(response.read())

    def doPost(self, url, data = None):
      """
      perform a POST request to the supplied url with the given fieldvalues
      """
      headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
      params = urllib.urlencode(data)
      response = urllib2.urlopen(urllib2.Request(url, params, headers))
      return json.loads(response.read())



    """ Application specific Methods """

    # (GET)    https://api.angel.co/1/me
    def getMe(self, access_token = None):
      #self.check_access_token(access_token)
      return self.doGet('%s/1/me?access_token=%s' % (self.API_ENDPOINT, self.access_token))
  
    # GET https://api.angel.co/1/jobs
    def getJobs(self,pageNumber):
        app.logger.info("Called with page Number:" + str(pageNumber))
        return self.doGet('https://api.angel.co/1/jobs?page=' + str(pageNumber)) 


    def storeAllJobsInDB(self):

        db = DbConnection()
        conn = db.conn
        
        x = conn.cursor()


        for i in range(1,12):

            allJobs = self.getJobs(i)

            #print str(allJobs)
        
            try:
                app.logger.info('Trying to save JOb in the db')
                a = x.execute("""
                INSERT INTO jobs
                VALUES (%s,%s)""",(str(i),json.dumps(allJobs)))
                conn.commit()
            except:
                app.logger.info('Exception Occured !')
                conn.rollback()

        conn.close()

        app.logger.info("Completed fetching all the jobs")


    def insertJob(self,jobsDict):

        db = DbConnection()
        conn = db.conn

        app.logger.info("insert Jobs Invoked %s" % json.dumps(jobsDict))
        x = conn.cursor()
        try:
            x.execute("""
                INSERT INTO filterJobs
                VALUES (%s,%s)""",(
                    jobsDict['page'],
                    json.dumps(jobsDict)
                    ))
            conn.commit()
        except:
            app.logger.info('Error in accessing the Job DB connection')

        conn.close()


    def getUser(self,access_token):
        db = DbConnection()
        conn = db.conn
    
        x = conn.cursor()

        try:
            cursor = x.execute("""
            select * from userTokens where access_token = '%s'
            """ % access_token)
            conn.commit()
        except:
            app.logger.info('Error in accessing the userToken DB connection')
    
        currentUser =  x.fetchone() or {}

        conn.close()
        
        return currentUser

    def getAllJobs(self):

        db = DbConnection()
        conn = db.conn
    
        x = conn.cursor()
        try:
            cursor = x.execute("""
            select * from jobs
            """)
            conn.commit()
        except:
            app.logger.info('Error in accessing the Job DB connection')
    
        allJobs =  x.fetchall()

        conn.close()
        return allJobs

    def getAllFilteredJobs(self):

        db = DbConnection()
        conn = db.conn

        app.logger.info("Get Filtered job called")
        x = conn.cursor()
        try:
            cursor = x.execute("""
            select * from filterJobs
            """)
            conn.commit()
        except:
            app.logger.info('Error in accessing the Job DB connection')
    
        allJobs =  x.fetchall()

        conn.close()
        return allJobs


    def filterCurrentJobs(self):
        allJobs = self.getAllJobs()
        
        app.logger.info("FilterJobsInvoked")
        allJobsList = []
        
        for jobPage in allJobs:
            jobsList = []
            jobsDict = { 'page' :jobPage[0]  }
            jobs =  json.loads(jobPage[1])['jobs']
            for oneJob in jobs:
                if ('market' in oneJob['title'].lower() or
                    ('manage' in oneJob['title'].lower()) or
                    ('growth' in oneJob['title'].lower()) or
                    ('business' in oneJob['title'].lower()) or
                    ('operation' in oneJob['title'].lower()) or
                    ('account' in oneJob['title'].lower()) or
                    ('finance' in oneJob['title'].lower()) or
                    ('sale' in oneJob['title'].lower())):
                    jobsList.append(oneJob)
                    
            jobsDict['jobs'] = jobsList
            self.insertJob(jobsDict)
            allJobsList.append(jobsDict)

        return
        
        


class DbConnection():

    def __init__(self):
        conn = psycopg2.connect(
            database=s_app.config['DB_NAME'],
            user = s_app.config['DB_USER'],
            password=s_app.config['DB_PASSWORD'],
            host=s_app.config['DB_HOST'],
            port=s_app.config['DB_PORT'])
        self.conn = conn


    def closeConnection(self):
        self.conn.close()
