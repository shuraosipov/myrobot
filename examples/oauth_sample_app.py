import os
from requests_oauthlib import OAuth2Session
import jwt
import requests
import json




def list_google_calendars(url, access_token) -> list:
    """
    Get List of calendars from Google Calendar API using the access token from the user.
    """
    
    headers = { "Authorization": f"Bearer {access_token}" }
    
    response = requests.get(url, headers=headers)
    
    return [calendar for calendar in json.loads(response.text)["items"]]


client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
redirect_uri = "https://oauth.pstmn.io/v1/browser-callback"
authz_endpoint = "https://shuraosipov.auth.us-east-1.amazoncognito.com/oauth2/authorize"
token_endpoint = "https://shuraosipov.auth.us-east-1.amazoncognito.com/oauth2/token"
resource_url = "https://www.googleapis.com/calendar/v3/users/me/calendarList"


scope = ["https://www.googleapis.com/auth/calendar.readonly", "email", "openid", "profile"]
oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)


authorization_url, state = oauth.authorization_url(authz_endpoint)
print("\n")
print("Please go to %s and authorize access." % authorization_url)
print("\n")
authorization_response = input("Enter the full callback url: ")
print("\n")

# Fetch an access token from the provider using the authorization code obtained during user authorization.
token = oauth.fetch_token(
    token_endpoint,
    authorization_response=authorization_response,
    client_secret=client_secret,
)

def decode_id_token(encoded_id_token) -> dict:
    return jwt.decode(
        encoded_id_token, 
        algorithms=["RS256"], 
        options={"verify_signature": False}
    )

def extract_attributes_from_id_token(decoded_id_token) -> dict:
    return {
        "email": decoded_id_token.get("email"),:
        "username": decoded_id_token.get("cognito:username"),
        "first_name": decoded_id_token.get("given_name"),
        "last_name": decoded_id_token.get("family_name"),
        "google_access_token": decoded_id_token.get("custom:google_access_token"),
    }
id_token = extract_attributes_from_id_token(decode_id_token(token["id_token"]))
google_access_token = id_token['google_access_token']
print(list_google_calendars(resource_url, google_access_token))


