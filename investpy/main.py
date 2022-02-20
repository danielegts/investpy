import investpy

# res = investpy.get_stock_historical_data(stock='IBM', from_date='1/1/2020', to_date='31/12/2020', country='united states')
res = investpy.get_etf_historical_data(etf='3OIS', from_date='1/1/2020', to_date='31/12/2020', country='italy')

print(res)