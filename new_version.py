import requests
import re
from util import get_edit_token, api_url

page_name = 'Main_Page/Latest_versions'

def main(forum_post_number, version):
  session = requests.Session()
  edit_token = get_edit_token(session)
  
  page_info = session.get(api_url, params={ #target page
    'format': 'json',
    'action': 'query',
    'assert': 'user',
    'titles': page_name,
    'prop': 'revisions',
    'rvprop': 'content'
  })
  page = page_info.json()['query']['pages']
  revisions = list(page.values())[0]['revisions'][0]
  content = list(revisions.values())[2]
  
  #TODO: https://wiki.factorio.com/Template:VersionNav
  
  if version in content:
    return f'Version {version} already found on page. Aborting.'
  
  new_content = re.sub(r'({{Translation\|Latest experimental version}}: \[https:\/\/forums\.factorio\.com\/)\d+ \d\.\d+\.\d+', rf'\g<1>{forum_post_number} {version}', content)
  
  edit_response = session.post(api_url, data={
    'format': 'json',
    'action': 'edit',
    'assert': 'user',
    'text': new_content,
    'summary': 'New FFF',
    'title': page_name,
    'bot': True,
    'token': edit_token,
  })
  
  return edit_response.text
  