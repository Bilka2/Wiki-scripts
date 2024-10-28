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


def prototype_migration_remove_old_content(): # ran after prototype_migration_link_styling()
  with open(os.path.dirname(os.path.abspath(__file__)) + '/prototype_doc_migration/link_mapping.json', 'r') as f:
    link_mapping = json.load(f)
  
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)
  
  for section in ['types', 'prototypes']:
    for wiki_page in link_mapping[section]:
      page_name = wiki_page.removeprefix('https://wiki.factorio.com/')
      page_data = get_page(session, api_url, page_name)
      page_data = page_data[:page_data.find("on the forums].</p></div>\n\n\n\n") + 26]
      print(edit_page(session, api_url, edit_token, page_name, page_data, 'Removed old prototype docs').text)


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


def two_point_zero():
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)
  
  moves_and_more_data = {
    "archive": [
      "Rail signals (research)",
      "Rail signals (research)/zh",
      "Rail signals (research)/de",
      "Rail signals (research)/ru",
      "Rail signals (research)/uk",
      "Rail signals (research)/ja",
      "Stack filter inserter",
      "Stack filter inserter/nl",
      "Stack filter inserter/fr",
      "Stack filter inserter/ko",
      "Stack filter inserter/ru",
      "Stack filter inserter/zh",
      "Stack filter inserter/de",
      "Stack filter inserter/uk",
      "Stack filter inserter/pl",
      "Stack filter inserter/ja",
      "Filter inserter",
      "Filter inserter/de",
      "Filter inserter/nl",
      "Filter inserter/zh",
      "Filter inserter/uk",
      "Filter inserter/ru",
      "Filter inserter/fr",
      "Filter inserter/pl",
      "Filter inserter/ko",
      "Filter inserter/ja",
      "Filter inserter/pt-br",
      "Rocket control unit (research)",
      "Rocket control unit (research)/ja",
      "Rocket control unit (research)/ru",
      "Rocket control unit (research)/de",
      "Rocket control unit (research)/zh",
      "Rocket control unit (research)/uk",
      "Rocket control unit",
      "Rocket control unit/ko",
      "Rocket control unit/fr",
      "Rocket control unit/nl",
      "Rocket control unit/de",
      "Rocket control unit/es",
      "Rocket control unit/uk",
      "Rocket control unit/ru",
      "Rocket control unit/zh",
      "Rocket control unit/ja",
      "Rocket control unit/it",
      "Rocket control unit/pl",
      "Rocket control unit/pt-br",
    ],
    "move": [
      {"from": "Infobox:Portable fusion reactor", "to": "Infobox:Portable fission reactor"},
      {"from": "Portable fusion reactor", "to": "Portable fission reactor"},
      {"from": "Portable fusion reactor/zh", "to": "Portable fission reactor/zh"},
      {"from": "Portable fusion reactor/de", "to": "Portable fission reactor/de"},
      {"from": "Portable fusion reactor/uk", "to": "Portable fission reactor/uk"},
      {"from": "Portable fusion reactor/ja", "to": "Portable fission reactor/ja"},
      {"from": "Portable fusion reactor/ru", "to": "Portable fission reactor/ru"},
      {"from": "Portable fusion reactor/pt-br", "to": "Portable fission reactor/pt-br"},
      {"from": "Infobox:Portable fusion reactor (research)", "to": "Infobox:Portable fission reactor (research)"},
      {"from": "Portable fusion reactor (research)", "to": "Portable fission reactor (research)"},
      {"from": "Portable fusion reactor (research)/ru", "to": "Portable fission reactor (research)/ru"},
      {"from": "Portable fusion reactor (research)/de", "to": "Portable fission reactor (research)/de"},
      {"from": "Portable fusion reactor (research)/uk", "to": "Portable fission reactor (research)/uk"},
      {"from": "Portable fusion reactor (research)/ja", "to": "Portable fission reactor (research)/ja"},
      {"from": "Portable fusion reactor (research)/zh", "to": "Portable fission reactor (research)/zh"},
      {"from": "Infobox:Stack inserter", "to": "Infobox:Bulk inserter"},
      {"from": "Stack inserter", "to": "Bulk inserter"},
      {"from": "Stack inserter/ja", "to": "Bulk inserter/ja"},
      {"from": "Stack inserter/de", "to": "Bulk inserter/de"},
      {"from": "Stack inserter/fr", "to": "Bulk inserter/fr"},
      {"from": "Stack inserter/uk", "to": "Bulk inserter/uk"},
      {"from": "Stack inserter/ko", "to": "Bulk inserter/ko"},
      {"from": "Stack inserter/ru", "to": "Bulk inserter/ru"},
      {"from": "Stack inserter/pl", "to": "Bulk inserter/pl"},
      {"from": "Stack inserter/zh", "to": "Bulk inserter/zh"},
      {"from": "Infobox:Stack inserter (research)", "to": "Infobox:Bulk inserter (research)"},
      {"from": "Stack inserter (research)", "to": "Bulk inserter (research)"},
      {"from": "Stack inserter (research)/zh", "to": "Bulk inserter (research)/zh"},
      {"from": "Stack inserter (research)/ru", "to": "Bulk inserter (research)/ru"},
      {"from": "Stack inserter (research)/es", "to": "Bulk inserter (research)/es"},
      {"from": "Stack inserter (research)/uk", "to": "Bulk inserter (research)/uk"},
      {"from": "Stack inserter (research)/ja", "to": "Bulk inserter (research)/ja"},
      {"from": "Stack inserter (research)/de", "to": "Bulk inserter (research)/de"},
      {"from": "Infobox:Advanced electronics (research)", "to": "Infobox:Advanced circuit (research)"},
      {"from": "Advanced electronics (research)", "to": "Advanced circuit (research)"},
      {"from": "Advanced electronics (research)/pl", "to": "Advanced circuit (research)/pl"},
      {"from": "Advanced electronics (research)/zh", "to": "Advanced circuit (research)/zh"},
      {"from": "Advanced electronics (research)/cs", "to": "Advanced circuit (research)/cs"},
      {"from": "Advanced electronics (research)/uk", "to": "Advanced circuit (research)/uk"},
      {"from": "Advanced electronics (research)/de", "to": "Advanced circuit (research)/de"},
      {"from": "Advanced electronics (research)/ja", "to": "Advanced circuit (research)/ja"},
      {"from": "Advanced electronics (research)/nl", "to": "Advanced circuit (research)/nl"},
      {"from": "Advanced electronics (research)/ru", "to": "Advanced circuit (research)/ru"},
      {"from": "Infobox:Advanced electronics 2 (research)", "to": "Infobox:Processing unit (research)"},
      {"from": "Advanced electronics 2 (research)", "to": "Processing unit (research)"},
      {"from": "Advanced electronics 2 (research)/zh", "to": "Processing unit (research)/zh"},
      {"from": "Advanced electronics 2 (research)/cs", "to": "Processing unit (research)/cs"},
      {"from": "Advanced electronics 2 (research)/ru", "to": "Processing unit (research)/ru"},
      {"from": "Advanced electronics 2 (research)/uk", "to": "Processing unit (research)/uk"},
      {"from": "Advanced electronics 2 (research)/ja", "to": "Processing unit (research)/ja"},
      {"from": "Advanced electronics 2 (research)/pl", "to": "Processing unit (research)/pl"},
      {"from": "Advanced electronics 2 (research)/de", "to": "Processing unit (research)/de"},
      {"from": "Infobox:Used up uranium fuel cell", "to": "Infobox:Depleted uranium fuel cell"},
      {"from": "Used up uranium fuel cell", "to": "Depleted uranium fuel cell"},
      {"from": "Used up uranium fuel cell/fr", "to": "Depleted uranium fuel cell/fr"},
      {"from": "Used up uranium fuel cell/ru", "to": "Depleted uranium fuel cell/ru"},
      {"from": "Used up uranium fuel cell/zh", "to": "Depleted uranium fuel cell/zh"},
      {"from": "Used up uranium fuel cell/ja", "to": "Depleted uranium fuel cell/ja"},
      {"from": "Used up uranium fuel cell/de", "to": "Depleted uranium fuel cell/de"},
      {"from": "Used up uranium fuel cell/pl", "to": "Depleted uranium fuel cell/pl"},
      {"from": "Used up uranium fuel cell/ko", "to": "Depleted uranium fuel cell/ko"},
      {"from": "Used up uranium fuel cell/uk", "to": "Depleted uranium fuel cell/uk"},
      {"from": "Used up uranium fuel cell/nl", "to": "Depleted uranium fuel cell/nl"},
      {"from": "Used up uranium fuel cell/es", "to": "Depleted uranium fuel cell/es"},
      {"from": "Used up uranium fuel cell/pt-br", "to": "Depleted uranium fuel cell/pt-br"},
      {"from": "Infobox:Optics (research)", "to": "Infobox:Lamp (research)"},
      {"from": "Optics (research)", "to": "Lamp (research)"},
      {"from": "Optics (research)/zh", "to": "Lamp (research)/zh"},
      {"from": "Optics (research)/nl", "to": "Lamp (research)/nl"},
      {"from": "Optics (research)/de", "to": "Lamp (research)/de"},
      {"from": "Optics (research)/ru", "to": "Lamp (research)/ru"},
      {"from": "Optics (research)/uk", "to": "Lamp (research)/uk"},
      {"from": "Optics (research)/ja", "to": "Lamp (research)/ja"},
      {"from": "Infobox:Energy weapons damage (research)", "to": "Infobox:Laser weapons damage (research)"},
      {"from": "Energy weapons damage (research)", "to": "Laser weapons damage (research)"},
      {"from": "Energy weapons damage (research)/de", "to": "Laser weapons damage (research)/de"},
      {"from": "Energy weapons damage (research)/ru", "to": "Laser weapons damage (research)/ru"},
      {"from": "Energy weapons damage (research)/zh", "to": "Laser weapons damage (research)/zh"},
      {"from": "Energy weapons damage (research)/uk", "to": "Laser weapons damage (research)/uk"},
      {"from": "Energy weapons damage (research)/ja", "to": "Laser weapons damage (research)/ja"}
    ]
  }
  
  # archive pages + files = prepend edit {{archive}} onto them and move to archive namespace
  for title in moves_and_more_data['archive']:
    print(edit_page(session, api_url, edit_token, title, '{{archive}}', 'Archived page (Removed in 2.0)', True).text) # prepend edit 
    print(move_page(session, api_url, edit_token, title, f'Archive:{title}', 'Archived page (Removed in 2.0)').text)
  
  
  # move pages + files - leave redirects - also do infoboxes on the pages
  for move_data in moves_and_more_data['move']:
    if 'Infobox' not in move_data['from'] and 'File' not in move_data['from']:
      page = get_page(session, api_url, move_data['from'])
      from_title_no_lang_suffix = re.search('([^/]+)(\/\S+)?', move_data['from']).group(1)
      to_title_no_lang_suffix = re.search('([^/]+)(\/\S+)?', move_data['to']).group(1)
      page = page.replace('{{:Infobox:' + from_title_no_lang_suffix + '}}', '{{:Infobox:' + to_title_no_lang_suffix + '}}')
      
      print(edit_page(session, api_url, edit_token, move_data['from'], page, 'Renamed in 2.0').text)
      
    print(move_page(session, api_url, edit_token, move_data['from'], move_data['to'], 'Renamed in 2.0').text)


if __name__ == '__main__':
  # used_as_ammo_by_in_infobox(["Flamethrower turret"], "Light oil")
  
  # infobox_category_change(["Infobox:Artillery shell", "Infobox:Artillery targeting remote", "Infobox:Artillery turret", "Infobox:Atomic bomb", "Infobox:Battery MK1", "Infobox:Battery MK2", "Infobox:Cannon shell", "Infobox:Cluster grenade", "Infobox:Combat shotgun", "Infobox:Defender capsule", "Infobox:Destroyer capsule", "Infobox:Discharge defense", "Infobox:Discharge defense remote", "Infobox:Distractor capsule", "Infobox:Energy shield", "Infobox:Energy shield MK2", "Infobox:Exoskeleton", "Infobox:Explosive cannon shell", "Infobox:Explosive rocket", "Infobox:Explosive uranium cannon shell", "Infobox:Firearm magazine", "Infobox:Flamethrower", "Infobox:Flamethrower ammo", "Infobox:Flamethrower turret", "Infobox:Gate", "Infobox:Grenade", "Infobox:Gun turret", "Infobox:Heavy armor", "Infobox:Land mine", "Infobox:Laser turret", "Infobox:Light armor", "Infobox:Modular armor", "Infobox:Nightvision", "Infobox:Personal laser defense", "Infobox:Personal roboport", "Infobox:Personal roboport MK2", "Infobox:Piercing rounds magazine", "Infobox:Piercing shotgun shells", "Infobox:Pistol", "Infobox:Poison capsule", "Infobox:Portable fusion reactor", "Infobox:Portable solar panel", "Infobox:Power armor", "Infobox:Power armor MK2", "Infobox:Radar", "Infobox:Rocket", "Infobox:Rocket launcher", "Infobox:Rocket silo", "Infobox:Shotgun", "Infobox:Shotgun shells", "Infobox:Slowdown capsule", "Infobox:Stone wall", "Infobox:Submachine gun", "Infobox:Uranium cannon shell", "Infobox:Uranium rounds magazine"], "Combat")
  
  # make_type()
  
  # check_if_all_prototypes_are_on_page()
    
  # upload_file_test()
  # move_page_test()
  # create_page_test()
  
  print(convert_data_raw('2.0.10'))
  
  # update_tech_icons()
  # update_icons()
  
  # categorize_images(["File:Yumako_(research).png", "File:Uranium_mining_(research).png", "File:Turbo_transport_belt_(research).png", "File:Tungsten_steel_(research).png", "File:Tungsten_carbide_(research).png", "File:Tree_seeding_(research).png", "File:Transport_belt_capacity_(research).png", "File:Toolbelt_equipment_(research).png", "File:Tesla_weapons_(research).png", "File:Steel_plate_productivity_(research).png", "File:Space_platform_(research).png", "File:Space_platform_thruster_(research).png", "File:Scrap_recycling_productivity_(research).png", "File:Rocket_turret_(research).png", "File:Rocket_part_productivity_(research).png", "File:Rocket_fuel_productivity_(research).png", "File:Research_productivity_(research).png", "File:Recycling_(research).png", "File:Railgun_(research).png", "File:Railgun_shooting_speed_(research).png", "File:Railgun_damage_(research).png", "File:Rail_support_foundations_(research).png", "File:Quantum_processor_(research).png", "File:Quality_module_(research).png", "File:Quality_module_3_(research).png", "File:Quality_module_2_(research).png", "File:Processing_unit_(research).png", "File:Processing_unit_productivity_(research).png", "File:Portable_fission_reactor_(research).png", "File:Plastic_bar_productivity_(research).png", "File:Planet_discovery_Vulcanus_(research).png", "File:Planet_discovery_Gleba_(research).png", "File:Planet_discovery_Fulgora_(research).png", "File:Planet_discovery_Aquilo_(research).png", "File:Personal_battery_MK3_(research).png", "File:Overgrowth_soil_(research).png", "File:Metallurgic_science_pack_(research).png", "File:Mech_armor_(research).png", "File:Low_density_structure_productivity_(research).png", "File:Lithium_processing_(research).png", "File:Lightning_collector_(research).png", "File:Legendary_quality_(research).png", "File:Jellynut_(research).png", "File:Holmium_processing_(research).png", "File:Heating_tower_(research).png", "File:Health_(research).png", "File:Fusion_reactor_(research).png", "File:Foundation_(research).png", "File:Fish_breeding_(research).png", "File:Epic_quality_(research).png", "File:Elevated_rail_(research).png", "File:Electromagnetic_science_pack_(research).png", "File:Electromagnetic_plant_(research).png", "File:Electric_weapons_damage_(research).png", "File:Cryogenic_science_pack_(research).png", "File:Cryogenic_plant_(research).png", "File:Carbon_fiber_(research).png", "File:Captivity_(research).png", "File:Captive_biter_spawner_(research).png", "File:Calcite_processing_(research).png", "File:Biter_egg_handling_(research).png", "File:Biolab_(research).png", "File:Bioflux_(research).png", "File:Bioflux_processing_(research).png", "File:Biochamber_(research).png", "File:Big_mining_drill_(research).png", "File:Bacteria_cultivation_(research).png", "File:Asteroid_reprocessing_(research).png", "File:Asteroid_productivity_(research).png", "File:Artillery_shell_damage_(research).png", "File:Artificial_soil_(research).png", "File:Agriculture_(research).png", "File:Agricultural_science_pack_(research).png", "File:Advanced_combinators_(research).png", "File:Advanced_circuit_(research).png", "File:Advanced_asteroid_processing_(research).png"])
  
  # dump_pages(['Types/ActivateEquipmentCapsuleAction', 'Types/ActivityBarStyleSpecification', 'Types/AmmoDamageModifierPrototype'])
  
  # prototype_migration_remove_old_content()

  #move_archived_pages_to_namespace()
