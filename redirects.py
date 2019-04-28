import re
import requests
import urllib.parse
from util import get_edit_token, get_allpages, get_backlinks, get_imageusage, edit_page

base_url = 'https://wiki.factorio.com'
api_url = base_url + '/api.php'


class Redirect:
  def __init__(self, title):
    self.title = title
    self.urlencoded_title = urllib.parse.quote(title, safe='/:()')
    self.links_here = 0
    self.eval_links_here()
    
  def eval_links_here(self):
    backlinks = [page['title'] for page in get_backlinks(self.session, api_url, self.title)]
    self.links_here = len(backlinks)
    if not re.search('^File:', self.title, re.IGNORECASE):
      return
    
    imageusage = [page['title'] for page in get_imageusage(self.session, api_url, self.title)]
    for title in imageusage:
      if title not in backlinks:
        self.links_here += 1
    
  def __lt__(self, other):
    return (self.links_here, other.title) > (other.links_here, self.title) #inf-0 (descending) for links_here, a-z (ascending) for title
  
  def __str__(self):
    return f'\n|[{base_url}/index.php?title={self.urlencoded_title}&redirect=no {self.title}]\n|[{base_url}/index.php?title=Special:WhatLinksHere/{self.urlencoded_title} {self.links_here}]'


def main():
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)
  
  redirects = get_allpages(session, api_url, apfilterredir = 'redirects')
  redirects.extend(get_allpages(session, api_url, apfilterredir = 'redirects', apnamespace = '6'))
  
  Redirect.session = session
  redirects = [Redirect(page['title']) for page in redirects]
  redirects.sort()
  
  content = '{|class=wikitable\n!#\n!Redirect\n!Links to this redirect'
  for i, redirect in enumerate(redirects):
    content += f'\n|-\n|{i+1}{redirect}'
  content += '\n|}'
  
  edit_response = edit_page(session, api_url, edit_token, 'Factorio:Redirects', content, 'Updated the list of redirects.')
  return edit_response.text


if __name__ == '__main__':
  print(main())
