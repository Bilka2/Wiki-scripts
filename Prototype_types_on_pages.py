import requests
import json
import re
from util import get_edit_token, edit_page, get_page

with open('prototype-types.json', 'r') as f:
  pageToTypeMapping = json.load(f)

api_url = 'https://wiki.factorio.com/api.php'

def main():
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)
  for page, type in pageToTypeMapping.items():
    try:
      pageData = get_page(session, api_url, page)
      if "Basics" in pageData or "basics" in pageData:
        replacement = r"\1Prototype type: '''" + type + "'''\n\n"
        if type == "<abstract>":
          replacement = r"\1This type is abstract and cannot be created directly.\n\n"
        pattern = re.compile(r"(==\s*Basics\s*==\n)", re.IGNORECASE)
        pageData = re.sub(pattern, replacement, pageData)
        print(edit_page(session, api_url, edit_token, page, pageData, "Added prototype type to page").text)
      else: 
        print(page + " Does not have basics on page")
    except:
      print(page + " Something went wrong")

if __name__ == '__main__':
  main()
