import requests
from requests.auth import HTTPBasicAuth
import webbrowser
from flask import Flask, request
from constants import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from data import DATA_STORE
import threading
from skipper import skipper
from set_interval import setInterval

APP = Flask(__name__)

@APP.route("/info", methods=['GET'])
def get_info():
    return {
        'token': DATA_STORE['token'],
        'refresh_token': DATA_STORE['refresh_token'],
        'expires_in': DATA_STORE['expires_in'],
    }

@APP.route("/", methods=['GET'])
def auth():
    scope = 'user-read-currently-playing'

    reqAuth = requests.get("https://accounts.spotify.com/authorize", params={
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': f'{REDIRECT_URI}/callback',
        'scope': scope
    })
    success = True if reqAuth.status_code == 200 else False
    try:
        webbrowser.open(reqAuth.url, new=1)
    except Exception:
        success = False

    return {
        'success': success
    }

# helper to refresh token after expiry time using a valid refresh token
def timed_refresh(expiry_time):
    def req_refresh():
        resp = refresh_token()
        if not resp['success']: 
            print('error: could not refresh token')
        print('token refreshed!')
    
    if expiry_time > 0:
        refresher = threading.Timer(expiry_time + 0.5, req_refresh)
        refresher.start()

@APP.route("/callback", methods=['GET'])
def set_token():
    # get code from url 
    code = request.args.get('code')
    if code == 'access_denied':
        raise Exception('auth request denied :(')

    # get token
    reqTok = requests.post("https://accounts.spotify.com/api/token", data={
        'code': code,
        'redirect_uri': f'{REDIRECT_URI}/callback',
        'grant_type': 'authorization_code', 
    }, headers={
        'Content-Type': 'application/x-www-form-urlencoded'
    }, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))
    success = True if reqTok.status_code == 200 else False

    try:
        DATA_STORE['token'] = reqTok.json()['access_token']
        DATA_STORE['refresh_token'] = reqTok.json()['refresh_token']
        DATA_STORE['expires_in'] = int(reqTok.json()['expires_in'])
    except KeyError:
        success = False

    timed_refresh(DATA_STORE['expires_in'])

    skipper_start()

    return {
        'success': 'skipper now running, close server to stop' if success else 'failed'
    }

@APP.route("/refresh", methods=['GET'])
def refresh_token():
    refresh_token = DATA_STORE['refresh_token']

    reqTok = requests.post("https://accounts.spotify.com/api/token", data={
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token', 
    }, headers={
        'Content-Type': 'application/x-www-form-urlencoded'
    }, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))
    success = True if reqTok.status_code == 200 else False

    try:
        DATA_STORE['token'] = reqTok.json()['access_token']
        DATA_STORE['expires_in'] = int(reqTok.json()['expires_in'])
    except KeyError:
        success = False

    timed_refresh(DATA_STORE['expires_in'])

    return {
        'success': success
    }

@APP.route("/skipper", methods=['GET'])
def skipper_start():
    token = DATA_STORE['token']

    if not token:
        auth()
        return {
            'message': 'please give access to the skipper'
        }
    
    # call skipper every 5 seconds
    setInterval(5, skipper, token)

    return {
        'message': 'skipper now running, close server to stop'
    }

if __name__ == "__main__":
    APP.run(port=8080) # Do not edit this port
