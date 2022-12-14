from os import getenv
from requests_oauthlib import OAuth2Session
from google.cloud import datastore
import urllib.parse

client_id = getenv('GOOGLE_FIT_CLIENT_ID')
client_secret = getenv('GOOGLE_FIT_CLIENT_SECRET')
host = getenv('GOOGLE_FIT_REDIRECT_HOST')

redirect_uri = f'https://{host}/googlefitauth'
token_url = "https://www.googleapis.com/oauth2/v4/token"
scope = [
    "https://www.googleapis.com/auth/fitness.activity.read",
]

def execute(request):
    url = f"https://localhost/googlefitauth?state=try_sample_request&code=4%2F0ARtbsJrXL9CFg-WynvhXSXel6x4G1UQvrA39BqrT8xrBqsuSU7enPJKs1bLCVryamcHcnQ&scope={urllib.parse.quote_plus(scope[0])}"
    google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    token = google.fetch_token(token_url, client_secret=client_secret, authorization_response=url)

    db = datastore.Client()
    key = db.key('fit_tokens', 'fit_tokens')
    entity = datastore.Entity(key=key)
    entity.update(token)
    db.put(entity)

    return ""