import re

prototype_name = input('prototype_name ')

with open('C:\\Users\\Erik\\Documents\\GitHub\\Factorio\\src\\Entity\\' + prototype_name + 'Prototype.hpp', 'r') as f:
  hpp = list(f)

name_to_type = {}

for line in hpp:
  type = re.search('^(\s\s)?\S+\s', line)
  if not type:
    continue
  else:
    type = type.group().strip()
  names = re.sub('^(\s\s)?\S+\s', '', line).replace(';', '').strip()
  name_list = re.split(',\s', names)
  for name in name_list:
    name_to_type[name] = type

with open('C:\\Users\\Erik\\Documents\\GitHub\\Factorio\\src\\Entity\\' + prototype_name + 'Prototype.cpp', 'r') as f:
  cpp = list(f)

parent = ''
if ': super(input)' in '\n'.join(cpp) and 'using super = ' in '\n'.join(hpp):
  parent = re.search('  using super = (\w+);', '\n'.join(hpp)).group(1).replace('Prototype', '')

mandatory_properties = []
if parent != '':
  mandatory_properties.append('== Mandatory properties ==\nThis prototype inherits all the properties from [[Prototype/{0}]].\n'.format(parent))
else:
  mandatory_properties.append('== Mandatory properties ==\n')
optional_properties = []
optional_properties.append('== Optional properties ==\n')

beginning = 0
for i in range(len(cpp)):
  if prototype_name + 'Prototype::' + prototype_name + 'Prototype(const PropertyTree& input)' in cpp[i]:
    beginning = i + 1
    break

end = 0
for i in range(beginning, len(cpp)):
  if '{' in cpp[i]:
    end = i
    break

for i in range(beginning, end):
  line = cpp[i]
  name = re.search('^\s\s,\s\w+', line)
  if not name:
    continue
  else:
    name = name.group().replace(',', '').strip()
  property = re.sub('^\s\s,\s\w+\(', '', line)
  type = name_to_type[name]
  print('--- in files ---')
  print(type + ' ' + name)
  print(property)
  
  property_name = re.search('"\w+"', property)
  if property_name:
    property_name = property_name.group().replace('"', '')
  else:
    property_name = property
  description_addition = ''
  better_type = type.replace('*', '').replace('&', '').replace('_t', '')
  if better_type == 'ElectricEnergy':
    better_type = 'Energy'
  if better_type == 'ElectricEnergySourcePrototype':
    better_type = 'EnergySource'
    description_addition = 'Must be an electric energy source.'
  optional = False
  if ('default' in property or 'optional' in property or 'Default' in property or 'Optional' in property) or re.search('input, "\w+"', property):
    optional = True  
  print('----- best guess -----')
  print(property_name)
  print(better_type)
  print('optional' if optional else 'mandatory')
  correct = input('nothing if guess is correct, anything else if incorrect: ')
  
  if correct == '':
    out = '=== ' + property_name + ' ===\n\'\'\'Type\'\'\': [[Types/' + better_type + ']]\n'
    default = input('default ')
    description = input('description ')
    
    if default != '':
      out += '\n\'\'\'Default\'\'\': ' + default + '\n'
    
    if description != '':
      out += '\n' + description + '\n'
      
    if optional:
      optional_properties.append(out)
    else:
      mandatory_properties.append(out)
  else:
    property_name = input('property name ')
    if property_name == '':
      continue
    better_type = input('type ')
    out = '=== ' + property_name + ' ===\n\'\'\'Type\'\'\': [[Types/' + better_type + ']]\n'
    default = input('default ')
    description = input('description ')
    
    if default != '':
      out += '\n\'\'\'Default\'\'\': ' + default + '\n'
    
    if description != '':
      if description_addition != '':
        out += '\n' + description + ' ' + description_addition + '\n'
      else:
        out += '\n' + description + '\n'
    elif description_addition != '':
      out += '\n' + description_addition + '\n'
    
    mandatory = input('mandatory t/f ')
    if mandatory == 'f':
      optional_properties.append(out)
    else:
      mandatory_properties.append(out)

out = '== Basics ==\n'
if parent != '':
  out += 'Based on [[Prototype/{0}]].\n'.format(parent)
out += '\n'
out += '\n'.join(mandatory_properties)

if len(optional_properties) > 1:
  out += '\n' + '\n'.join(optional_properties)

print(out)
