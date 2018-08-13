import requests
import re
from util import get_edit_token, get_page, edit_page

api_url = 'https://wiki.factorio.com/api.php'


def main(forum_post_number, version):
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)
  latest_version_page_name = 'Main_Page/Latest_versions'
  version_nav_page_name = 'Template:VersionNav'
  
  latest_version_page = get_page(session, api_url, latest_version_page_name)
  version_nav_page = get_page(session, api_url, version_nav_page_name)
  
  if version in latest_version_page:
    return f'Version {version} already found on "{latest_version_page_name}". Aborting.'
  if version in version_nav_page:
    return f'Version {version} already found on "{version_nav_page_name}". Aborting.'
  
  #TODO: FIX THIS FOR WHEN THERE IS NO EXPERIMENTAL
  new_latest_version_page = re.sub(r'({{Translation\|Latest experimental version}}: \[https:\/\/forums\.factorio\.com\/)\d+ \d\.\d+\.\d+', rf'\g<1>{forum_post_number} {version}', latest_version_page)
  new_version_nav_page = re.sub(r'(}}\n)(}}\n<noinclude>{{Documentation}}<\/noinclude>)', rf'\1* {{{{TransLink|Version history/{version[:5]}0#{version}|{version}}}}}\n\2', version_nav_page) #assumes 2 digit major version
  
  edit_response_latest_version_page = edit_page(session, api_url, edit_token, latest_version_page_name, new_latest_version_page, f'{version}')
  edit_response_version_nav_page = edit_page(session, api_url, edit_token, version_nav_page_name, new_version_nav_page, f'{version}')
  
  return edit_response_latest_version_page.text + '\n' + edit_response_version_nav_page.text


if __name__ == '__main__':
  print(main('12345', '0.16.99'))
