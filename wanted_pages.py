from collections import defaultdict
import re
import requests
import urllib.parse
from util import get_edit_token, get_categorymembers, get_wantedpages, get_page_info, edit_page

base_url = 'https://wiki.factorio.com'
api_url = base_url + '/api.php'


class WantedPage:

  stubs = []
  archived = []
  disambigs = []
  valid_lang_suffixes = ['cs', 'de', 'es', 'fr', 'it', 'ja', 'nl', 'pl', 'pt-br', 'ru', 'sv', 'uk', 'zh', 'tr', 'ko', 'ms', 'da', 'hu', 'vi', 'pt-pt', 'zh-tw']
  enPageCache = defaultdict(str)
  #possible_locations = ['template', 'file', 'other'].extend(self.valid_lang_suffixes)
  
  
  def __init__(self, title, links_here):
    self.title = title
    self.urlencoded_title = urllib.parse.quote(title, safe='/:()')
    self.links_here = int(links_here)
    self.location = ''
    self.eval_location()
    self.en_page_title = ''
    self.en_page_info = ''
    self.eval_en_page()
  
  
  def eval_location(self):
    has_lang_suffix = re.search('^.+/([^/\s]+)$', self.title)
    if has_lang_suffix and has_lang_suffix.group(1) in self.valid_lang_suffixes:
      self.location = has_lang_suffix.group(1)
      return
    if 'Template:' in self.title:
      self.location = 'template'
      return
    if 'File:' in self.title:
      self.location = 'file'
      return
    self.location = 'other'
  
  
  def eval_en_page(self):
    if self.location not in self.valid_lang_suffixes:
      return
    self.en_page_title = self.title[: -len(self.location)-1]
    if self.enPageCache[self.en_page_title]:
      self.en_page_info = self.enPageCache[self.en_page_title]
      return
    page_info = get_page_info(self.session, api_url, self.en_page_title)
    if 'missing' in page_info:
      self.en_page_info = '---'
      self.enPageCache[self.en_page_title] = self.en_page_info
      return
    self.en_page_info = str(page_info['length'])
    if 'redirect' in page_info:
      self.en_page_info += ' (Redirect)'
      self.enPageCache[self.en_page_title] = self.en_page_info
      return
    if self.en_page_title in self.stubs:
      self.en_page_info += ' (Stub)'
    if self.en_page_title in self.disambigs:
      self.en_page_info += ' (Disambiguation)'
    if self.en_page_title in self.archived:
      self.en_page_info += ' (Archived)'
    self.enPageCache[self.en_page_title] = self.en_page_info
  
  
  def __lt__(self, other):
    return (self.links_here, other.title) > (other.links_here, self.title) #inf-0 (descending) for links_here, a-z (ascending) for title
  
  
  def __str__(self):
    if self.en_page_title:
      return f'\n|[{base_url}/index.php?title={self.urlencoded_title} {self.title}]\n|[{base_url}/index.php?title=Special:WhatLinksHere/{self.urlencoded_title} {self.links_here}]\n|[{base_url}/index.php?title={urllib.parse.quote(self.en_page_title, safe="/:()")} {self.en_page_info}]'
    return f'\n|[{base_url}/index.php?title={self.urlencoded_title} {self.title}]\n|[{base_url}/index.php?title=Special:WhatLinksHere/{self.urlencoded_title} {self.links_here}]'


def main(testing):
  print('Getting wanted pages')
  
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)
  
  wanted_pages = get_wantedpages(session, api_url, qpoffset = '0')
  wanted_pages.extend(get_wantedpages(session, api_url, qpoffset = '5000'))
  #TODO: Automatically check if this is needed:
  #wanted_pages.extend(get_wantedpages(session, api_url, qpoffset = '10000'))
  print('Converting wanted pages')
  
  WantedPage.stubs = [page['title'] for page in get_categorymembers(session, api_url, 'Category:Stubs')]
  WantedPage.archived = [page['title'] for page in get_categorymembers(session, api_url, 'Category:Archived')]
  WantedPage.disambigs = [page['title'] for page in get_categorymembers(session, api_url, 'Category:Disambiguations')]
  WantedPage.session = session
  
  wanted_pages = [WantedPage(page['title'], page['value']) for page in wanted_pages]
  print('Sorting wanted pages')
  wanted_pages.sort()
  
  print('Separating wanted pages by location')
  wanted_pages_by_location = defaultdict(list)
  for page in wanted_pages:
    wanted_pages_by_location[page.location].append(page)
  
  print('Generating output and editing pages')
  edit_responses = []
  for location, pages in wanted_pages_by_location.items():
    output_array = [f'\n|-\n|{i+1}{page}' for i, page in enumerate(pages)]
    
    if location in WantedPage.valid_lang_suffixes:
      output = 'Number of wanted pages: ' + str(len(output_array)) + '\n{|class=wikitable\n!#\n!Page\n!Links to this page\n!Length of the corresponding English page in bytes' + ''.join(output_array) + '\n|}'
    else:
      output = 'Number of wanted pages: ' + str(len(output_array)) + '\n{|class=wikitable\n!#\n!Page\n!Links to this page' + ''.join(output_array) + '\n|}'
    
    if testing:
      edit_responses.append(output)
    else:
      edit_responses.append(edit_page(session, api_url, edit_token, 'Factorio:Wanted pages/' + location, output, 'Updated the list of wanted pages').text)
    
  return edit_responses

  
if __name__ == '__main__':
  print('\n'.join(main(testing = False)))
