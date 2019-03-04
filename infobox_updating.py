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

import json
import os.path
import re
import requests
from enum import Enum
from util import get_edit_token, get_page_safe, edit_page, DictUtil


class InfoboxType(Enum):
  Entity = 1
  Technology = 2
  Item = 3
  Recipe = 4
  Prototype = 5


class PrototypeInfobox:
  def __init__(self, name, data):
    self.name = name
    self.internal_name = String('internal-name', data['internal-name'])
    self.prototype_type = String('prototype-type', data['prototype-type'])
    
  def get_all_properties(self):
    return [self.internal_name, self.prototype_type]


class EntityInfobox: # also does tile colors
  def __init__(self, name, data):
    self.name = name
    self.health = Number('health', DictUtil.get_optional_number(data, 'health'))
    self.mining_time = Number('mining-time', DictUtil.get_optional_number(data, 'mining-time'))
    self.map_color = MapColor('map-color', DictUtil.get_optional_string(data, 'map-color'))
    
  def get_all_properties(self):
    return [self.health, self.map_color, self.mining_time]
    
    
class TechnologyInfobox:    
  def __init__(self, name, data):
    self.name = name + ' (research)'
    self.cost_multiplier = Number('cost-multiplier', data['cost-multiplier'])
    self.expensive_cost_multiplier = Number('expensive-cost-multiplier', data['expensive-cost-multiplier'])
    self.cost = IconWithCaptionList('cost', data['cost'])
    self.allows = IconWithCaptionList_from_list_of_strings('allows', DictUtil.get_optional_list(data, 'allows')) # the technologies that are unlocked by this technology
    self.effects = IconWithCaptionList_from_list_of_strings('effects', DictUtil.get_optional_list(data, 'effects')) # the recipes that are unlocked by this technology
    self.required_technologies =  IconWithCaptionList_from_list_of_strings('required-technologies', DictUtil.get_optional_list(data, 'required-technologies')) #the technologies that are must be researched before this technology can be researched
    self.internal_name = String('internal-name', data['internal-name'])
    self.prototype_type = String('prototype-type', 'technology')
    self.category = String('category', "Technology")
    
    # HACK
    if self.name == 'Mining productivity (research)':
      self.allows.list[0].caption = '2-&infin;'
  
  def get_all_properties(self):
    return [self.cost_multiplier, self.expensive_cost_multiplier, self.cost, self.allows, self.effects, self.required_technologies, self.internal_name, self.prototype_type, self.category]


class ItemInfobox:
  def __init__(self, name, data):
    self.name = name
    self.consumers = IconWithCaptionList_from_list_of_strings('consumers', DictUtil.get_optional_list(data, 'consumers'))
    self.stack_size = Number('stack-size', data['stack-size'])
    self.req_tech = IconWithCaptionList_from_list_of_strings('required-technologies', DictUtil.get_optional_list(data, 'required-technologies'))
    
  def get_all_properties(self):
    return [self.consumers, self.stack_size, self.req_tech]
    

class RecipeInfobox:
  def __init__(self, name, data):
    self.name = name
    self.recipe = Recipe('recipe', data['recipe'], DictUtil.get_optional_list(data, 'recipe-output'))
    self.total_raw = Recipe('total-raw', data['total-raw'], [])
    self.expensive_recipe = Recipe('expensive-recipe', data['expensive-recipe'], DictUtil.get_optional_list(data, 'expensive-recipe-output'))
    self.expensive_total_raw = Recipe('expensive-total-raw', data['expensive-total-raw'], [])
    self.remove_duplicate_recipes()
  
  def remove_duplicate_recipes(self):
    if self.expensive_total_raw == self.expensive_recipe:
      self.expensive_total_raw.clear()
      print(f'{self.name}: Removed expensive-total-raw because it was a duplicate of expensive-recipe.')
    elif self.expensive_total_raw == self.total_raw:
      self.expensive_total_raw.clear()
      print(f'{self.name}: Removed expensive-total-raw because it was a duplicate of total-raw.')
    if self.expensive_recipe == self.recipe:
      self.expensive_recipe.clear()
      print(f'{self.name}: Removed expensive-recipe because it was a duplicate of recipe.')
    if self.total_raw == self.recipe:
      self.total_raw.clear()
      print(f'{self.name}: Removed total-raw because it was a duplicate of recipe.')
  
  def get_all_properties(self):
    return [self.recipe, self.total_raw, self.expensive_recipe, self.total_raw, self.expensive_total_raw]
  

class Property:
  def __str__(self):
    return f'|{self.name} = {self.get_data_string()}'


class Number(Property):
  def __init__(self, name, number):
    self.name = name
    self.number = number
    
  def get_data_string(self):
    return str(self.number)


class String(Property):
  def __init__(self, name, string):
    self.name = name
    self.string = string
    
  def get_data_string(self):
    return self.string


class MapColor(Property):
  def __init__(self, name, data):
    self.name = name
    self.color = self.convert_to_chart_color(data) if data else data
    
  @staticmethod  
  def convert_to_chart_color(color): # convert from rgb888 to rgb565 to rgb888 (chart uses rgb565)
    return format((int(color, 16) & 0xF8FAF8), '06x')

  def get_data_string(self):
    return self.color

class Recipe(Property):
  def __init__(self, name, ingredients, products):
    self.name = name
    self.ingredients = [IconWithCaption(item) for item in ingredients]
    self.products = [IconWithCaption(item) for item in products]
    
  def get_data_string(self):
    ret = ' + '.join([str(icon) for icon in self.ingredients])
    if self.products:
      ret += ' = ' + ' + '.join([str(icon) for icon in self.products])
    return ret
    
  def __eq__(self, other): # Ignores name
    if self.ingredients != other.ingredients:
      return False
    if (not self.products) or (not other.products): # Only compare products if both have them
      return True
    return self.products == other.products
    
  def clear(self):
    self.ingredients.clear()
    self.products.clear()


class IconWithCaptionList(Property):
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
  
  def __eq__(self, other):
    return self.file_name == other.file_name and self.caption == other.caption


def IconWithCaptionList_from_list_of_strings(name, list):
  return IconWithCaptionList(name, [string.split(', ') for string in list])


class InfoboxUpdate:
  no_infobox = ["Basic oil processing", "Advanced oil processing", "Coal liquefaction", "Empty barrel", "Heavy oil cracking", "Light oil cracking", "Solid fuel from heavy oil", "Solid fuel from light oil", "Solid fuel from petroleum gas", "Water barrel", "Crude oil barrel", "Heavy oil barrel", "Sulfuric acid barrel", "Light oil barrel", "Petroleum gas barrel", "Lubricant barrel", "Empty crude oil barrel", "Empty heavy oil barrel", "Empty light oil barrel", "Empty lubricant barrel", "Empty petroleum gas barrel", "Empty sulfuric acid barrel", "Empty water barrel", "Fill crude oil barrel", "Fill heavy oil barrel", "Fill light oil barrel", "Fill lubricant barrel", "Fill petroleum gas barrel", "Fill sulfuric acid barrel", "Fill water barrel"]
  re_start_of_infobox = re.compile('{{infobox', re.I)

  def __init__(self, infoboxes, api_url, version, testing):
    self.api_url = api_url
    self.version = version
    self.testing = testing
    self.infoboxes = infoboxes
    
    self.update_infoboxes()

  
  def update_infoboxes(self):
    print('Updating the following infoboxes: ' + str(self.infoboxes))
    if InfoboxType.Entity in self.infoboxes:
      self.update_infobox('entities', EntityInfobox)
    if InfoboxType.Technology in self.infoboxes:
      self.update_infobox('technologies', TechnologyInfobox)
    if InfoboxType.Item in self.infoboxes:
      self.update_infobox('items', ItemInfobox)
    if InfoboxType.Recipe in self.infoboxes:
      self.update_infobox('recipes', RecipeInfobox)
    if InfoboxType.Prototype in self.infoboxes:
      self.update_infobox('types', PrototypeInfobox)
  
    
  def update_infobox(self, file_name, klass):    
    with open(os.path.dirname(os.path.abspath(__file__)) + f'/data/{self.version}/wiki-{file_name}-{self.version}.json', 'r') as f:
      file = json.load(f)
      
    session = requests.Session()
    edit_token = get_edit_token(session, self.api_url)
    
    for name, data in file.items():
      if name in self.no_infobox:
        continue
      infobox_data = klass(name, data)
      page_name = 'Infobox:' + infobox_data.name
      page = get_page_safe(session, self.api_url, page_name)
      if not page:
        print(f'Page for Infobox:{infobox_data.name} does not exist. Creating....')
        page = '{{Infobox\n}}<noinclude>[[Category:Infobox page]]</noinclude>'
      new_page = page
      summary = ''
      
      for property in infobox_data.get_all_properties():     
        new_page, summary = self.update_property(property, new_page, summary)
        
      if page != new_page:
        if self.testing:
          print(new_page + '      ' + summary)
        else:
          print(edit_page(session, self.api_url, edit_token, page_name, new_page, summary).text)
      else:
        print(f'{infobox_data.name} was not changed.')


  def update_property(self, property, page, summary):
    on_page = re.search(r'(\|\s*' + property.name + r'\s*=\s*([^\|}\n]+))\n*(\||}})', page)
    if on_page:
      if (not property.get_data_string()) or property.get_data_string() == '0': # our property is empty and should be removed from the page
        page = page[:on_page.start()] + on_page.group(3) + page[on_page.end():]
        summary += 'Removed ' + property.name + '. '
      elif on_page.group(2) == property.get_data_string(): # our page contains exactly what we want
        return page, summary
      else: # replace data that is on the page
        page = page[:on_page.start()] + str(property) + page[on_page.start() + len(on_page.group(1)):]
        summary += 'Updated ' + property.name + f' to {self.version}. '
    elif property.get_data_string() and property.get_data_string() != '0': # add data to page (if there is any to add)
      page = re.sub(self.re_start_of_infobox, r'\g<0>\n' + str(property), page)
      summary += 'Added ' + property.name + '. '
    
    return page, summary
    
if __name__ == '__main__':
  InfoboxUpdate([InfoboxType.Entity, InfoboxType.Technology, InfoboxType.Item, InfoboxType.Recipe, InfoboxType.Prototype], 'https://wiki.factorio.com/api.php', '0.17.5', False)
