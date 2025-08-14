from flask import Flask, redirect, request, render_template, url_for
from dotenv import load_dotenv
import requests
import os

# Load .env one folder up
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path=env_path)

# Important Variables. Probably don't touch them..
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:8080/callback'
SCOPES = 'chat:read chat:edit'

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return redirect(
        f"https://id.twitch.tv/oauth2/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPES}"
    )

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return 'No code provided', 400

    token_url = 'https://id.twitch.tv/oauth2/token'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
    }

    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        return f"Error getting token: {response.text}", 500

    token_info = response.json()
    access_token = token_info.get('access_token')
    refresh_token = token_info.get('refresh_token')

    update_env({
        'OAUTH_ID': f'oauth:{access_token}',
        'TWITCH_REFRESH_TOKEN': refresh_token
    }, env_path)

    return render_template('callback.html', access_token=access_token, refresh_token=refresh_token)

def update_env(new_values, env_path):
    if not os.path.exists(env_path):
        with open(env_path, 'w') as f:
            for key, value in new_values.items():
                f.write(f'{key}={value}\n')
        return

    with open(env_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    keys_written = set()
    with open(env_path, 'w', encoding='utf-8') as file:
        for line in lines:
            key = line.split('=')[0]
            if key in new_values:
                file.write(f"{key}={new_values[key]}\n")
                keys_written.add(key)
            else:
                file.write(line)
        for key, value in new_values.items():
            if key not in keys_written:
                file.write(f"{key}={value}\n")

if __name__ == '__main__':
    app.run(port=8080, debug=True)
