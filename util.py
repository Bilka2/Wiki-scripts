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

def get_page(session, api_url, title):
  page_info = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'assert': 'user',
    'titles': title,
    'prop': 'revisions',
    'rvprop': 'content'
  })
  page = page_info.json()['query']['pages']
  revisions = list(page.values())[0]['revisions'][0]
  content = list(revisions.values())[2]
  return content
  
def edit_page(session, api_url, edit_token, title, text, summary):
  edit_response = session.post(api_url, data={
    'format': 'json',
    'action': 'edit',
    'assert': 'user',
    'text': text,
    'summary': summary,
    'title': title,
    'bot': True,
    'token': edit_token,
  })
  return edit_response
