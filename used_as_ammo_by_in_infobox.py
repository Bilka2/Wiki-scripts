import requests
import re
from util import get_edit_token, get_page, edit_page

api_url = 'https://wiki.factorio.com/api.php'

def main(used_by, page):
  page = "Infobox:" + page
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)
  page_data = get_page(session, api_url, page)
  infobox_start = page_data.find("|")
  used_by_string = " + ".join(used_by)
  new_page_data = page_data[:infobox_start] + f"|used-as-ammo-by = {used_by_string}\n" + page_data[infobox_start:]
  print(new_page_data)
  print(edit_page(session, api_url, edit_token, page, new_page_data, "Added \"Usable Ammunition For\" to infobox").text)


if __name__ == '__main__':
  main(["Flamethrower turret"], "Light oil")
