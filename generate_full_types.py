import argparse
import re

class_suffix = 'Prototype'

parser = argparse.ArgumentParser()
parser.add_argument('--not-prototype', action='store_true')
parser.add_argument('--file-name', help='Used to specify a file name if it differs from the prototype name')
parser.add_argument('--short-output', action='store_true')
parser.add_argument('--path-to-source', default='C:\\Users\\Erik\\Documents\\GitHub\\Factorio\\')
parser.add_argument('--path-to-prototype', default='src\\Entity\\')
args = parser.parse_args()

if args.not_prototype:
  class_suffix = ''
path_to_source = args.path_to_source
path_to_prototype = args.path_to_prototype

def main(prototype_name):
  file_name = args.file_name if args.file_name else prototype_name

  with open(path_to_source + path_to_prototype + file_name + class_suffix + '.hpp', 'r', encoding="utf8") as f:
    hpp_file = list(f)

  name_to_type = get_name_to_type_mapping(hpp_file)

  with open(path_to_source + path_to_prototype + file_name + class_suffix + '.cpp', 'r', encoding="utf8") as f:
    cpp_file = list(f)

  parent = get_parent(hpp_file, cpp_file)

  mandatory_properties = []
  optional_properties = []
  beginning, end = get_lines_of_constructor(prototype_name, cpp_file) # The lines in the file that are part of the constructor

  # Parsing all the line of the constructor to find and parse all the properties
  for i in range(beginning, end):
    line = cpp_file[i]
    if ': super(input)' in line:
      continue

    name_matcher = '^\s\s(,|:)\s\w+' # "  , propertyName" or "  : propertyName"
    name = re.search(name_matcher, line)
    if not name:
      continue
    else:
      name = re.sub('^\s*(,|:)\s+', '', name.group()) # Remove the whitespace and "," or ":" in front of the propertyName
    property_arguments = re.sub(name_matcher + '\(', '', line) # Arguments of the constructor of the property

    if name in name_to_type:
      type = name_to_type[name]
    else:
      print(f'Could not find "{name}" in type list. Skipping property.')
      continue

    print('--- in files ---')
    print(type + ' ' + name) # Internal name and class
    print(property_arguments)

    current_property = Property(type, property_arguments) # Most of the parsing happens here - see Property.__init__

    print('----- best guess -----')
    print(current_property.name) # Lua name
    print(current_property.type) # Wiki type
    if current_property.default:
      print('Default: ' + current_property.default)
    print('optional' if current_property.optional else 'mandatory')
    correct = input('nothing if guess is correct, anything else if incorrect: ')

    if correct == '': # Everything is correct
      current_property.set_description()

      if current_property.optional:
        optional_properties.append(str(current_property)) #is this str() needed?
      else:
        mandatory_properties.append(str(current_property))
    else: # Our parsing is wrong, get everything from the user
      property_name = input('property name ')
      if not property_name: # Allows to skip this property by not giving a name
        continue
      current_property.name = property_name
      current_property.type = input('type ')
      current_property.default = input('default ')

      current_property.set_description()

      optional_input = input('optional t/f ')
      current_property.optional = False
      if optional_input == 't':
        current_property.optional = True

      if current_property.optional:
        optional_properties.append(str(current_property))
      else:
        mandatory_properties.append(str(current_property))

  return convert_to_string(parent, mandatory_properties, optional_properties)


# Map the internal property names to their classes
def get_name_to_type_mapping(hpp_file):
  name_to_type = {}
  type_matcher = '^\s+\S+?(<.*>)*\s'
  for line in hpp_file:
    type = re.search(type_matcher, line)
    if not type:
      continue
    else:
      type = type.group().strip()
    names = re.sub(type_matcher, '', line).replace(';', '').strip()
    names = re.sub('=.*$', '', names).strip() # no defaults
    names = re.sub('//.*$', '', names).strip() # no comments
    name_list = re.split(',\s', names)
    for name in name_list:
      name_to_type[name] = type
  return name_to_type


# Prototype class that this class inherits from
def get_parent(hpp_file, cpp_file):
  parent = ''
  if ': super(input)' in ''.join(cpp_file) and 'using super = ' in ''.join(hpp_file):
    parent = re.search('  using super = (\S+);', ''.join(hpp_file)).group(1).replace('Prototype', '')
  return parent


def get_lines_of_constructor(prototype_name, cpp_file):
  beginning = 0
  for i in range(len(cpp_file)):
    if prototype_name + class_suffix + '::' + prototype_name + class_suffix + '(const PropertyTree& input' in cpp_file[i]:
      beginning = i
      break

  end = len(cpp_file)
  for i in range(beginning, len(cpp_file)):
    if '{' in cpp_file[i]:
      end = i
      break

  return beginning, end


class Property:
  def __init__(self, type, property_arguments):
    self.set_name(property_arguments)
    self.type, description_addition = self.sanitize_type(type)
    self.set_optional(property_arguments)
    self.set_default(property_arguments)
    self.description = []
    if description_addition:
      self.description.append(description_addition)


  # Set the name used when loading from lua, snake_case
  def set_name(self, property_arguments):
    property_name = re.search('"\w+"', property_arguments)
    if property_name:
      property_name = property_name.group().replace('"', '')
    else:
      property_name = property_arguments
    self.name = property_name


  # The types on the wiki are slightly different from the classes in the code, so we convert to the wiki types
  @staticmethod
  def sanitize_type(type):
    description_addition = ''
    wiki_type = type.replace('*', '').replace('&', '').replace('_t', '')
    if wiki_type == 'std::string':
      wiki_type = 'string'
    elif wiki_type == 'RenderLayer::Enum':
      wiki_type = 'RenderLayer'
    elif wiki_type == 'CollisionMask::Type':
      wiki_type = 'CollisionMask'
    elif wiki_type == 'Vector':
      wiki_type = 'vector'
    elif wiki_type == 'Vector2f':
      wiki_type = "vector" #technically this vector is different (~2f has 2 floats instead of doubles) but we dont care for now
    elif wiki_type == 'ElectricEnergy':
      wiki_type = 'Energy'
    elif wiki_type == 'SimpleBoundingBox':
      wiki_type = 'BoundingBox'
    elif wiki_type == 'std::unique_ptr<Sound>':
      wiki_type = "Sound"
    elif wiki_type == 'FluidBoxPrototype' or wiki_type == 'std::unique_ptr<FluidBoxPrototype>':
      wiki_type = 'FluidBox'
    elif wiki_type == 'ElectricEnergySourcePrototype' or wiki_type == 'std::unique_ptr<ElectricEnergySourcePrototype>':
      wiki_type = 'EnergySource'
      description_addition = 'Must be an electric energy source.' # We must note this distinction in the property description
    elif wiki_type == 'BurnerPrototype' or wiki_type == 'std::unique_ptr<BurnerPrototype>':
      wiki_type = 'EnergySource'
      description_addition = 'Must be a burner energy source.'
    elif wiki_type == 'EnergySourcePrototype' or wiki_type == 'std::unique_ptr<EnergySourcePrototype>':
      wiki_type = 'EnergySource'
    elif 'IDConnector<' in type:
      wiki_type = 'string'
    return wiki_type, description_addition


  def set_optional(self, property_arguments):
    optional = False
    if ('default' in property_arguments or 'optional' in property_arguments or 'Default' in property_arguments or 'Optional' in property_arguments) or (re.search('input, "\w+"', property_arguments) and self.type != 'Sound'):
      optional = True
    self.optional = optional


  def set_default(self, property_arguments):
    if self.optional and 'getDefault' in property_arguments:
      default = re.search(',([^\),]+)\)+$', property_arguments)
      if default:
        self.default = default.group(1).strip()
        return
    self.default = ''


  def set_description(self):
    desc_input = input('description ')
    if desc_input:
      self.description.insert(0, desc_input)


  def __str__(self):
    if args.short_output:
      return f'* {self.name} - [[Types/{self.type}|{self.type}]]' + (' - Optional' if self.optional else ' - Mandatory') # Sentence above the list is: Table with the following mandatory members:
    else:
      ret = '{{Prototype property|' + self.name + '|[[Types/' + self.type + '|' + self.type + ']]'
      if self.default:
        ret += '|' + self.default
      if self.optional:
        ret += '|optional=true'
      ret += '}}\n'
      if self.description:
        ret += ' '.join(self.description) + '\n'
      return ret


# Convert all the properties to the wiki page string, include info about parent class
def convert_to_string(parent, mandatory_properties, optional_properties):
  out = '{{Prototype parent'
  lua_type_name = 'unknown' # TODO Bilka
  if parent:
    out += '|Prototype/{}'.format(parent)
  out += '}}\n\n'
  out += '{{Prototype TOC|' + lua_type_name + '}}\n\n'
  out += '== Mandatory properties =='
  if parent:
    out += f'\nThis prototype inherits all the properties from [[Prototype/{parent}]].'
  out += '\n'
  if len(mandatory_properties) > 0:
    out += '\n' + '\n'.join(mandatory_properties)

  if len(optional_properties) != 0:
    out += '\n== Optional properties ==\n\n' + '\n'.join(optional_properties)
  return out


if __name__ == '__main__':
  prototype_name = input('prototype_name ')
  print(main(prototype_name))
