import pyautogui
import requests
import threading
import math
import json

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
        # avoid bug where hangs at 0 seconds
        if progress == 0:
            pyautogui.press('playpause')
            pyautogui.press('playpause')

        time_until_5 = math.ceil(5500 - progress)
        
        if time_until_5 <= 0:
            pyautogui.press('nexttrack')
            print('ad skipped!')
        else:
            t = threading.Timer(math.ceil(time_until_5 / 1000), skipper, [token])
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
