from the_kraken import api

krakenapi = api.API()
b = krakenapi.get_balance()
print(b)