import requests
import json
import os.path

with open(os.path.dirname(__file__) + '/matomo-credentials.json', 'r') as f:
  credentials = json.load(f)
token = credentials['token']

pages_file_name = 'analytics.csv'
totals_file_name = 'totals_analytics.csv'
url = 'https://tracking.ops.wube.software/index.php'
common_params = {
  'module': 'API',
  'format': 'CSV',
  'idSite': '4',
  'period': 'range',
  'date': 'previous7',
  'token_auth': token
}

pages_response = requests.get(url, params={**common_params,
  'method': 'Actions.getPageUrls',
  'flat': '1',
  'filter_limit': '40',
  'hideColumns': 'sum_time_network,sum_time_server,sum_time_transfer,sum_time_dom_processing,sum_time_dom_completion,sum_time_on_load,sum_time_spent,nb_hits_with_time_network,min_time_network,max_time_network,nb_hits_with_time_server,min_time_server,max_time_server,nb_hits_with_time_transfer,min_time_transfer,max_time_transfer,nb_hits_with_time_dom_processing,min_time_dom_processing,max_time_dom_processing,nb_hits_with_time_dom_completion,min_time_dom_completion,max_time_dom_completion,nb_hits_with_time_on_load,min_time_on_load,max_time_on_load,entry_nb_visits,entry_nb_actions,entry_sum_visit_length,entry_bounce_count,exit_nb_visits,sum_daily_nb_uniq_visitors,sum_daily_entry_nb_uniq_visitors,sum_daily_exit_nb_uniq_visitors,avg_time_network,avg_time_server,avg_time_transfer,avg_time_dom_processing,avg_time_dom_completion,avg_time_on_load,avg_page_load_time,avg_time_on_page,bounce_rate,exit_rate'
})
pages_response.raise_for_status()

with open(pages_file_name, 'wb') as file:
  file.write(pages_response.content)

totals_response = requests.get(url, params={**common_params,
  'method': 'Actions.get',
  'hideColumns': 'nb_downloads,nb_uniq_downloads,nb_outlinks,nb_uniq_outlinks,nb_searches,nb_keywords'
})
totals_response.raise_for_status()

with open(totals_file_name, 'wb') as file:
  file.write(totals_response.content)
