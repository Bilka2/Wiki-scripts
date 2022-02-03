## A collection of miscellaneous one-off scripts ##

import json
import os
import re
import requests
from util import get_edit_token, get_page, edit_page, upload_file, move_page, update_file
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
  edit_token = get_edit_token(session, 'https://wiki.factorio.com/api.php')

  directory = os.fsencode(os.path.dirname(os.path.abspath(__file__)) + '/data/icons/')

  for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if not filename.endswith(".png"):
      continue
    image = open(os.path.dirname(os.path.abspath(__file__)) + '/data/icons/' + filename, 'rb')
    print(filename + ' upload: ' + update_file(session, 'https://wiki.factorio.com/api.php', edit_token, filename, image).json()['upload']['result'])
    
def update_tech_icons():
  session = requests.Session()
  edit_token = get_edit_token(session, 'https://wiki.factorio.com/api.php')

  directory = os.fsencode(os.path.dirname(os.path.abspath(__file__)) + '/data/icons/technology/')

  for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if not filename.endswith(".png"):
      continue
    image = open(os.path.dirname(os.path.abspath(__file__)) + '/data/icons/technology/' + filename, 'rb')
    print(filename + ' upload: ' + update_file(session, 'https://wiki.factorio.com/api.php', edit_token, filename[:-4] + ' (research).png', image).json()['upload']['result'])


def dump_pages(pages):
  session = requests.Session()
  edit_token = get_edit_token(session, 'https://wiki.factorio.com/api.php')

  content = ''
  for page in pages:
    content += get_page(session, api_url, page) + '\n'
   
  with open('out.txt', 'w', encoding="utf-8") as f:
    f.write(content)
  

if __name__ == '__main__':
  # used_as_ammo_by_in_infobox(["Flamethrower turret"], "Light oil")
  
  # infobox_category_change(["Infobox:Artillery shell", "Infobox:Artillery targeting remote", "Infobox:Artillery turret", "Infobox:Atomic bomb", "Infobox:Battery MK1", "Infobox:Battery MK2", "Infobox:Cannon shell", "Infobox:Cluster grenade", "Infobox:Combat shotgun", "Infobox:Defender capsule", "Infobox:Destroyer capsule", "Infobox:Discharge defense", "Infobox:Discharge defense remote", "Infobox:Distractor capsule", "Infobox:Energy shield", "Infobox:Energy shield MK2", "Infobox:Exoskeleton", "Infobox:Explosive cannon shell", "Infobox:Explosive rocket", "Infobox:Explosive uranium cannon shell", "Infobox:Firearm magazine", "Infobox:Flamethrower", "Infobox:Flamethrower ammo", "Infobox:Flamethrower turret", "Infobox:Gate", "Infobox:Grenade", "Infobox:Gun turret", "Infobox:Heavy armor", "Infobox:Land mine", "Infobox:Laser turret", "Infobox:Light armor", "Infobox:Modular armor", "Infobox:Nightvision", "Infobox:Personal laser defense", "Infobox:Personal roboport", "Infobox:Personal roboport MK2", "Infobox:Piercing rounds magazine", "Infobox:Piercing shotgun shells", "Infobox:Pistol", "Infobox:Poison capsule", "Infobox:Portable fusion reactor", "Infobox:Portable solar panel", "Infobox:Power armor", "Infobox:Power armor MK2", "Infobox:Radar", "Infobox:Rocket", "Infobox:Rocket launcher", "Infobox:Rocket silo", "Infobox:Shotgun", "Infobox:Shotgun shells", "Infobox:Slowdown capsule", "Infobox:Stone wall", "Infobox:Submachine gun", "Infobox:Uranium cannon shell", "Infobox:Uranium rounds magazine"], "Combat")
  
  # make_type()
  
  # check_if_all_prototypes_are_on_page()
    
  # upload_file_test()
  # move_page_test()
  # create_page_test()
  
  print(convert_data_raw('1.1.53'))
  
  update_tech_icons()
  # update_icons()
  
  # dump_pages(['Types/ActivateEquipmentCapsuleAction', 'Types/ActivityBarStyleSpecification', 'Types/AmmoDamageModifierPrototype', 'Types/AmmoSourceType', 'Types/AmmoType', 'Types/AnimatedVector', 'Types/Animation', 'Types/Animation4Way', 'Types/AnimationElement', 'Types/AnimationFrameSequence', 'Types/AnimationVariations', 'Types/AreaTriggerItem', 'Types/ArtilleryRemoteCapsuleAction', 'Types/ArtilleryTriggerDelivery', 'Types/AttackParameters', 'Types/AttackReaction', 'Types/AttackReactionItem', 'Types/AutoplaceSpecification', 'Types/BaseAttackParameters', 'Types/BeaconGraphicsSet', 'Types/BeaconModuleVisualization', 'Types/BeaconModuleVisualizations', 'Types/BeamAttackParameters', 'Types/BeamTriggerDelivery', 'Types/BlendMode', 'Types/BoolModifierPrototype', 'Types/BorderImageSet', 'Types/BoundingBox', 'Types/BoxSpecification', 'Types/ButtonStyleSpecification', 'Types/CameraEffectTriggerEffectItem', 'Types/CameraStyleSpecification', 'Types/CapsuleAction', 'Types/CharacterArmorAnimation', 'Types/CheckBoxStyleSpecification', 'Types/CircuitConnectorSprites', 'Types/CircularParticleCreationSpecification', 'Types/CircularProjectileCreationSpecification', 'Types/ClusterTriggerItem', 'Types/CollisionMask', 'Types/Color', 'Types/ConnectableEntityGraphics', 'Types/ConsumingType', 'Types/CreateDecorativesTriggerEffectItem', 'Types/CreateEntityTriggerEffectItem', 'Types/CreateExplosionTriggerEffectItem', 'Types/CreateFireTriggerEffectItem', 'Types/CreateParticleTriggerEffectItem', 'Types/CreateSmokeTriggerEffectItem', 'Types/CreateStickerTriggerEffectItem', 'Types/CreateTrivialSmokeEffectItem', 'Types/CursorBoxType', 'Types/CyclicSound', 'Types/DamagePrototype', 'Types/DamageTriggerEffectItem', 'Types/DamageTypeFilters', 'Types/DaytimeColorLookupTable', 'Types/DestroyCliffsCapsuleAction', 'Types/DestroyCliffsTriggerEffectItem', 'Types/DestroyDecorativesTriggerEffectItem', 'Types/DirectTriggerItem', 'Types/Direction', 'Types/DoubleSliderStyleSpecification', 'Types/DropDownStyleSpecification', 'Types/Effect', 'Types/EffectTypeLimitation', 'Types/ElectricUsagePriority', 'Types/ElementImageSet', 'Types/ElementImageSetLayer', 'Types/EmptyWidgetStyleSpecification', 'Types/Energy', 'Types/EnergySource', 'Types/EntityPrototypeFlags', 'Types/EquipmentShape', 'Types/ExplosionDefinition', 'Types/FileName', 'Types/FlameThrowerExplosionTriggerDelivery', 'Types/FlowStyleSpecification', 'Types/FluidBox', 'Types/FluidIngredientPrototype', 'Types/FluidProductPrototype', 'Types/FootprintParticle', 'Types/FootstepTriggerEffectList', 'Types/ForceCondition', 'Types/FrameStyleSpecification', 'Types/GiveItemModifierPrototype', 'Types/GlowStyleSpecification', 'Types/GraphStyleSpecification', 'Types/GraphicsVariation', 'Types/GunSpeedModifierPrototype', 'Types/HeatBuffer', 'Types/HeatConnection', 'Types/HorizontalFlowStyleSpecification', 'Types/HorizontalScrollBarStyleSpecification', 'Types/IconData', 'Types/IconSpecification', 'Types/ImageStyleSpecification', 'Types/IngredientPrototype', 'Types/InsertItemTriggerEffectItem', 'Types/InstantTriggerDelivery', 'Types/InterruptibleSound', 'Types/InvokeTileEffectTriggerEffectItem', 'Types/ItemCountType', 'Types/ItemIngredientPrototype', 'Types/ItemProductPrototype', 'Types/ItemPrototypeFlags', 'Types/ItemStackIndex', 'Types/ItemToPlace', 'Types/LabelStyleSpecification', 'Types/LayeredSound', 'Types/LightDefinition', 'Types/LightFlickeringDefinition', 'Types/LineStyleSpecification', 'Types/LineTriggerItem', 'Types/ListBoxStyleSpecification', 'Types/LocalisedString', 'Types/Loot', 'Types/MapGenPreset', 'Types/MapGenSize', 'Types/MaterialAmountType', 'Types/MinableProperties', 'Types/MinimapStyleSpecification', 'Types/MiningDrillGraphicsSet', 'Types/ModifierPrototype', 'Types/ModuleSpecification', 'Types/NestedTriggerEffectItem', 'Types/NoiseExpression', 'Types/NothingModifierPrototype', 'Types/Order', 'Types/OrientedCliffPrototype', 'Types/PipeConnectionDefinition', 'Types/PlaceAsTile', 'Types/PlaySoundTriggerEffectItem', 'Types/Position', 'Types/ProductPrototype', 'Types/ProgressBarStyleSpecification', 'Types/ProjectileAttackParameters', 'Types/ProjectileTriggerDelivery', 'Types/PumpConnectorGraphics', 'Types/PushBackTriggerEffectItem', 'Types/RadioButtonStyleSpecification', 'Types/RadiusVisualisationSpecification', 'Types/RailPieceLayers', 'Types/RealOrientation', 'Types/RenderLayer', 'Types/Resistances', 'Types/RotatedAnimation', 'Types/RotatedAnimation4Way', 'Types/RotatedAnimationVariations', 'Types/RotatedSprite', 'Types/ScriptTriggerEffectItem', 'Types/ScrollBarStyleSpecification', 'Types/ScrollPaneStyleSpecification', 'Types/SetTileTriggerEffectItem', 'Types/ShowExplosionOnChartTriggerEffectItem', 'Types/SignalColorMapping', 'Types/SignalIDConnector', 'Types/SimpleModifierPrototype', 'Types/SimulationDefinition', 'Types/SliderStyleSpecification', 'Types/SmokeSource', 'Types/Sound', 'Types/SpawnPoint', 'Types/SpeechBubbleStyleSpecification', 'Types/SpiderEnginePrototype', 'Types/SpiderLegGraphicsSet', 'Types/SpiderLegPart', 'Types/SpiderLegSpecification', 'Types/SpiderVehicleGraphicsSet', 'Types/Sprite', 'Types/Sprite4Way', 'Types/Sprite8Way', 'Types/SpriteFlags', 'Types/SpriteNWaySheet', 'Types/SpritePriority', 'Types/SpriteSizeType', 'Types/SpriteVariations', 'Types/StreamAttackParameters', 'Types/StreamTriggerDelivery', 'Types/StretchRule', 'Types/Stripe', 'Types/StyleSpecification', 'Types/StyleWithClickableGraphicalSetSpecification', 'Types/SwitchStyleSpecification', 'Types/TabStyleSpecification', 'Types/TabbedPaneStyleSpecification', 'Types/TableStyleSpecification', 'Types/TechnologySlotStyleSpecification', 'Types/TextBoxStyleSpecification', 'Types/ThrowCapsuleAction', 'Types/TileSprite', 'Types/TileTransitionSprite', 'Types/TileTransitions', 'Types/TipStatus', 'Types/TipTrigger', 'Types/TransportBeltConnectorFrame', 'Types/TreePrototypeVariation', 'Types/Trigger', 'Types/TriggerDelivery', 'Types/TriggerEffect', 'Types/TriggerEffectItem', 'Types/TriggerItem', 'Types/TriggerTargetMask', 'Types/TurretAttackModifierPrototype', 'Types/UnitAISettings', 'Types/UnitSpawnDefinition', 'Types/UnlockRecipeModifierPrototype', 'Types/UseOnSelfCapsuleAction', 'Types/Vector3D', 'Types/VerticalFlowStyleSpecification', 'Types/VerticalScrollBarStyleSpecification', 'Types/WaterReflectionDefinition', 'Types/WireConnectionPoint', 'Types/WirePosition', 'Types/WorkingSound', 'Types/WorkingVisualisation', 'Types/bool', 'Types/double', 'Types/float', 'Types/int16', 'Types/int32', 'Types/int64', 'Types/int8', 'Types/string', 'Types/table', 'Types/uint16', 'Types/uint32', 'Types/uint64', 'Types/uint8', 'Types/vector'])
