import requests
from util import get_edit_token, api_url

with open('C:\\Users\\Erik\\Documents\\Factorio\\prototype_types_the_game_will_respond_to.txt', 'r') as f:
   data = list(f)

session = requests.Session()
edit_token = get_edit_token(session)

page_info = session.get(api_url, params={ #target page
  'format': 'json',
  'action': 'query',
  'assert': 'user',
  'titles': 'Prototype definitions',
  'prop': 'revisions',
  'rvprop': 'content'
})
page = page_info.json()['query']['pages']
revisions = list(page.values())[0]['revisions'][0]
content = list(revisions.values())[2]

for line in data:
  if not ('\'\'\'' + line.strip() + '\'\'\'' in content):
    print(line.strip())

