import requests
import json
import base64
import os.path

with open(os.path.dirname(__file__) + '/bot-credentials.json', 'r') as f:
  credentials = json.load(f)

username = credentials['username']
password = base64.b64decode(credentials['password']).decode('utf-8')

def get_edit_token(session, api_url):
  login_token = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'meta': 'tokens',
    'type': 'login',
  })
  login_token.raise_for_status()
  
  login = session.post(api_url, data={
    'format': 'json',
    'action': 'login',
    'lgname': username,
    'lgpassword': password,
    'lgtoken': login_token.json()['query']['tokens']['logintoken'],
  })
  if login.json()['login']['result'] != 'Success':
    raise RuntimeError(login.json()['login']['reason'])
  
  edit_token = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'meta': 'tokens',
  })
  
  return edit_token.json()['query']['tokens']['csrftoken']
