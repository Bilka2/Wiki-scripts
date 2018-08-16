import requests
import re
from util import get_edit_token, get_page, edit_page

api_url = 'https://wiki.factorio.com/api.php'

def main(pages, category):
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)
  for page in pages:
    page_data = get_page(session, api_url, page)
    page_data = re.sub(r'\|\s*category\s*=([^\n])+\n', f'|category = {category}\n', page_data)
    if 'category-name' in page_data:
      page_data = re.sub(r'\|\s*category-name([^\n])+\n', '', page_data)
    print(page_data)
    print(edit_page(session, api_url, edit_token, page, page_data, "New infobox categories").text)


if __name__ == '__main__':
  main(["Infobox:Artillery shell", "Infobox:Artillery targeting remote", "Infobox:Artillery turret", "Infobox:Atomic bomb", "Infobox:Battery MK1", "Infobox:Battery MK2", "Infobox:Cannon shell", "Infobox:Cluster grenade", "Infobox:Combat shotgun", "Infobox:Defender capsule", "Infobox:Destroyer capsule", "Infobox:Discharge defense", "Infobox:Discharge defense remote", "Infobox:Distractor capsule", "Infobox:Energy shield", "Infobox:Energy shield MK2", "Infobox:Exoskeleton", "Infobox:Explosive cannon shell", "Infobox:Explosive rocket", "Infobox:Explosive uranium cannon shell", "Infobox:Firearm magazine", "Infobox:Flamethrower", "Infobox:Flamethrower ammo", "Infobox:Flamethrower turret", "Infobox:Gate", "Infobox:Grenade", "Infobox:Gun turret", "Infobox:Heavy armor", "Infobox:Land mine", "Infobox:Laser turret", "Infobox:Light armor", "Infobox:Modular armor", "Infobox:Nightvision", "Infobox:Personal laser defense", "Infobox:Personal roboport", "Infobox:Personal roboport MK2", "Infobox:Piercing rounds magazine", "Infobox:Piercing shotgun shells", "Infobox:Pistol", "Infobox:Poison capsule", "Infobox:Portable fusion reactor", "Infobox:Portable solar panel", "Infobox:Power armor", "Infobox:Power armor MK2", "Infobox:Radar", "Infobox:Rocket", "Infobox:Rocket launcher", "Infobox:Rocket silo", "Infobox:Shotgun", "Infobox:Shotgun shells", "Infobox:Slowdown capsule", "Infobox:Stone wall", "Infobox:Submachine gun", "Infobox:Uranium cannon shell", "Infobox:Uranium rounds magazine"], "Combat")

# regexr.com/3trgo
