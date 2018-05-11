import requests
import json
import base64
import os.path

with open(os.path.dirname(__file__) + '/bot-credentials.json', 'r') as f:
  credentials = json.load(f)

username = credentials['username']
password = base64.b64decode(credentials['password']).decode('utf-8')
api_url = 'https://wiki.factorio.com/api.php'

def get_edit_token(session):
  #get login token
  login_token = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'meta': 'tokens',
    'type': 'login',
  })
  login_token.raise_for_status()
  
  #log in
  login = session.post(api_url, data={
    'format': 'json',
    'action': 'login',
    'lgname': username,
    'lgpassword': password,
    'lgtoken': login_token.json()['query']['tokens']['logintoken'],
  })
  if login.json()['login']['result'] != 'Success':
    raise RuntimeError(login.json()['login']['reason'])
  
  #get edit token
  edit_token = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'meta': 'tokens',
  })
  
  return edit_token.json()['query']['tokens']['csrftoken']
