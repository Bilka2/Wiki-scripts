import re
import requests
from util import get_edit_token, get_page, edit_page # needed: move page, prepend edit, create page, upload file
# import the infobox updating

def update(testing=True):
  # move that one really special page - need to update the infobox on the page too
  # archive pages + files = prepend edit {{archive}} onto them
  # move pages + files - leave redirects - maybe also do infoboxes?
  # upload files
  # infobox update
  # what about the version history itself??
  # latest version update ??? latest experimental is done outside of this function (probably)
    # updating https://wiki.factorio.com/Template:VersionNav
      # page = page.replace('}}\n<noinclude>', '|group10 = {{Translation|0.17}}\n|list10 =\n* {{TransLink|Version history/0.17.0#0.17.0|0.17.0}}\n}}\n<noinclude>')
    # updating https://wiki.factorio.com/Main_Page/Latest_versions
      # page = page.replace('[[File:Space science pack.png|link=]]', '[[File:Automation science pack.png|link=]]')
      # page = page.replace('[[File:Speed module 3.png|link=]]', '[[File:Speed module.png|link=]]')
      # page = page.replace('{{Translation|The wiki is based on version}} [[Version history/0.16.0|0.16]]', '{{Translation|The wiki is based on version}} [[Version history/0.17.0|0.17]]')
  # sitenotice https://wiki.factorio.com/MediaWiki:Sitenotice
  # change/publish misc pages
  # perhaps do some of the "manual" infobox work here?
