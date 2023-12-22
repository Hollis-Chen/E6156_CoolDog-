from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
import json
import os
from authlib.integrations.flask_client import OAuth
from datetime import timedelta

app = Flask(__name__)
app.secret_key = '2j9amMWoGgbhXk3SME49arFB'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
app.debug = True 

CLIENT_ID = "808583469127-vdok1207i7asec52bakknkla2f9rvlr2.apps.googleusercontent.com"
CLIENT_SECRET = "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"
OAUTH_URL =  "http://localhost:5000"
"http://3.210.123.50:5000"
#"http://localhost:5000"
#"http://3.210.123.50.nip.io:5000"

oauth = OAuth(app)
google_sso = oauth.register(
    name='google',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs', 
    client_kwargs={'scope': 'openid email profile'},
    redirect_uri=OAUTH_URL + "/callback"
)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login_sso', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.after_request
def add_security_headers(resp):
    if request.endpoint in ['login_sso', 'callback', 'authorize']:
        resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        resp.headers['Pragma'] = 'no-cache'
        resp.headers['Expires'] = '0'
    return resp

# Store user data in session for demonstration purposes
user_sessions = {}
@app.route('/')
def home():
    if 'user' in session:
        return render_template('base.html')

    # If user is not logged in, show the home page with a login button
    return render_template('home.html')

@app.route('/login_sso')
def login_sso():
    session.pop('user', None)
    nonce = os.urandom(16).hex()  # Generates a random nonce
    session['nonce'] = nonce
    redirect_uri = url_for('authorize', _external=True)
    return google_sso.authorize_redirect(redirect_uri, nonce=nonce, prompt='select_account')

@app.route('/callback')
def authorize():
    token = google_sso.authorize_access_token()
    nonce = session.pop('nonce', None)
    user_info = google_sso.parse_id_token(token, nonce=nonce)
    session['user'] = user_info
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    return redirect(url_for('home'))

@app.route('/reading_group', methods=['GET', 'POST'])
@login_required
def reading_group():
    return render_template('reading_group.html')

@app.route('/my_papers', methods=['GET', 'POST'])
@login_required
def my_papers():
    return render_template('my_papers.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/link_zotero', methods=['GET', 'POST'])
@login_required
def link_zotero():
    if request.method == 'POST':
        # Ensure that we are receiving a JSON payload
        if not request.is_json:
            return jsonify({"error": "Missing JSON in request"}), 415

        data = request.get_json()  # Get JSON data sent with POST request
        zotero_user_id = data.get('userId')
        zotero_api_key = data.get('apiKey')

        if not zotero_user_id or not zotero_api_key:
            return jsonify({"error": "Missing Zotero user ID or API key"}), 400
        
        session['zotero_user_id'] = zotero_user_id
        session['zotero_api_key'] = zotero_api_key

        try:
            response = requests.get(f"https://api.zotero.org/users/{zotero_user_id}/items", headers={
                'Authorization': f'Bearer {zotero_api_key}',
                'Content-Type': 'application/json'
            })
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.exceptions.HTTPError as e:
            # Handle any errors that occur during the request to Zotero API
            return jsonify({"error": f"Failed to link Zotero account, status code: {e.response.status_code}"}), e.response.status_code

        return redirect(url_for('import_papers_page'))

    # If it's a GET request, render the form template
    return render_template('link_zotero.html')

@app.route('/import_papers')
@login_required
def import_papers_page():
    return render_template('import_papers.html')


@app.route('/fetch-papers-from-zotero', methods=["GET"])
@login_required
def fetch_papers_from_zotero():
    zotero_user_id = session.get('zotero_user_id')
    zotero_api_key = session.get('zotero_api_key')
    if not zotero_user_id:
        return jsonify({"error": "Zotero user ID not found in session"}), 400

    zotero_url = f"https://api.zotero.org/users/{zotero_user_id}/items"
    
    headers = {
        'Authorization': f'Bearer {zotero_api_key}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(zotero_url, headers=headers)
        
        if response.status_code == 200:
            papers = response.json()
            return jsonify(papers)
        else:
            return jsonify({"error": f"Failed to fetch papers from Zotero, status code: {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Failed to fetch papers from Zotero: {str(e)}"}), 500


# Route for creating a new paper in Zotero
@app.route("/create-paper-in-zotero", methods=["POST"])
@login_required
def create_paper_in_zotero():
    # Implement your POST logic here to create a new paper in Zotero
    # Example: Receive data in request.json and create a new paper
    # Replace this with your actual logic to create a paper

    return jsonify({"message": "Paper created successfully"})

# Route for updating an existing paper in Zotero
@app.route("/update-paper-in-zotero/<paper_id>", methods=["PUT"])
@login_required
def update_paper_in_zotero(paper_id):
    # Implement your PUT logic here to update an existing paper in Zotero
    # Example: Receive data in request.json and update the paper with paper_id
    # Replace this with your actual logic to update a paper

    return jsonify({"message": "Paper updated successfully"})

# Route for deleting a paper in Zotero
@app.route("/delete-paper-in-zotero/<paper_id>", methods=["DELETE"])
@login_required
def delete_paper_in_zotero(paper_id):
    # Implement your DELETE logic here to delete a paper in Zotero
    # Example: Delete the paper with paper_id
    # Replace this with your actual logic to delete a paper

    return jsonify({"message": "Paper deleted successfully"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

