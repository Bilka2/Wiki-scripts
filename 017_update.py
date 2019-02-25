import json
import re
import requests
from util import get_edit_token, get_page, edit_page, upload_file, move_page
from infobox_updating import InfoboxUpdate, InfoboxType

def update(testing=True):
  api_url = 'https://wiki.factorio.com/api.php'
  session = requests.Session()
  edit_token = get_edit_token(session, api_url) 
  with open('C:\\Users\\Win 10\\Documents\\Wiki-data\\moves_and_more.json') as f:
    moves_and_more_data = json.load(f)
  
  
  # move that one really special page - need to update the infobox on the page too + archive the page
  for title in moves_and_more_data['special_move']:
    page = get_page(session, api_url, title)
    page = page.replace('{{:Infobox:Wood}}', '{{:Infobox:Wood (archived)}}')
    if 'Infobox' not in title:
      page = '{{archive}}' + page
    
    edit_page(session, api_url, edit_token, title, page, 'Archived wood (removed in 0.17)')
    
    move_page(session, api_url, edit_token, title, title.replace('Wood', 'Wood (archived)'), 'Archived wood (removed in 0.17)', False) # no redirect
  
  
  # archive pages + files = prepend edit {{archive}} onto them
  for title in moves_and_more_data['archive']:
    edit_page(session, api_url, edit_token, title, '{{archive}}', 'Archived page (removed in 0.17)', True) # prepend edit 
  
  
  # move pages + files - leave redirects - also do infoboxes on the pages
  for move_data in moves_and_more_data['move']:
    if 'Infobox' not in move_data['from'] and 'File' not in move_data['from']:
      page = get_page(session, api_url, title)
      from_title_no_lang_suffix = re.search('([^/]+)(\/\S+)?', move_data['from']).group(1)
      to_title_no_lang_suffix = re.search('([^/]+)(\/\S+)?', move_data['to']).group(1)
      page = page.replace('{{:Infobox:' + from_title_no_lang_suffix + '}}', '{{:Infobox:' + to_title_no_lang_suffix + '}}')
      
      edit_page(session, api_url, edit_token, move_data['from'], page, 'Renamed in 0.17')
      
    move_page(session, api_url, edit_token, move_data['from'], move_data['to'], 'Renamed in 0.17')
  
  
  # upload files
  
  
  #create pages
  with open('C:\\Users\\Win 10\\Documents\\Wiki-data\\new_pages.json') as f:
    create_page_data = json.load(f)
  
  for name, page in create_page_data.items():
    edit_page(session, api_url, edit_token, name, page, 'Added in 0.17')
  
  
  # infobox update
  InfoboxUpdate([InfoboxType.Entity, InfoboxType.Technology, InfoboxType.Item, InfoboxType.Recipe, InfoboxType.Prototype], api_url, '0.17.0', False)
  
  # what about the version history itself??
  # latest version update ??? latest experimental is done outside of this function
    # updating https://wiki.factorio.com/Template:VersionNav
      # page = page.replace('}}\n<noinclude>', '|group10 = {{Translation|0.17}}\n|list10 =\n* {{TransLink|Version history/0.17.0#0.17.0|0.17.0}}\n}}\n<noinclude>')
    # updating https://wiki.factorio.com/Main_Page/Latest_versions
      # page = page.replace('[[File:Space science pack.png|link=]]', '[[File:Automation science pack.png|link=]]')
      # page = page.replace('[[File:Speed module 3.png|link=]]', '[[File:Speed module.png|link=]]')
      # page = page.replace('{{Translation|The wiki is based on version}} [[Version history/0.16.0|0.16]]', '{{Translation|The wiki is based on version}} [[Version history/0.17.0|0.17]]')
  # sitenotice https://wiki.factorio.com/MediaWiki:Sitenotice
  # change/publish misc pages
  # perhaps do some of the "manual" infobox work here?
