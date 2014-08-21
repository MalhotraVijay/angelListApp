import app
import json
from models import AngelListModel
from flask import render_template,redirect



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
    if code:
        return json.dumps({'code':code})
    else:
        return render_template('landing.html')
