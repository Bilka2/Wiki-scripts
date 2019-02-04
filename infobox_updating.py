''' Class structure:
__str__(self):
  The __str__ method of each class has to result in a string that can be parsed by Template:Infobox.
  The string contains all important info saved in the class.
  Note: This can be different from a string that can be parsed as plain wikitext!

Tech:
  desc: All(?) information that can be found in technology infoboxes is part in this class. It can be parsed from "wiki-technologies-x.xx.xx.json" files. Note: Bonuses unlocked by technologies are not shown in infoboxes.
  members:
    name - string - the wiki name of the technology  without " (research)" suffix
    cost - list of IconWithCaption
    cost-multiplier - uint
    expensive-cost-multiplier - uint
    allows - list of IconStrings - the technologies that are unlocked by this technology
    effects - list of IconStrings - the recipes that are unlocked by this technology
    required-technologies - list of IconStrings - the technologies that are must be researched before this technology can be researched

IconWithCaption:
  desc: Abstract container for the information required to generate the wikitext or infobox syntax for an icon.
  to_do: Make this class support uint and string captions.
  members:
    name - string - the file name, like a technology or item, can also be "Time". Does not have "File:" prefix or ".png" suffix.
    caption - uint - the amount or level - displayed as extra info on the icon
  json_representation:
    list:
      at index 0 - string - represents: name
      at index 1 - uint - represents: caption
  
IconString:
  desc: A string that represents the infobox syntax for an icon. Has the form "name, caption". Caption is optional, if it does not exist ", " will also not be present in the string. Note: Caption may not be parsable as a number.
  to_do: Should have a function to be converted into a IconWithCaption when that supports uints and strings as captions.
  members:
    icon - string - the string.
  json_representation: 
    string - represents: icon
'''
