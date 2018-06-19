# Wiki scripts

Scripts used on the [factorio wiki.](https://wiki.factorio.com)

The javascript files in this repo:

Common.js - Scripts used for more than one module of wiki scripts; [location on the wiki.](https://wiki.factorio.com/MediaWiki:Common.js)

Infobox-move.js - Scripts used to move the infoboxes. Used once. Currently not on the wiki because they don't need to be used again.

Bot_common.js - All scripts that can only be used by User:BilkaBot because they are located on the [bot's common.js page.](https://wiki.factorio.com/User:BilkaBot/common.js) The infobox updating scripts need the newest version of  [these files](https://github.com/demodude4u/Java-Factorio-Data-Wrapper/tree/master/FactorioDataWrapper/output) as input.

Other js files: Misc scripts that are not not used regularly

Python files in this repo:

util.py - Utility functions, such as logging in. Needs the bot-credentials.json file. Format of that file:

```json
{
  "username": "<Name of the bot>",
  "password": "<Password for the bot, base64encoded>"
}
```

https://www.base64encode.org/ can be used to encode the password.

analytics.py - Put the top pages pulled from google analytics onto the wiki. Needs analytics.csv.

new_fff.py - Get the latest FFF and put it on a page if it isn't already on there.

new_version.py - If provided the forum post number and version number it will put it on a page if it isn't already on there.

redirects.py - Generates a list of redirects, including how many pages link to them. Puts the list on a page.

wanted_pages.py - Generates a list of wanted pages (red links), including how many pages link to them and for wanted language pages some info about the English page. Puts the list on a page.

generate_type.py - Easily format a property for a prototype page.

generate_full_types.py - Read the Factorio source files to semi-automatically generate the documentation for a given prototype.

check_if_all_prototypes_are_on_page.py - Check if all the prototype types listed in a file are also present on a wiki page.

Dependencies:

* feedparser
* requests

