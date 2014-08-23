from app import s_app
import json
from models import AngelListModel, DbConnection
from flask import render_template,redirect,session
import app


from flask import Blueprint, request, g, make_response, current_app

angelListregister = Blueprint('angelList', __name__)



@angelListregister.route('/connect', methods=['GET'])
def ConnectHandler():
    ag = AngelListModel()
    ag.client_id = app.s_app.config['CLIENT_ID']
    app.s_app.logger.info('received the client id as: %s' % ag.client_id)

    auth = ag.getAuthentication(ag.client_id)
    
    if auth['error']:
        app.s_app.logger("Client Id not returned from authenticator")
        return json.dumps(
            {'error':'Client Id not returned'}
            )
    else:
        return redirect(auth['response'])


    
@angelListregister.route('/',methods=['GET','POST'])
def AuthenticationHandler():
    code =  request.args.get('code',None)
    error = request.args.get('error',None)
    error_desc = request.args.get('error_description')
    
    if error:
        return render_template('landing.html', error_desc = 'Authentication failure. Please try again !')

    
    if code:
        ag = AngelListModel()
        ag.client_id = app.s_app.config['CLIENT_ID']
        ag.client_secret = app.s_app.config['CLIENT_SECRET']
        access_token = ag.getAccessToken(ag.client_id,ag.client_secret,code)
        #In case of error
        if access_token == '':
            return render_template(
                'landing.html',
                 error = 'Authorization Failure'
                )

        angelUser = ag.getMe()

        db = DbConnection()

        conn = db.conn

        print conn
        
        x = conn.cursor()

        cursor = x.execute("""
        select * from userTokens where access_token = '%s'
        """ % access_token)

        conn.commit()

        rows = x.fetchall()

        session['userToken'] = access_token
        print rows


        if rows != []:
            app.logger.info('Returning User exists in db !')
        else:
            # Make the entry for the user and save the tokens
            try:
                x.execute("""
                INSERT INTO userTokens
                VALUES (%s,%s,%s,%s)""",(
                    angelUser['id'],
                    angelUser['name'],
                    access_token,
                    json.dumps(angelUser)))
    
                conn.commit()
            except:
                conn.rollback()

        conn.close()
        app.logger.info('Authenticated the user')
        return redirect('/jobs')
    else:
        return render_template('landing.html')



    
@angelListregister.route('/jobs',methods=['GET'])
def jobsHandler():

    print session['userToken']

    '''
    Get user from the db
    Get jobs from the db
    Make an angular algorithm to make search easier and intutive
    let everyone be benifited by the app    '''

    db = DbConnection()
    conn = db.conn
    
    x = conn.cursor()
    try:
        cursor = x.execute("""
        select * from jobs
        """)
        conn.commit()
    except:
        app.logger.info('Error in accessing the DB connection')
    
    allJobs =  x.fetchall()

    #print allJobs
    
    return render_template('jobs.html',allJobs = allJobs)
    
@angelListregister.route('/fetchJobs',methods=['GET'])
def fetchJobsHandler():
    '''For the job handler'''
    ag = AngelListModel()
    ag.storeAllJobsInDB()
    return "success"
