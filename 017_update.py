import json
import re
import requests
from util import get_edit_token, get_page, edit_page, upload_file, move_page
from infobox_updating import InfoboxUpdate, InfoboxType

def update():
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
    
    print(edit_page(session, api_url, edit_token, title, page, 'Archived wood (removed in 0.17)').text)
    
    print(move_page(session, api_url, edit_token, title, title.replace('Wood', 'Wood (archived)'), 'Archived wood (removed in 0.17)', False).text) # no redirect
  
  
  # archive pages + files = prepend edit {{archive}} onto them
  for title in moves_and_more_data['archive']:
    print(edit_page(session, api_url, edit_token, title, '{{archive}}', 'Archived page (removed in 0.17)', True).text) # prepend edit 
  
  
  # move pages + files - leave redirects - also do infoboxes on the pages
  for move_data in moves_and_more_data['move']:
    if 'Infobox' not in move_data['from'] and 'File' not in move_data['from']:
      page = get_page(session, api_url, move_data['from'])
      from_title_no_lang_suffix = re.search('([^/]+)(\/\S+)?', move_data['from']).group(1)
      to_title_no_lang_suffix = re.search('([^/]+)(\/\S+)?', move_data['to']).group(1)
      page = page.replace('{{:Infobox:' + from_title_no_lang_suffix + '}}', '{{:Infobox:' + to_title_no_lang_suffix + '}}')
      
      print(edit_page(session, api_url, edit_token, move_data['from'], page, 'Renamed in 0.17').text)
      
    print(move_page(session, api_url, edit_token, move_data['from'], move_data['to'], 'Renamed in 0.17').text)
  
  
  # upload files
  for filename in moves_and_more_data['upload']:
    file = open('C:\\Users\\Win 10\\Documents\\Wiki-data\\icons\\', 'rb')
  
    print(upload_file(session, api_url, edit_token, filename, file, '{{Game image}}').text)
  
  #create pages
  with open('C:\\Users\\Win 10\\Documents\\Wiki-data\\new_pages.json') as f:
    create_page_data = json.load(f)
  
  for name, page in create_page_data.items():
    print(edit_page(session, api_url, edit_token, name, page, 'Added in 0.17').text)
  
  
  # infobox update
  InfoboxUpdate([InfoboxType.Entity, InfoboxType.Technology, InfoboxType.Item, InfoboxType.Recipe, InfoboxType.Prototype], api_url, '0.17.0', False)
  
  
  # updating https://wiki.factorio.com/Template:VersionNav
  versionnav = get_page(session, api_url, 'Template:VersionNav')
  versionnav = versionnav.replace('}}\n<noinclude>', '|group10 = {{Translation|0.17}}\n|list10 =\n* {{TransLink|Version history/0.17.0#0.17.0|0.17.0}}\n}}\n<noinclude>')
  print(edit_page(session, api_url, edit_token, 'Template:VersionNav', versionnav, '0.17').text)
  
  
  # updating https://wiki.factorio.com/Main_Page/Latest_versions
  latest_versions = get_page(session, api_url, 'Main_Page/Latest_versions')
  latest_versions = latest_versions.replace('[[File:Space science pack.png|link=]]', '[[File:Automation science pack.png|link=]]')
  latest_versions = latest_versions.replace('[[File:Speed module 3.png|link=]]', '[[File:Speed module.png|link=]]')
  latest_versions = latest_versions.replace('{{Translation|The wiki is based on version}} [[Version history/0.16.0|0.16]]', '{{Translation|The wiki is based on version}} [[Version history/0.17.0|0.17]]')
  print(edit_page(session, api_url, edit_token, 'Main_Page/Latest_versions', latest_versions, 'Experimental 0.17').text)
  
  
  # sitenotice https://wiki.factorio.com/MediaWiki:Sitenotice
  sitenotice = "'''This wiki is about [[Tutorial:Cheat_sheet#0.17_change_overview|0.17]], the current [[Install_guide#Downloading_and_installing_experimental_versions|experimental version]] of ''Factorio''.'''\n\nInformation about 0.16, the current stable version of ''Factorio'', can be found on [https://stable.wiki.factorio.com/ stable.wiki.factorio.com]."
  print(edit_page(session, api_url, edit_token, 'MediaWiki:Sitenotice', sitenotice, 'Experimental 0.17').text)

  
if __name__ == '__main__':
  update()
