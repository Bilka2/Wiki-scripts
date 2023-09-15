import requests
import re
from util import get_edit_token, get_page, edit_page


def main(forum_post_number, version, api_url = 'https://wiki.factorio.com/api.php', version_nav = True):
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)
  latest_version_page_name = 'Main_Page/Latest_versions'
  version_nav_page_name = 'Template:VersionNav'
  
  latest_version_page = get_page(session, api_url, latest_version_page_name)
  if version_nav:
    version_nav_page = get_page(session, api_url, version_nav_page_name)
  
  if version in latest_version_page:
    return f'Version {version} already found on "{latest_version_page_name}". Aborting.'
  if version_nav:
    if version in version_nav_page:
      return f'Version {version} already found on "{version_nav_page_name}". Aborting.'
  
  if 'None' not in latest_version_page:
    new_latest_version_page = re.sub(r'({{Translation\|Latest experimental version}}: \[https:\/\/forums\.factorio\.com\/)\d+ \d\.\d+\.\d+', rf'\g<1>{forum_post_number} {version}', latest_version_page)
  else:
    new_latest_version_page = re.sub(r'({{Translation\|Latest experimental version}}: ){{Translation\|None}}', rf'\g<1>[https://forums.factorio.com/{forum_post_number} {version}]', latest_version_page)
  if version_nav:
    new_version_nav_page = re.sub(r'(}}\n)(}}\n<noinclude>\n{{Documentation}}\n\[\[Category:Navbox templates\]\]\n<\/noinclude>)', rf'\1* {{{{TransLink|Version history/{version[:version.rfind(".")+1]}0#{version}|{version}}}}}\n\2', version_nav_page)
  
  edit_response_latest_version_page = edit_page(session, api_url, edit_token, latest_version_page_name, new_latest_version_page, f'{version}')
  if version_nav:
    edit_response_version_nav_page = edit_page(session, api_url, edit_token, version_nav_page_name, new_version_nav_page, f'{version}')
  
  return edit_response_latest_version_page.text + (('\n' + edit_response_version_nav_page.text) if version_nav else '')


if __name__ == '__main__':
  print(main('108687', '1.1.91', 'https://wiki.factorio.com/api.php', True))
