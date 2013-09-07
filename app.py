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
    return render_template('session.html')

@app.route('/create', methods=['POST'])
def create_session():
    """Creates a session, and inserts the data into the database."""
    users = request.form['users']
    contributions = get_contributions.get_public_contributions(users)
    user_dict = session_functions.build_user_dict(users, contributions)
    session_id = session_functions.create_session_id()
    mongoFunctions.insert_into_db(session_id, user_dict)
    return render_template('session.html', session_id=session_id)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug="true")
