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
import math
import numbers
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
  def __init__(self, name, vanilla_data, space_age_data):
    self.name = name
    # this covers everything besides techs, so use this one to mark space-age only
    if vanilla_data and space_age_data:
      self.space_age = String('space-age', '') # since it's in both, this should not be set
    elif space_age_data: # space age only
      self.space_age = String('space-age', 'yes')    
    elif vanilla_data: # vanilla only
      self.space_age = String('space-age', 'no')
    
    # these dont actually get changed by the mods so just pick one of the datas that is available
    data = vanilla_data or space_age_data
    self.internal_name = String('internal-name', data['internal-name'])
    self.prototype_type = String('prototype-type', data['prototype-type'])
  
  def get_all_properties(self):
    return [self.internal_name, self.prototype_type, self.space_age]


class EntityInfobox: # also does tile colors
  def __init__(self, name, vanilla_data, space_age_data):
    self.name = name
    # these dont actually get changed by the mods so just pick one of the datas that is available
    data = vanilla_data or space_age_data
      
    self.health = NumberWithQuality('health', DictUtil.get_optional_number(data, 'health'), 0.3)
    self.mining_time = Number('mining-time', DictUtil.get_optional_number(data, 'mining-time'))
    self.map_color = MapColor('map-color', DictUtil.get_optional_string(data, 'map-color'))
    self.pollution = NumberWithUnit('pollution', DictUtil.get_optional_number(data, 'pollution'), '{{Translation|/m}}')
    self.resistances = Resistances('resistance', DictUtil.get_optional_dict(data, 'resistances'))
    
  def get_all_properties(self):
    return [self.health, self.map_color, self.mining_time, self.pollution, self.resistances]
    
    
class TechnologyInfobox:    
  def __init__(self, name, data): # TODO space-age + changed
    self.name = name + ' (research)'
    self.cost_multiplier = Number('cost-multiplier', DictUtil.get_optional_number(data, 'cost-multiplier'))
    self.cost = IconWithCaptionList('cost', DictUtil.get_optional_list(data, 'cost'))
    self.trigger = TechnologyTrigger('technology-trigger', DictUtil.get_optional_string(data, 'trigger-type'), DictUtil.get_optional_list(data, 'trigger-object'))
    self.allows = IconWithCaptionList_from_list_of_strings('allows', DictUtil.get_optional_list(data, 'allows')) # the technologies that are unlocked by this technology
    self.effects = IconWithCaptionList_from_list_of_strings('effects', DictUtil.get_optional_list(data, 'effects')) # the recipes that are unlocked by this technology
    self.required_technologies =  IconWithCaptionList_from_list_of_strings('required-technologies', DictUtil.get_optional_list(data, 'required-technologies')) #the technologies that are must be researched before this technology can be researched
    self.internal_name = String('internal-name', data['internal-name'])
    self.prototype_type = String('prototype-type', 'technology')
    self.category = String('category', "Technology")
    self.expensive_cost_multiplier = Number('expensive-cost-multiplier', 0) # to remove from existing infoboxes
  
  def get_all_properties(self):
    return [self.cost_multiplier, self.cost, self.trigger, self.allows, self.effects, self.required_technologies, self.internal_name, self.prototype_type, self.category, self.expensive_cost_multiplier]


class ItemInfobox:
  def __init__(self, name, vanilla_data, space_age_data):
    self.name = name
    data = {}
    if vanilla_data and space_age_data:
      if vanilla_data['stack-size'] != space_age_data['stack-size']:
        self.changed_by_space_age_mod = String('changed-by-space-age-mod', 'yes')
        self.stack_size = Number('stack-size', vanilla_data['stack-size'])
        self.space_age_stack_size = Number('space-age-stack-size', space_age_data['stack-size'])
      else:
        self.stack_size = Number('stack-size', vanilla_data['stack-size'])
      
      if DictUtil.get_optional_list(vanilla_data, 'consumers') != DictUtil.get_optional_list(space_age_data, 'consumers'):
        # TODO confused yelling
        # self.changed_by_space_age_mod = String('changed-by-space-age-mod', 'yes')
        self.consumers = IconWithCaptionList_from_list_of_strings('consumers', DictUtil.get_optional_list(vanilla_data, 'consumers'))
        # self.space_age_consumers = IconWithCaptionList_from_list_of_strings('space-age-consumers', DictUtil.get_optional_list(space_age_data, 'consumers'))
      else:
        self.consumers = IconWithCaptionList_from_list_of_strings('consumers', DictUtil.get_optional_list(vanilla_data, 'consumers'))
      
      if hasattr(self, 'changed_by_space_age_mod'):
        # to remove the properties from the infobox if the property is set but not actually different
        if not hasattr(self, 'space_age_stack_size'):
          self.space_age_stack_size = Number('space-age-stack-size', 0)
        if not hasattr(self, 'space_age_consumers'):
          self.space_age_consumers = IconWithCaptionList_from_list_of_strings('consumers', [])
      
      # TODO handle space age required technologies
      self.req_tech = IconWithCaptionList_from_list_of_strings('required-technologies', DictUtil.get_optional_list(vanilla_data, 'required-technologies'))
      return
    
    data = vanilla_data or space_age_data    
    
    self.stack_size = Number('stack-size', data['stack-size'])
    # TODO fix the broken consumers
    if not name in ['Scrap']:
      self.consumers = IconWithCaptionList_from_list_of_strings('consumers', DictUtil.get_optional_list(data, 'consumers'))
    else:
      self.consumers = IconWithCaptionList_from_list_of_strings('consumers', [])
      
    # TODO fix the broken required technologies
    if not name in ['Spoilage', 'Metallic asteroid chunk', 'Carbonic asteroid chunk', 'Oxide asteroid chunk', 'Nutrients', 'Jellynut seed', 'Yumako seed', 'Iron bacteria', 'Copper bacteria', 'Ice', 'Carbon', 'Calcite']:
      self.req_tech = IconWithCaptionList_from_list_of_strings('required-technologies', DictUtil.get_optional_list(data, 'required-technologies'))
    # when adding spoil ticks remember that spoil time is in minutes on the wiki - or maybe not because someone asked for that to be removed. in that case, include the unit here
    
  def get_all_properties(self):
    if hasattr(self, 'changed_by_space_age_mod'):
      return [self.consumers, self.stack_size, self.req_tech, self.changed_by_space_age_mod, self.space_age_stack_size, self.space_age_consumers]
    elif hasattr(self, 'req_tech'): # TODO fix the broken required technologies and remove this elif 
      return [self.consumers, self.stack_size, self.req_tech]
    else:
      return [self.consumers, self.stack_size]
    

class RecipeInfobox:
  def __init__(self, name, data): # TODO changed
    self.name = name
    self.recipe = Recipe('recipe', data['recipe'], DictUtil.get_optional_list(data, 'recipe-output'))
    self.total_raw = Recipe('total-raw', data['total-raw'], [])
    self.producers = IconWithCaptionList_from_list_of_strings('producers', data['producers'])
    self.remove_duplicate_recipes()
    self.cleanup_producers()
    self.expensive_total_raw = Recipe('expensive-recipe', [], []) # to remove from existing infoboxes
    self.expensive_recipe = Recipe('expensive-total-raw', [], []) # to remove from existing infoboxes
  
  def remove_duplicate_recipes(self):
    if self.total_raw == self.recipe:
      self.total_raw.clear()
      print(f'{self.name}: Removed total-raw because it was a duplicate of recipe.') 
  
  def cleanup_producers(self):
    if IconWithCaption(['Assembling machine 1']) in self.producers and IconWithCaption(['Assembling machine 2']) in self.producers and IconWithCaption(['Assembling machine 3']) in self.producers:
      self.producers.remove(IconWithCaption(['Assembling machine 1']))
      self.producers.remove(IconWithCaption(['Assembling machine 2']))
      self.producers.remove(IconWithCaption(['Assembling machine 3']))
      self.producers.add(IconWithCaption(['Assembling machine']))
      
    if IconWithCaption(['Electric furnace']) in self.producers and IconWithCaption(['Steel furnace']) in self.producers and IconWithCaption(['Stone furnace']) in self.producers:
      self.producers.remove(IconWithCaption(['Electric furnace']))
      self.producers.remove(IconWithCaption(['Steel furnace']))
      self.producers.remove(IconWithCaption(['Stone furnace']))
      self.producers.add(IconWithCaption(['Furnace']))
      
    if IconWithCaption(['Character']) in self.producers:
      self.producers.remove(IconWithCaption(['Character']))
      self.producers.add(IconWithCaption(['Player']))
    
    self.producers.sort()
  
  def get_all_properties(self):
    return [self.recipe, self.total_raw, self.producers, self.expensive_recipe, self.expensive_total_raw]
  

class Property:
  def __str__(self):
    return f'|{self.name} = {self.get_data_string()}'
    
  def is_empty(self):
    return True


class Number(Property):
  def __init__(self, name, number):
    self.name = name
    self.number = number
    
  def get_data_string(self):
    return str(self.number)
    
  def is_empty(self):
    return not self.number


class NumberWithUnit(Number):
  def __init__(self, name, number, unit):
    super().__init__(name, number)
    self.unit = unit
    
  def get_data_string(self):
    return str(super().get_data_string() + self.unit)
    
  def is_empty(self):
    return super().is_empty()


class NumberWithQuality(Number):
  def __init__(self, name, number, multiplier):
    super().__init__(name, number)
    self.multiplier = multiplier
    
  def value_for_level(self, level):
    return math.floor(self.number * (1 + self.multiplier * level))
    
  def get_data_string(self):
    return f'{{{{Quality|{self.number}|{self.value_for_level(1)}|{self.value_for_level(2)}|{self.value_for_level(3)}|{self.value_for_level(5)}}}}}'
    
  def is_empty(self):
    return super().is_empty()


class String(Property):
  def __init__(self, name, string):
    self.name = name
    self.string = string
    
  def get_data_string(self):
    return self.string
  
  def is_empty(self):
    return not self.string


class MapColor(Property):
  def __init__(self, name, data):
    self.name = name
    self.color = self.convert_to_chart_color(data) if data else data
    
  @staticmethod  
  def convert_to_chart_color(color): # convert from rgb888 to rgb565 to rgb888 (chart uses rgb565)
    return format((int(color, 16) & 0xF8FAF8), '06x')

  def get_data_string(self):
    return self.color
    
  def is_empty(self):
    return not self.color


class Resistances(Property):
  def __init__(self, name, resistances):
    self.name = name
    self.resistances = resistances
    
  def get_data_string(self):
    ret = []
    for type in sorted(self.resistances.keys()):
      resist = self.resistances[type]
      ret.append('{{Translation|' + type.capitalize() + '}}: ' + str(resist['decrease']) + '/' + str(resist['percent']) + '%')
    return '<br>'.join(ret)
    
  def is_empty(self):
    return not self.resistances


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
    
  def is_empty(self):
    return not self.ingredients and not self.products


class TechnologyTrigger(Property):
  def __init__(self, name, trigger_type, trigger_object):    
    self.name = name
    self.trigger_type = trigger_type
    self.trigger_object = IconWithCaption(trigger_object) if trigger_object else trigger_object
    
  def get_data_string(self):
    ret = self.trigger_type
    if not self.trigger_object.is_empty():
      ret = ret + ": " + str(self.trigger_object)
    return ret
    
  def is_empty(self):
    return not self.trigger_type


class IconWithCaptionList(Property):
  def __init__(self, name, data):
    self.name = name
    self.list = [IconWithCaption(icon) for icon in data]
  
  def get_data_string(self):
    return ' + '.join([str(icon) for icon in self.list])
  
  def sort(self):
    self.list.sort()
    
  def remove(self, IconWithCaption):
    self.list.remove(IconWithCaption)
    
  def add(self, IconWithCaption):
    self.list.append(IconWithCaption)
  
  def __contains__(self, IconWithCaption):
    return IconWithCaption in self.list
  
  def is_empty(self):
    return not self.list


class IconWithCaption:
  def __init__(self, data):
    self.file_name = data[0]
    self.caption = data[1] if len(data) == 2 else ""
    
  def __str__(self):
    if self.caption:
      if isinstance(self.caption, numbers.Number):
        return f'{self.file_name}, {self.caption:.6g}'
      else:
        return f'{self.file_name}, {self.caption}'
    else:
      return f'{self.file_name}'
  
  def __eq__(self, other):
    return self.file_name == other.file_name and self.caption == other.caption
    
  def __lt__(self, other):
    if self.file_name != other.file_name:
      return self.file_name < other.file_name
    
    return self.caption < other.caption
    
  def is_empty(self):
    return not self.file_name


def IconWithCaptionList_from_list_of_strings(name, list):
  return IconWithCaptionList(name, [string.split(', ') for string in list])


class InfoboxUpdate:
  no_infobox = ["Basic oil processing", "Advanced oil processing", "Coal liquefaction", "Barrel", "Heavy oil cracking", "Light oil cracking", "Solid fuel from heavy oil", "Solid fuel from light oil", "Solid fuel from petroleum gas", "Water barrel", "Crude oil barrel", "Heavy oil barrel", "Sulfuric acid barrel", "Light oil barrel", "Petroleum gas barrel", "Lubricant barrel", "Empty crude oil barrel", "Empty heavy oil barrel", "Empty light oil barrel", "Empty lubricant barrel", "Empty petroleum gas barrel", "Empty sulfuric acid barrel", "Empty water barrel", "Fluoroketone (cold) barrel", "Fluoroketone (hot) barrel", "Empty fluoroketone (cold) barrel", "Empty fluoroketone (hot) barrel"]
  no_infobox += ["Casting copper", "Casting copper cable", "Casting iron", "Casting iron gear wheel", "Casting iron stick", "Casting low density structure", "Casting pipe", "Casting pipe to ground", "Casting steel", "Concrete from molten iron", "Nutrients from bioflux", "Nutrients from biter egg", "Nutrients from fish", "Nutrients from spoilage", "Nutrients from yumako mash", "Simple coal liquefaction", "Solid fuel from ammonia", "Scrap recycling", "Molten iron from lava", "Molten copper from lava", "Advanced thruster fuel", "Advanced thruster oxidizer", "Iron bacteria cultivation", "Copper bacteria cultivation", "Rocket fuel from jelly", "Ammonia rocket fuel", "Biolubricant", "Bioplastic", "Biosulfur"] # Space age exclusions that I'm sure about
  # Where are molten iron and molten copper from ore?
  no_infobox += ["Steam condensation", "Acid neutralisation", "Burnt spoilage"] # Space age exclusions that I'm not sure about. https://wiki.factorio.com/Steam_condensation - probably not???, it already is on water page. https://wiki.factorio.com/Acid_neutralisation ??? could be on steam page?
  no_infobox += ["Cooling hot fluoroketone", "Ammoniacal solution separation"] # These recipes should ideally just be in the fluid infoboxes (Fluoroketone (cold), Ammonia)
  # Wood processing recipe should go into Tree seed infobox
  no_infobox += ["Advanced carbonic asteroid crushing", "Advanced metallic asteroid crushing", "Advanced oxide asteroid crushing", "Carbonic asteroid crushing", "Carbonic asteroid reprocessing", "Metallic asteroid crushing", "Metallic asteroid reprocessing", "Oxide asteroid crushing", "Oxide asteroid reprocessing"] # Space age exclusions that I'm ????? about
  # ???? https://wiki.factorio.com/index.php?title=Fish_breeding&redirect=no
  # should get infobox: "Ice melting"
  # should coal synthesis really get an infobox?
  # yumako mash and jellynut processing - on jelly/mash or in seed infoboxes? same question re redirects https://wiki.factorio.com/index.php?title=Jellynut_processing&redirect=no
  # where is flourine map color + mining time?? entity doesnt seem to end up in fluid infobox
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
      vanilla_json = json.load(f)
    with open(os.path.dirname(os.path.abspath(__file__)) + f'/data/{self.version}-space-age/wiki-{file_name}-{self.version}.json', 'r') as f:
      space_age_json = json.load(f)

    session = requests.Session()
    edit_token = get_edit_token(session, self.api_url)

    for name, space_age_data in space_age_json.items():
      if name not in vanilla_json:
        self.update_infobox_data(klass, name, {}, space_age_data, session, edit_token)
      else:
        self.update_infobox_data(klass, name, vanilla_json[name], space_age_data, session, edit_token)

    if 'Satellite' in vanilla_json:
      self.update_infobox_data(klass, 'Satellite', vanilla_json['Satellite'], {}, session, edit_token)
  
  
  def update_infobox_data(self, klass, name, vanilla_data, space_age_data, session, edit_token):
    infobox_data = klass(name, vanilla_data, space_age_data)
    if infobox_data.name in self.no_infobox: #this is after the class instantiation to make sure we append (research) to things like techs and similar
      return
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
    on_page = re.search(r'(\|\s*' + property.name + r'\s*=\s*([^\n]+))\n*(\||}})', page)
    if on_page:
      if property.is_empty(): # our property is empty and should be removed from the page
        page = page[:on_page.start()] + on_page.group(3) + page[on_page.end():]
        summary += 'Removed ' + property.name + '. '
      elif on_page.group(2) == property.get_data_string(): # our page contains exactly what we want
        return page, summary
      else: # replace data that is on the page
        page = page[:on_page.start()] + str(property) + page[on_page.start() + len(on_page.group(1)):]
        summary += 'Updated ' + property.name + f' to {self.version}. '
    elif not property.is_empty(): # add data to page (if there is any to add)
      page = re.sub(self.re_start_of_infobox, r'\g<0>\n' + str(property), page)
      summary += 'Added ' + property.name + '. '
    
    return page, summary
    
if __name__ == '__main__':
  #InfoboxUpdate([InfoboxType.Entity, InfoboxType.Technology, InfoboxType.Item, InfoboxType.Recipe, InfoboxType.Prototype], 'https://wiki.factorio.com/api.php', '2.0.15', False)
  InfoboxUpdate([InfoboxType.Entity, InfoboxType.Prototype, InfoboxType.Item], 'https://wiki.factorio.com/api.php', '2.0.15', False)
  #InfoboxUpdate([InfoboxType.Prototype, InfoboxType.Entity, InfoboxType.Item], 'https://wiki.factorio.com/api.php', '2.0.15', True)
  