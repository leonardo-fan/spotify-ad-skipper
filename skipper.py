import pyautogui
import requests
import threading

def skipper(token):
    req = requests.get("https://api.spotify.com/v1/me/player/currently-playing", params={
        "market": "ES",
    }, headers={
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    })
    if req.status_code != 200:
        print('token invalid')
    
    type = req.json()['currently_playing_type']
    progress = req.json()['progress_ms']

    if type == 'ad':
        time_until_5 = 5000 - progress
        
        if time_until_5 <= 0:
            pyautogui.keyDown('nexttrack')
            pyautogui.keyUp('nexttrack')
            print('ad skipped!')
        else:
            t = threading.Timer(time_until_5 / 1000, skipper, [token])
            t.start()
        
        req = requests.get("https://api.spotify.com/v1/me/player/currently-playing", params={
            "market": "ES",
        }, headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        })
        if req.status_code != 200:
            print('token invalid during ad')
    
        type = req.json()['currently_playing_type']
        progress = req.json()['progress_ms']
