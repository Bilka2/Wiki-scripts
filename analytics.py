import requests
import csv
from operator import itemgetter, attrgetter
import os.path
from util import get_edit_token, edit_page

api_url = 'https://wiki.factorio.com/api.php'
page = 'Factorio:Top_pages'
file_name = 'analytics.csv'

def main():
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)
  
  with open(os.path.dirname(__file__) + '/' + file_name, newline='') as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)
  
  #csv config
  page_data_start = 7
  number_of_pages = 25
  total_views_row = page_data_start + number_of_pages
  wanted_number_of_pages = 21 #has to be < number_of_pages
  
  content = 'Total number of views in the last week: ' + rows[total_views_row][1] + ' (' + rows[total_views_row][2] + ' unique)\n{|class=wikitable\n!#\n!Page\n!Number of views (unique)'
  #add together the two main pages ('/' and 'Main_Page')
  main_views = 0
  main_uniques = 0
  for x in range(page_data_start, number_of_pages + page_data_start):
    title = rows[x][0].replace('/', '', 1)
    if title == '':
      main_views = int(rows[x][1].replace(',', ''))
      main_uniques = int(rows[x][2].replace(',', ''))
  for y in range(page_data_start, number_of_pages + page_data_start):
    title = rows[y][0].replace('/', '', 1)
    if title == 'Main_Page':
      rows[y][1] = str(int(rows[y][1].replace(',', '')) + main_views)
      rows[y][2] = str(int(rows[y][2].replace(',', '')) + main_uniques)
  
  for row in rows[page_data_start:(number_of_pages + page_data_start)]: #make sortable
    row[1] = int(row[1].replace(',', ''))
  sorted_rows = sorted(rows[page_data_start:(number_of_pages + page_data_start)], key=itemgetter(1), reverse=True)

  sorted_rows = sorted_rows[0:wanted_number_of_pages]
  
  n = 1
  for row in sorted_rows:
    title = row[0].replace('/', '', 1)
    views = str(row[1])
    uniques = row[2].replace(',', '')
    if title == '':
      continue
    content += '\n|-\n|' + str(n) + '\n|[[' + title + ']]\n|' + views + ' (' + uniques + ')'  #wikitable row
    n += 1
  content += '\n|}'
  
  edit_response = edit_page(session, api_url, edit_token, page, content, 'Updated top pages')
  
  return edit_response.text

#wont execute if file is imported instead of run
if __name__ == '__main__':
  print (main())
