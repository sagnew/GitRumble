import os
import get_contributions
#import db_utils
from flask import Flask, render_template, request, redirect, session
from constants import CONSUMER_KEY, CONSUMER_SECRET, APP_SECRET_KEY
import requests


app = Flask(__name__)
app.secret_key = APP_SECRET_KEY

@app.route('/', methods=['POST', 'GET'])
def index():
    """Respond to incoming requests."""
    return render_template('index.html')

@app.route('/session', methods=['POST', 'GET'])
def get_session():
    """Responds to session view requests"""
    session_id = request.form['session_id']
    user_dict = db_utils.get_user_dict_by_session_id(session_id)
    users = user_dict.keys()
    contributions = session_functions.get_public_contributions(users)
    for user in users:
        # Figure out how many contributions since the beginning of the competition.
        user_dict[user] = contributions - user_dict[user]
    return render_template('session.html', session_id=2, user_dict=user_dict)

@app.route('/create', methods=['POST'])
def create_session():
    """Creates a session, and inserts the data into the database."""
    user = request.form['user']
    contributions = get_contributions.get_public_contributions([user])
    user_dict = session_functions.build_user_dict([user], contributions)
    session_id = session_functions.create_session_id()
    payment = request.form['payment']
    session_id = db_utils.insert_into_db(session_id, user_dict, payment)
    return render_template('session.html', session_id=session_id)

@app.route('/token')
def token():
    if session.get('venmo_token'):
        return join_session()
    else:
        return redirect('https://api.venmo.com/oauth/authorize?client_id=%s&scope=make_payments,access_profile&response_type=code' % CONSUMER_KEY)

@app.route('/join', methods=['POST'])
def join_session():
    user = request.form['user']
    contributions = get_contributions.get_public_contributions([user])
    user_dict = db_utils.get_user_dict_by_session_id(session_id)
    user_dict[user] = contributions
    db_utils.update_user_dict(session_id, user_dict)
    return render_template('session.html', session_id=session_id, user_dict=user_dict)

@app.route('/oauth-authorized')
def oauth_authorized():
    AUTHORIZATION_CODE = request.args.get('code')
    data = {
    "client_id":CONSUMER_KEY,
    "client_secret":CONSUMER_SECRET,
    "code":AUTHORIZATION_CODE
    }
    url = "https://api.venmo.com/oauth/access_token"
    response = requests.post(url, data)
    response_dict = response.json()
    app.logger.debug(response_dict)
    access_token = response_dict.get('access_token')
    user = response_dict.get('user')

    session['venmo_token'] = access_token
    session['venmo_username'] = user['username']

    payload = {'access_token': access_token, 'email': 'lindsey.crocker@rutgers.edu', 'note': 'Git Ready to Rumble', 'amount': 1}
    r = requests.post('https://api.venmo.com/payments', params=payload)
    if(r.ok):
        print r.text
        return join_session()
    else:
        return index()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug="true")
