import re

with open('hpp.txt', 'r') as f:
  hpp = list(f)

name_to_type = {}

for line in hpp:
  type = re.search('^(\s\s)?\w+\s', line).group().strip()
  names = re.sub('^(\s\s)?\w+\s', '', line).replace(';', '').strip()
  name_list = re.split(',\s', names)
  for name in name_list:
    name_to_type[name] = type

with open('cpp.txt', 'r') as f:
  cpp = list(f)

for line in cpp:
  name = re.search('^\s\s,\s\w+', line).group().replace(',', '').strip()
  property = re.search('\w+', re.sub('^\s\s,\s\w+\(input\["pictures"\]\["', '', line)).group()
  type = name_to_type[name]
  print('=== ' + property + ' ===\n\'\'\'Type\'\'\': [[Types/' + type + ']]\n')