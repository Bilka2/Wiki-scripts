import requests
from util import get_edit_token, get_page

api_url = 'https://wiki.factorio.com/api.php'

with open('C:\\Users\\Erik\\Documents\\Factorio\\prototype_types_the_game_will_respond_to.txt', 'r') as f:
   data = list(f)

session = requests.Session()
edit_token = get_edit_token(session, api_url)

content = get_page(session, api_url, 'Prototype definitions')

for line in data:
  if not ('\'\'\'' + line.strip() + '\'\'\'' in content):
    print(line.strip())
