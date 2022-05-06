import requests
import time
import pyautogui
import webbrowser
import sys
from constants import CLIENT_ID, CLIENT_SECRET


try:  
    while True:
        token = "BQCZsG_g_TPyeRAp61FBWNYzjy0O8UtTy0iZWqQ5_Nb45JdNS_o9pXIftpyL4jR5ea19pQ"
        if len(sys.argv) > 1:
            token = sys.argv[1]

        req = requests.get("https://api.spotify.com/v1/me/player/currently-playing", params={
            "market": "ES",
        }, headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        })
        type = req.json()['currently_playing_type']
        progress = req.json()['progress_ms']

        while type == 'ad':
            print("Ad!")
            print("progress:", progress)
            time_until_5 = 5000 - progress
            print("time until 5 seconds:", time_until_5)
            if time_until_5 <= 0:
                print("instant key press")
                pyautogui.keyDown('nexttrack')
                pyautogui.keyUp('nexttrack')
            else:
                time.sleep(time_until_5 / 1000.0)
                print("wait key press")
                pyautogui.keyDown('nexttrack')
                pyautogui.keyUp('nexttrack')
            
            req = requests.get("https://api.spotify.com/v1/me/player/currently-playing", params={
                "market": "ES",
            }, headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            })
            type = req.json()['currently_playing_type']
            progress = req.json()['progress_ms']
        
        time.sleep(5)
except KeyboardInterrupt:
    print('\nDone\n')
except KeyError:
    print('\nReset token\n')
    webbrowser.open('https://developer.spotify.com/console/get-users-currently-playing-track/?market=&additional_types=', new=2)