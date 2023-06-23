import requests
import csv
from operator import itemgetter, attrgetter
import os.path
from util import get_edit_token, edit_page

api_url = 'https://wiki.factorio.com/api.php'
page = 'Factorio:Top_pages'
file_name = 'analytics.csv'
totals_file_name = 'totals_analytics.csv'

def main():
  session = requests.Session()
  edit_token = get_edit_token(session, api_url)

  with open(os.path.dirname(__file__) + '/' + file_name, newline='', encoding='utf-16-le') as csvfile:
    rows = list(csv.reader(csvfile))

  with open(os.path.dirname(__file__) + '/' + totals_file_name, newline='', encoding='utf-16-le') as csvfile:
    totals_rows = list(csv.reader(csvfile))

  #csv config
  page_data_start = 1
  number_of_pages = 40
  total_views_row = 1 # in totals_file_name
  wanted_number_of_pages = 20 # has to be < number_of_pages

  total_views = int(totals_rows[total_views_row][0])
  total_uniques = int(totals_rows[total_views_row][1])
  content = f'Total number of views in the last week: {total_views:,} ({total_uniques:,} unique)\n{{|class=wikitable\n!#\n!Page\n!Number of views (unique)'
  #add together the two main pages ('/' and 'Main_Page')
  main_uniques = 0
  main_views = 0
  for x in range(page_data_start, number_of_pages + page_data_start):
    if rows[x][0] == '/':
      main_uniques = int(rows[x][1])
      main_views = int(rows[x][2])
      break

  processed_data = []

  for y in range(page_data_start, number_of_pages + page_data_start):
    if rows[y][3] == '1' or rows[y][0] == '/': # exclude summary rows + main page row processed above
      continue

    title = rows[y][0].replace('/', '', 1)
    uniques = int(rows[y][1])
    views = int(rows[y][2])
    if title == 'Main_Page':
      views += main_views
      uniques += main_uniques
    processed_data.append([title, uniques, views])

  sorted_rows = sorted(processed_data, key=itemgetter(2), reverse=True)

  for n in range(wanted_number_of_pages):
    row = sorted_rows[n]
    title = row[0]
    uniques = row[1]
    views = row[2]
    content += f'\n|-\n|{n+1}\n|[[{title}]]\n|{views} ({uniques})'  #wikitable row
  content += '\n|}'

  edit_response = edit_page(session, api_url, edit_token, page, content, 'Updated top pages')

  return edit_response.text

#wont execute if file is imported instead of run
if __name__ == '__main__':
  print (main())
