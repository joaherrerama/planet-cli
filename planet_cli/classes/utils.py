from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient


def request_token(client_id: str, client_secret: str) -> str:
    auth_url = 'https://services.sentinel-hub.com/auth/realms/main/protocol/openid-connect/token'
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    try:
        token = oauth.fetch_token(token_url=auth_url,
                        client_secret=client_secret, include_client_id=True)
        return token
    except Exception as e:
        raise PermissionError(e)
