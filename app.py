import os
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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug="true")
