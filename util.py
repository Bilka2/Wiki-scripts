import base64
import json
import os.path
import requests

with open(os.path.dirname(__file__) + '/bot-credentials.json', 'r') as f:
  credentials = json.load(f)
username = credentials['username']
password = base64.b64decode(credentials['password']).decode('utf-8')


def normalize_pagename(pagename):
  return pagename.replace(' ', '_')

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


def get_page_safe(session, api_url, title):
  page_info = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'assert': 'user',
    'titles': title,
    'prop': 'revisions',
    'rvprop': 'content'
  })
  page = page_info.json()['query']['pages']
  if 'revisions' in list(page.values())[0]:
    revisions = list(page.values())[0]['revisions'][0]
    content = list(revisions.values())[2]
    return content
  return ''


def edit_page(session, api_url, edit_token, title, text, summary, prepend = False): # can also create pages
  data={
    'format': 'json',
    'action': 'edit',
    'assert': 'user',
    'summary': summary,
    'title': title,
    'bot': True,
    'token': edit_token,
  }
  if prepend:
    data['prependtext'] = text
  else:
    data['text'] = text
  
  return session.post(api_url, data=data)


def get_allpages(session, api_url, aplimit = '5000', apfilterredir = 'all', apnamespace = '0'):
  allpages = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'assert': 'user',
    'list': 'allpages',
    'aplimit': aplimit,
    'apfilterredir': apfilterredir,
    'apnamespace' : apnamespace
  })
  return allpages.json()['query']['allpages']


def get_backlinks(session, api_url, bltitle, bllimit = '1000', blfilterredir = 'all'):
  backlinks = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'assert': 'user',
    'list': 'backlinks',
    'bltitle': bltitle,
    'bllimit': bllimit,
    'blfilterredir' : blfilterredir
  })
  return backlinks.json()['query']['backlinks']


def get_imageusage(session, api_url, iutitle, iulimit = '1000', iufilterredir = 'all'):
  imageusage = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'assert': 'user',
    'list': 'imageusage',
    'iutitle': iutitle,
    'iulimit': iulimit,
    'iufilterredir' : iufilterredir
  })
  return imageusage.json()['query']['imageusage']


def get_wantedpages(session, api_url, qpoffset = '0', qplimit = '5000'):
  wantedpages = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'assert': 'user',
    'list': 'querypage',
    'qppage': 'Wantedpages',
    'qplimit': qplimit,
    'qpoffset': qpoffset
  })
  return wantedpages.json()['query']['querypage']['results']


def get_page_info(session, api_url, title):
  response = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'assert': 'user',
    'titles': title,
    'prop': 'info'
  })
  pages = response.json()['query']['pages']
  page_info = list(pages.values())[0]
  return page_info


def get_categorymembers(session, api_url, cmtitle, cmlimit = '400'):
  categorymembers = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'assert': 'user',
    'list': 'categorymembers',
    'cmtitle': cmtitle,
    'cmlimit': cmlimit,
    'cmprop' : 'title'
  })
  return categorymembers.json()['query']['categorymembers']

  
def get_user_groups(session, api_url):
  user_groups = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'assert': 'user',
    'meta': 'userinfo',
    'uiprop': 'groups'
  })
  return user_groups.json()['query']['userinfo']['groups']


def upload_file(session, api_url, edit_token, filename, file, text):
  data = {
    'format': 'json',
    'action': 'upload',
    'assert': 'user',
    'text': text,
    'filename': filename, # no File: prefix
    'text': text,
    'token': edit_token,
    'ignorewarnings': True
  }
    
  response = session.post(api_url, files = {'file': (filename, file)}, data=data)
  return response


def update_file(session, api_url, edit_token, filename, file):
  data = {
    'format': 'json',
    'action': 'upload',
    'assert': 'user',
    'filename': filename, # no File: prefix
    'token': edit_token
  }
  response = session.post(api_url, files = {'file': (filename, file)}, data=data)
  # file already exists and there are no other errors - the expected response
  if response.json()['upload']['result'] == 'Warning' and ('exists' in response.json()['upload']['warnings']) and response.json()['upload']['warnings']['exists'] == normalize_pagename(filename) and len(response.json()['upload']['warnings']) == 1:
    data['ignorewarnings'] = True
    data['filekey'] = response.json()['upload']['filekey']
    response = session.post(api_url, data=data)
  elif response.json()['upload']['result'] == 'Warning':
    print('Could not upload file ' + filename)
    print(response.json()['upload']['warnings'])
    
  return response


def move_page(session, api_url, edit_token, frm, to, summary, redirect = True):
  data = {
    'format': 'json',
    'action': 'move',
    'assert': 'user',
    'from': frm,
    'to': to,
    'reason': summary,
    'token': edit_token,
    'movetalk': True,
    'ignorewarnings': True
  }
  if not redirect:
    data['noredirect'] = True

  return session.post(api_url, data=data)
  
  
def protect_page(session, api_url, edit_token, title, summary):
  data = {
    'format': 'json',
    'action': 'protect',
    'assert': 'user',
    'title': title,
    'protections': 'edit=sysop|move=sysop',
    'reason': summary,
    'expiry': 'infinite',
    'token': edit_token
  }

  return session.post(api_url, data=data)


class DictUtil:
  @staticmethod
  def get_optional_list(dict, key):
    return dict.get(key, [])
  
  @staticmethod
  def get_optional_string(dict, key):
    return dict.get(key, "")
  
  @staticmethod
  def get_optional_number(dict, key):
    return dict.get(key, 0)
    
  @staticmethod
  def get_optional_dict(dict, key):
    return dict.get(key, {})
