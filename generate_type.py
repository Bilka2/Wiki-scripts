name = input('name ')
type = input('type ')
default = input('default ')

out = '=== ' + name + ' ===\n\'\'\'Type\'\'\': [[Types/' + type + ']]\n'

if default != '':
	out += '\n\'\'\'Default\'\'\': ' + default + '\n'

print(out)
