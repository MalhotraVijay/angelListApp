"""The AngleList model to store the application information """


import app
import json


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
