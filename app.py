import os
import get_contributions
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main_page():
    """Respond to incoming requests."""
    return render_template('index.html')

@app.route('/session', methods=['POST', 'GET'])
def session():
    """Responds to session view requests"""
    session_id = request.form['session_id']
    user_dict = db_utils.get_user_dict_by_session_id(session_id)
    users = user_dict.keys()
    contributions = session_functions.get_public_contributions(users)
    for user in users:
        # Figure out how many contributions since the beginning of the competition.
        user_dict[user] = contributions - user_dict[user]
    return render_template('session.html', session_id=session_id, user_dict=user_dict)

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

@app.route('/join', methods=['POST'])
def join_session():
    user = request.form['user']
    contributions = get_contributions.get_public_contributions([user])
    user_dict = db_utils.get_user_dict_by_session_id(session_id)
    user_dict[user] = contributions
    db_utils.update_user_dict(session_id, user_dict)
    return render_template('session.html', session_id=session_id, user_dict=user_dict)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug="true")
