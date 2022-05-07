# Skipper - An Automatic Spotify Ad Skipper
Uses the Spotify API with OAuth 2.0 to skip Spotify ads for a user on a computer through a local server. This was a one-night project I made because I got tired of manually skipping ads after 5 seconds and didn't want to pay for Spotify Premium haha.

# Set-up
## Spotify App Set-up
### Get Client ID and Secret
1. Follow the guide here to create a Spotify App: https://developer.spotify.com/documentation/general/guides/authorization/app-settings/
- Choose a related App Name and App Description e.g. Name: Skipper, Description: Skips Ads
- Record your Client ID and Client Secret![image](https://user-images.githubusercontent.com/90736577/167228842-282bb79f-7578-40ac-8418-a0dccd94a68b.png)
- For App Settings, only Redirect URIs are required:
  - Add http://localhost:8080/callback to the URI list (8080 can be switched out for any other port number if in use)

## Dependencies
1. pip install dependencies for the project
```
pip install -r requirements.txt
```

## Configurations
### Create constants.py file in root directory
1. Add the below to constants.py
```
CLIENT_ID='{your Spotify App Client ID}'
CLIENT_SECRET='{your Spotify App Client Secret}'
REDIRECT_URI='http://localhost:{your port}'
```

# Using the Server
1. Run the server
  ```
  python3 server.py
  ```
2. A browser window should pop up, sign in to your Spotify Account and allow access
3. Now your Spotify Ads should be getting skipped after 5 seconds :)
4. Ctrl+C the server when you are finished
