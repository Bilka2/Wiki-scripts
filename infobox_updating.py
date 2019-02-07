''' Class structure:

Classes for properties:
  __str__(self):
    The __str__ method of each property has to result in a string that can be parsed by Template:Infobox.
    The string contains all important info saved in the class.
    Note: This can be different from a string that can be parsed as plain wikitext!
  
  get_data_string(self):
    Each property must have a get_data_string method which returns the data as a string that can be parsed by Template:Infobox when placed behind a property name.
   
  IconWithCaption:
    desc: Abstract container for the information required to generate the wikitext or infobox syntax for an icon. Mandatory file name, optional caption

Classes for infoboxes:
  get_all_properties(self):
    Every infobox class must have this property. It returns a list of all members of the class, excluding "name"
'''

import re
import requests
import json
import os.path
from util import get_edit_token, get_page_safe, edit_page

no_infobox = ["Basic oil processing", "Advanced oil processing", "Coal liquefaction", "Empty barrel", "Heavy oil cracking", "Light oil cracking", "Solid fuel from heavy oil", "Solid fuel from light oil", "Solid fuel from petroleum gas", "Water barrel", "Crude oil barrel", "Heavy oil barrel", "Sulfuric acid barrel", "Light oil barrel", "Petroleum gas barrel", "Lubricant barrel", "Empty crude oil barrel", "Empty heavy oil barrel", "Empty light oil barrel", "Empty lubricant barrel", "Empty petroleum gas barrel", "Empty sulfuric acid barrel", "Empty water barrel", "Fill crude oil barrel", "Fill heavy oil barrel", "Fill light oil barrel", "Fill lubricant barrel", "Fill petroleum gas barrel", "Fill sulfuric acid barrel", "Fill water barrel"]
current_version = "0.16.51"
api_url = 'https://testing-wiki.factorio.com/api.php'
re_start_of_infobox = re.compile('{{infobox', re.I)

class Entity:
  def __init__(self, name, data):
    self.name = name
    self.health = Number('health', data['health'])
    
  def get_all_properties(self):
    return [self.health]
    
    
class Technology:    
  def __init__(self, name, data):
    self.name = name + ' (research)'
    self.cost_multiplier = Number('cost-multiplier', data['cost-multiplier'])
    self.expensive_cost_multiplier = Number('expensive-cost-multiplier', data['expensive-cost-multiplier'])
    self.cost = IconWithCaptionList('cost', data['cost'])
    self.allows = IconWithCaptionList_from_list_of_strings('allows', get_optional_list(data, 'allows')) # the technologies that are unlocked by this technology
    self.effects = IconWithCaptionList_from_list_of_strings('effects', get_optional_list(data, 'effects')) # the recipes that are unlocked by this technology
    self.required_technologies =  IconWithCaptionList_from_list_of_strings('required-technologies', get_optional_list(data, 'required-technologies')) #the technologies that are must be researched before this technology can be researched
    # HACK
    if self.name == 'Mining productivity (research)':
      self.allows.list[0].caption = '2-&infin;'
  
  def get_all_properties(self):
    return [self.cost_multiplier, self.expensive_cost_multiplier, self.cost, self.allows, self.effects, self.required_technologies]


class InfoboxProperty:
  def __str__(self):
    return f'|{self.name} = {self.get_data_string()}'


class Number(InfoboxProperty):
  def __init__(self, name, number):
    self.name = name
    self.number = number
    
  def get_data_string(self):
    return str(self.number)


class IconWithCaptionList(InfoboxProperty):
  def __init__(self, name, data):
    self.name = name
    self.list = [IconWithCaption(icon) for icon in data]
    
  def get_data_string(self):
    return ' + '.join([str(icon) for icon in self.list])


class IconWithCaption:
  def __init__(self, data):
    self.file_name = data[0]
    self.caption = data[1] if len(data) == 2 else ""
    
  def __str__(self):
    if self.caption:
      return f'{self.file_name}, {self.caption}'
    else:
      return f'{self.file_name}'


def IconWithCaptionList_from_list_of_strings(name, list):
  return IconWithCaptionList(name, [string.split(', ') for string in list])


def get_optional_list(dict, key):
  return dict[key] if key in dict else []


def update_infoboxes():
  #update_infobox('entities-health', Entity)
  update_infobox('technologies', Technology)
  
    
def update_infobox(file_name, klass):
  with open(os.path.dirname(os.path.abspath(__file__)) + f'/data/{current_version}/wiki-{file_name}-{current_version}.json', 'r') as f:
    file = json.load(f)
    
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)
  
  for name, data in file.items():
    if name in no_infobox:
      continue
    infobox_data = klass(name, data)
    page_name = 'Infobox:' + infobox_data.name
    page = get_page_safe(session, api_url, page_name)
    if not page: # TODO
      print(f'Page for {infobox_data.name} does not exit')
      continue
    new_page = page
    summary = ''
    
    for property in infobox_data.get_all_properties():     
      new_page, summary = update_property(property, new_page, summary)
      
    if page != new_page:
      print(new_page + '      ' + summary)
      # print(edit_page(session, api_url, edit_token, page_name, new_page, summary).text)
    else:
      print(f'{infobox_data.name} was not changed.')


def update_property(property, page, summary):
  on_page = re.search(r'(\|\s*' + property.name + r'\s*=\s*(.+))\n*(\||}})', page)
  if on_page:
    if not property.get_data_string(): # our property is empty and should be removed from the page
      page = page[:on_page.start()] + on_page.group(3) + page[on_page.end():]
      summary += 'Removed ' + property.name + '. '
    elif on_page.group(2) == property.get_data_string(): #our page contains exactly what we want
      return page, summary
    else: # replace data that is on the page
      page = page[:on_page.start()] + str(property) + page[on_page.start() + len(on_page.group(1)):]
      summary += 'Updated ' + property.name + f' to {current_version}. '
  elif property.get_data_string(): # add data to page (if there is any to add)
    page = re.sub(re_start_of_infobox, r'\g<0>\n' + str(property), page)
    summary += 'Added ' + property.name + '. '
  
  return page, summary
    
if __name__ == '__main__':
  update_infoboxes()
