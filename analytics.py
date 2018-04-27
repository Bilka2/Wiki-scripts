import requests
import csv
from getpass import getpass
from operator import itemgetter, attrgetter

file_name = 'analytics.csv'
username = 'BilkaBot'
password = getpass('Password for ' + username)
api_url = 'https://wiki.factorio.com/api.php'
page = 'Factorio:Top_pages'
content = ''

session = requests.Session()

#get login token
login_token = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'meta': 'tokens',
    'type': 'login',
})
login_token.raise_for_status()

#log in
login = session.post(api_url, data={
    'format': 'json',
    'action': 'login',
    'lgname': username,
    'lgpassword': password,
    'lgtoken': login_token.json()['query']['tokens']['logintoken'],
})
if login.json()['login']['result'] != 'Success':
    raise RuntimeError(login.json()['login']['reason'])

#get edit token
edit_token = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'meta': 'tokens',
})

#read csv file
page_data_start = 7
number_of_pages = 25
total_views_row = page_data_start + number_of_pages
wanted_number_of_pages = 21 #has to be < number_of_pages
with open(file_name, newline='') as csvfile:
	reader = csv.reader(csvfile)
	rows = list(reader)
	#page header
	content += 'Total number of views in the last week: ' + rows[total_views_row][1] + ' (' + rows[total_views_row][2] + ' unique)\n{|class=wikitable\n!#\n!Page\n!Number of views(unique)'
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
	
	#sort
	for row in rows[page_data_start:(number_of_pages + page_data_start)]:
		row[1] = int(row[1].replace(',', ''))
	sorted_rows = sorted(rows[page_data_start:(number_of_pages + page_data_start)], key=itemgetter(1), reverse=True)
	#only use the wanted number of pages
	sorted_rows = sorted_rows[0:wanted_number_of_pages]
	#turn into wikitable
	n = 1
	for row in sorted_rows:
		title = row[0].replace('/', '', 1)
		views = str(row[1])
		uniques = row[2].replace(',', '')
		if title == '':
			continue
		content += '\n|-\n|' + str(n) + '\n|[[' + title + ']]\n|' + views + ' (' + uniques + ')'
		n += 1
	content += '\n|}'

#edit page
edit_response = session.post(api_url, data={
    'format': 'json',
    'action': 'edit',
    'assert': 'user',
    'text': content,
    'summary': 'Updated top pages',
    'title': page,
	'bot': True,
    'token': edit_token.json()['query']['tokens']['csrftoken'],
})

print (edit_response.text)
