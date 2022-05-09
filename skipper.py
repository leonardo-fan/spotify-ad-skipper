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
        return

    try:
        type = req.json()['currently_playing_type']
        progress = req.json()['progress_ms']
    except KeyError:
        print('wrong data format returned')
        print(json.dumps(req.json(), indent=4))
        return

    if type == 'ad':
        # avoid bug where hangs at 0 seconds
        if progress == 0:
            pyautogui.press('playpause')
            pyautogui.press('playpause')

        time_until_5 = 5500 - progress
        
        if time_until_5 <= 0:
            pyautogui.press('nexttrack')
            print('ad skipped!')
        else:
            time_until_5 = round(time_until_5, -3)
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
            return
    
        type = req.json()['currently_playing_type']
        progress = req.json()['progress_ms']
