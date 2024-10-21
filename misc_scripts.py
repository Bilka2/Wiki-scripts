## A collection of miscellaneous one-off scripts ##

import json
import os
import re
import requests
from util import get_edit_token, get_page, edit_page, upload_file, move_page, update_file, protect_page, get_categorymembers
api_url = 'https://wiki.factorio.com/api.php'


def used_as_ammo_by_in_infobox(used_by, page):
  page = "Infobox:" + page
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)
  page_data = get_page(session, api_url, page)
  infobox_start = page_data.find("|")
  used_by_string = " + ".join(used_by)
  new_page_data = page_data[:infobox_start] + f"|used-as-ammo-by = {used_by_string}\n" + page_data[infobox_start:]
  print(new_page_data)
  print(edit_page(session, api_url, edit_token, page, new_page_data, "Added \"Usable Ammunition For\" to infobox").text)


def infobox_category_change(pages, category): # regexr.com/3trgo
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)
  for page in pages:
    page_data = get_page(session, api_url, page)
    page_data = re.sub(r'\|\s*category\s*=([^\n])+\n', f'|category = {category}\n', page_data)
    if 'category-name' in page_data:
      page_data = re.sub(r'\|\s*category-name([^\n])+\n', '', page_data)
    print(page_data)
    print(edit_page(session, api_url, edit_token, page, page_data, "New infobox categories").text)


def make_type():
  name = input('name ')
  type = input('type ')
  default = input('default ')
  
  out = '{{Prototype property|' + name + '|[[Types/' + type + '|' + type + ']]'
  
  if default:
    out += '|' + default
    
  out += '}}'
  
  print(out)


def check_if_all_prototypes_are_on_page():
  with open('C:\\Users\\Erik\\Documents\\Factorio\\prototype_types_the_game_will_respond_to.txt', 'r') as f: # https://gist.github.com/Bilka2/e1dd885f5ff8eb53d1b66315663f5ca5
    data = list(f)
  
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)
  content = get_page(session, api_url, 'Prototype definitions')
  
  for line in data:
    if not ('\'\'\'' + line.strip() + '\'\'\'' in content):
      print(line.strip())


def convert_data_raw(version):
  with open(os.path.dirname(os.path.abspath(__file__)) + f'/data/{version}/data-raw-tree-{version}.json', 'r') as f:
    dataRawJson = json.load(f)
  
  out = ''
  
  for type, names in dataRawJson.items():
    assert names
    out += '== {{Prototype page|' + type + '}} ==\n'
    out += '<div style="column-count:2;-moz-column-count:2;-webkit-column-count:2">\n'
    for name in names:
      out += f'* {name}\n'
    out += '</div>\n'

  return out


def upload_file_test():
  session = requests.Session()
  edit_token = get_edit_token(session, 'https://testing-wiki.factorio.com/api.php')
  
  file = open('test.png', 'rb')
  
  print(upload_file(session, 'https://testing-wiki.factorio.com/api.php', edit_token, 'Test.png', file, '{{Game image}}').text)


def move_page_test():
  session = requests.Session()
  edit_token = get_edit_token(session, 'https://testing-wiki.factorio.com/api.php')
  
  print(move_page(session, 'https://testing-wiki.factorio.com/api.php', edit_token, 'User:Bilka/Sandbox1', 'User:Bilka/Sandbox', 'This is a test', False).text)


def create_page_test():
  session = requests.Session()
  edit_token = get_edit_token(session, 'https://testing-wiki.factorio.com/api.php')
  
  print(edit_page(session, 'https://testing-wiki.factorio.com/api.php', edit_token, 'User:Bilka/Sandbox1', 'This is a test. Foo bar', 'test').text)


def update_icons():
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)

  directory = os.fsencode(os.path.dirname(os.path.abspath(__file__)) + '/data/icons/')

  for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if not filename.endswith(".png"):
      continue
    image = open(os.path.dirname(os.path.abspath(__file__)) + '/data/icons/' + filename, 'rb')
    print(filename + ' upload: ' + update_file(session, api_url, edit_token, filename, image).json()['upload']['result'])
    
def update_tech_icons():
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)

  directory = os.fsencode(os.path.dirname(os.path.abspath(__file__)) + '/data/icons/technology/')

  for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if not filename.endswith(".png"):
      continue
    image = open(os.path.dirname(os.path.abspath(__file__)) + '/data/icons/technology/' + filename, 'rb')
    print(filename + ' upload: ' + update_file(session, api_url, edit_token, filename[:-4] + ' (research).png', image).json()['upload']['result'])


def dump_pages(pages):
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)

  content = ''
  for page in pages:
    content += get_page(session, api_url, page) + '\n'
   
  with open('out.txt', 'w', encoding="utf-8") as f:
    f.write(content)


def categorize_images(images):
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)  

  for page_name in images:
    page_text = "{{Game image}}"
    print(edit_page(session, api_url, edit_token, page_name, page_text, "Categorized as game image", True).text)
  

def prototype_migration_links():
  with open(os.path.dirname(os.path.abspath(__file__)) + '/prototype_doc_migration/link_mapping.json', 'r') as f:
    link_mapping = json.load(f)
  
  page_text_template = "'''The prototype docs have moved to a new website with an improved format.''' This documentation page can now be found here: [link_placeholder link_placeholder]\n\nThis wiki page is no longer updated and '''will be removed at some point in the future''', so please update your browser bookmarks or other links that sent you here. If you'd like to contribute to the new docs, you can leave your feedback [https://forums.factorio.com/viewforum.php?f=233 on the forums].\n\n\n\n"
  
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)
  
  for section in ['types', 'prototypes']:
    for old, new in link_mapping[section].items():
      if not isinstance(new, str):
        print(f'Not editing page {old} because no new link exists.')
        continue
      page_text = page_text_template.replace('link_placeholder', new)
      page_name = old.removeprefix('https://wiki.factorio.com/')
      print(edit_page(session, api_url, edit_token, page_name, page_text, 'Migrated prototype doc to separate website', True).text)
      print(protect_page(session, api_url, edit_token, page_name, 'Migrated prototype doc to separate website').text)


def prototype_migration_link_styling(): # ran after prototype_migration_links()
  with open(os.path.dirname(os.path.abspath(__file__)) + '/prototype_doc_migration/link_mapping.json', 'r') as f:
    link_mapping = json.load(f)
  
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)
  
  for section in ['types', 'prototypes']:
    for wiki_page in link_mapping[section]:
      page_name = wiki_page.removeprefix('https://wiki.factorio.com/')
      page_data = get_page(session, api_url, page_name)
      page_data = page_data.replace("'''The prototype docs", "<div class=\"stub\"><p>'''The prototype docs")
      page_data = page_data.replace('This wiki page', '</p><p>This wiki page')
      page_data = page_data.replace('on the forums].', 'on the forums].</p></div>')
      print(edit_page(session, api_url, edit_token, page_name, page_data, 'Updated styling of prototype doc migration note').text)


def move_archived_pages_to_namespace(): # https://forums.factorio.com/viewtopic.php?p=597811#p597811
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)
  valid_lang_suffixes = ['', '/cs', '/de', '/es', '/fr', '/it', '/ja', '/nl', '/pl', '/pt-br', '/ru', '/sv', '/uk', '/zh', '/tr', '/ko', '/ms', '/da', '/hu', '/vi', '/pt-pt', '/zh-tw']
  category_name = 'Category:Archived'

  archived_pages = [page['title']
          for suffix in valid_lang_suffixes
            for page in get_categorymembers(session, api_url, f'{category_name}{suffix}')
              if page['ns'] == 0] # No files or infoboxes

  for title in archived_pages:
    # There is 'Wood (archived)' and its translated versions. I decided against removing the '(archived)' because the namespace doesnt show in the infobox title.
    # So wood and wood (archived) would have been named exactly the same in infobox (and displaytitle). That just seems confusing. So don't do that.
    move_target = f'Archive:{title}' # .replace(' (archived)', '')
    print(move_page(session, api_url, edit_token, title, move_target, 'Move archived pages to separate namespace').text)


if __name__ == '__main__':
  # used_as_ammo_by_in_infobox(["Flamethrower turret"], "Light oil")
  
  # infobox_category_change(["Infobox:Artillery shell", "Infobox:Artillery targeting remote", "Infobox:Artillery turret", "Infobox:Atomic bomb", "Infobox:Battery MK1", "Infobox:Battery MK2", "Infobox:Cannon shell", "Infobox:Cluster grenade", "Infobox:Combat shotgun", "Infobox:Defender capsule", "Infobox:Destroyer capsule", "Infobox:Discharge defense", "Infobox:Discharge defense remote", "Infobox:Distractor capsule", "Infobox:Energy shield", "Infobox:Energy shield MK2", "Infobox:Exoskeleton", "Infobox:Explosive cannon shell", "Infobox:Explosive rocket", "Infobox:Explosive uranium cannon shell", "Infobox:Firearm magazine", "Infobox:Flamethrower", "Infobox:Flamethrower ammo", "Infobox:Flamethrower turret", "Infobox:Gate", "Infobox:Grenade", "Infobox:Gun turret", "Infobox:Heavy armor", "Infobox:Land mine", "Infobox:Laser turret", "Infobox:Light armor", "Infobox:Modular armor", "Infobox:Nightvision", "Infobox:Personal laser defense", "Infobox:Personal roboport", "Infobox:Personal roboport MK2", "Infobox:Piercing rounds magazine", "Infobox:Piercing shotgun shells", "Infobox:Pistol", "Infobox:Poison capsule", "Infobox:Portable fusion reactor", "Infobox:Portable solar panel", "Infobox:Power armor", "Infobox:Power armor MK2", "Infobox:Radar", "Infobox:Rocket", "Infobox:Rocket launcher", "Infobox:Rocket silo", "Infobox:Shotgun", "Infobox:Shotgun shells", "Infobox:Slowdown capsule", "Infobox:Stone wall", "Infobox:Submachine gun", "Infobox:Uranium cannon shell", "Infobox:Uranium rounds magazine"], "Combat")
  
  # make_type()
  
  # check_if_all_prototypes_are_on_page()
    
  # upload_file_test()
  # move_page_test()
  # create_page_test()
  
  # print(convert_data_raw('1.1.91'))
  
  # update_tech_icons()
  # update_icons()
  
  categorize_images(["File:Yumako.png", "File:Yumako_seed.png", "File:Yumako_processing.png", "File:Yumako_mash.png", "File:Wood_processing.png", "File:Turbo_underground_belt.png", "File:Turbo_transport_belt.png", "File:Turbo_splitter.png", "File:Tungsten_ore.png", "File:Tree_seed.png", "File:Toolbelt_equipment.png", "File:Thruster.png", "File:Thruster_oxidizer.png", "File:Thruster_fuel.png", "File:Tesla_gun.png", "File:Tesla_ammo.png", "File:Supercapacitor.png", "File:Steam_condensation.png", "File:Spoilage.png", "File:Space_platform_hub.png", "File:Space_platform_foundation.png", "File:Solid_fuel_from_ammonia.png", "File:Simple_coal_liquefaction.png", "File:Selector_combinator.png", "File:Scrap_recycling.png", "File:Rocket_turret.png", "File:Rocket_fuel_from_jelly.png", "File:Railgun_ammo.png", "File:Rail_support.png", "File:Rail_ramp.png", "File:Quality_module.png", "File:Quality_module_3.png", "File:Quality_module_2.png", "File:Promethium_asteroid_chunk.png", "File:Portable_fission_reactor.png", "File:Plasma.png", "File:Personal_battery_MK3.png", "File:Pentapod_egg.png", "File:Oxide_asteroid_reprocessing.png", "File:Oxide_asteroid_crushing.png", "File:Oxide_asteroid_chunk.png", "File:Overgrowth_yumako_soil.png", "File:Overgrowth_jellynut_soil.png", "File:Nutrients.png", "File:Nutrients_from_yumako_mash.png", "File:Nutrients_from_spoilage.png", "File:Nutrients_from_fish.png", "File:Nutrients_from_biter_egg.png", "File:Nutrients_from_bioflux.png", "File:Molten_iron_from_lava.png", "File:Molten_copper.png", "File:Molten_copper_from_lava.png", "File:Metallic_asteroid_reprocessing.png", "File:Metallic_asteroid_crushing.png", "File:Metallic_asteroid_chunk.png", "File:Mech_armor.png", "File:Lithium.png", "File:Lithium_brine.png", "File:Lightning_rod.png", "File:Lightning_collector.png", "File:Jellynut.png", "File:Jellynut_seed.png", "File:Jellynut_processing.png", "File:Jelly.png", "File:Iron_bacteria.png", "File:Iron_bacteria_cultivation.png", "File:Ice_platform.png", "File:Ice_melting.png", "File:Holmium_solution.png", "File:Holmium_plate.png", "File:Heating_tower.png", "File:Fusion_reactor.png", "File:Fusion_power_cell.png", "File:Fusion_generator.png", "File:Foundation.png", "File:Fluoroketone.png", "File:Fluoroketone_cooling.png", "File:Fluoroketone_(hot)_barrel.png", "File:Fluoroketone_(cold)_barrel.png", "File:Fluorine.png", "File:Fish_breeding.png", "File:Empty_fluoroketone_(hot)_barrel.png", "File:Empty_fluoroketone_(cold)_barrel.png", "File:Electrolyte.png", "File:Display_panel.png", "File:Crusher.png", "File:Copper_bacteria.png", "File:Copper_bacteria_cultivation.png", "File:Concrete_from_molten_iron.png", "File:Coal_synthesis.png", "File:Casting_steel.png", "File:Casting_pipe.png", "File:Casting_pipe_to_ground.png", "File:Casting_low_density_structure.png", "File:Casting_iron.png", "File:Casting_iron_stick.png", "File:Casting_iron_gear_wheel.png", "File:Casting_copper.png", "File:Casting_copper_cable.png", "File:Cargo_bay.png", "File:Carbonic_asteroid_reprocessing.png", "File:Carbonic_asteroid_crushing.png", "File:Carbonic_asteroid_chunk.png", "File:Capture_bot_rocket.png", "File:Captive_biter_spawner.png", "File:Calcite.png", "File:Burnt_spoilage.png", "File:Biter_egg.png", "File:Biosulfur.png", "File:Bioplastic.png", "File:Biolubricant.png", "File:Biolab.png", "File:Bioflux.png", "File:Biochamber.png", "File:Asteroid_collector.png", "File:Artificial_yumako_soil.png", "File:Artificial_jellynut_soil.png", "File:Ammoniacal_solution.png", "File:Ammoniacal_solution_separation.png", "File:Ammonia.png", "File:Ammonia_rocket_fuel.png", "File:Advanced_thruster_oxidizer.png", "File:Advanced_thruster_fuel.png", "File:Advanced_oxide_asteroid_crushing.png", "File:Advanced_metallic_asteroid_crushing.png", "File:Advanced_carbonic_asteroid_crushing.png", "File:Acid_neutralisation.png"])
  
  # dump_pages(['Types/ActivateEquipmentCapsuleAction', 'Types/ActivityBarStyleSpecification', 'Types/AmmoDamageModifierPrototype'])
  
  # prototype_migration_link_styling()

  #move_archived_pages_to_namespace()
