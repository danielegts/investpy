from datetime import datetime
import json
import cloudscraper
import pandas as pd

from investpy.globals import PROXIES
from .utils import constant as cst


def get_quotes(instrument_id, start_date, end_date, order="desc", interval="daily", as_json=False, head=None):
	scraper = cloudscraper.create_scraper()
	url = "https://api.investing.com/api/financialdata/{}/historical/chart/?period=MAX&interval={}&pointscount=120"
	url = url.format(instrument_id, cst.QUOTES_INTERVALS[interval])

	req = scraper.get(url, headers=head, proxies=PROXIES)

	if req.status_code != 200:
		raise ConnectionError(
			"ERR#0015: error " + str(req.status_code) + ", try again later."
		)
	else:
		df = pd.DataFrame(json.loads(req.text)['data'])

		df = df[df.columns[:-1]]
		df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
		df.loc[:, 'Date'] = df['Date'].apply(lambda x: datetime.fromtimestamp(int(str(x)[:-3])))

		# df.loc[:, 'Date'] = df['Date'].apply(
		# 	lambda x: datetime.fromtimestamp(int(str(x)[:-3])).strftime('%Y-%m-%d %H:%M:%S'))

		if order in ["descending", "desc"]:
			df.sort_values(ascending=False, inplace=True)

		if as_json is True:
			return df.to_json()

		elif as_json is False:
			return df[(df.Date > start_date) & (df.Date < end_date)]
