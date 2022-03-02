import calendar
import requests
import re
import feedparser
import time
from util import get_edit_token, get_page, edit_page

page_name = 'News'


def month_abbr_to_month_name(month):
  return calendar.month_name[list(calendar.month_abbr).index(month)] #first to number, then to long name


def turn_page_into_sections(content, depth):
  header_edge = '=' * depth
  separator = '([^=]{0}[^=]+?{0}[^=])'.format(header_edge)
  page_split_into_sections = re.split(separator, content)
  
  sections = []
  for i in range(0, len(page_split_into_sections), 2):
    section = {}
    section['title'] = page_split_into_sections[i-1].strip().replace('=', '').strip() if i-1 > 0 else ''
    section['content'] = page_split_into_sections[i-1] + page_split_into_sections[i] if i-1 > 0 else page_split_into_sections[i]
    sections.append(section)
  
  return sections


def main(api_url = 'https://wiki.factorio.com/api.php'):
  feed = feedparser.parse('https://www.factorio.com/blog/rss')
  if not ('Friday Facts' in feed.entries[0].title):
    return 'Latest blog post is not FFF. Aborting.'
  title = feed.entries[0].title.replace(re.search('Friday Facts #\d+ - ', feed.entries[0].title).group(), '') #without {Friday Facts #241 - } etc
  number = re.search('#\d+', feed.entries[0].title).group().replace('#', '') #string
  release_time = time.strftime("%b %d", feed.entries[0].updated_parsed) #string
  news_line = '* {0} FFF #{1}: [https://www.factorio.com/blog/post/fff-{1} {2}]\n'.format(release_time, number, title) #line that ends up on page

  session = requests.Session()
  edit_token = get_edit_token(session, api_url)
  
  content = get_page(session, api_url, page_name)
  
  if news_line in content:
    return 'FFF already found on page. Aborting.'
  
  sections = turn_page_into_sections(content, 2)
  
  for section in sections:
    if section['title'] == 'Latest':
      latest_news = section['content']
    elif section['title'] == 'Archive':
      archive_sections = turn_page_into_sections(section['content'], 4)
  
  #add new fff
  news_list_start = re.search('<div style=\"column-count:2;-moz-column-count:2;-webkit-column-count:2\">\n\* \w\w\w', latest_news).end() - 5
  new_news = latest_news[:news_list_start] + news_line + latest_news[news_list_start:]
  
  #remove oldest fff
  old_fff = re.sub('\n</div><includeonly>', '', re.search('(\* [^\n]+?)\n</div><includeonly>', new_news).group())
  new_news = new_news.replace(old_fff + '\n', '')
  
  #add oldest fff to archive_section
  old_month = month_abbr_to_month_name(re.search('\* \w\w\w', old_fff).group().replace('* ', ''))
  found_section = False
  for section in archive_sections:
    if section['title'] == old_month:
      found_section = True
      archive_list_start = re.search('=\n\n*', section['content']).end()
      section['content'] =  section['content'][:archive_list_start] + old_fff + '\n' + section['content'][archive_list_start:]
  
  if not found_section:
    archive_sections[0]['content'] += '\n==== ' + old_month + ' ====\n\n' + old_fff + '\n'
  
  #final content
  archive_joined = ''
  for section in archive_sections:
    archive_joined += section['content']
  
  for section in sections:
    if section['title'] == 'Latest':
      section['content'] = new_news
    elif section['title'] == 'Archive':
      section['content'] = archive_joined
  
  end_content = ''
  for section in sections:
    end_content += section['content']
  
  edit_response = edit_page(session, api_url, edit_token, page_name, end_content, 'New FFF')
  
  return edit_response.text


if __name__ == '__main__':
  print (main())
