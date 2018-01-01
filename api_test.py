market = "GB"
currency = "GBP"
locale = "en-GB"
origin_place = "LON"
desination_place = "anywhere"
outbound_partial_date = "2017-09"
inbound_partial_data = "2017-09"
api_key = "prtl6749387986743898559646983194"
req_params = [market, currency, locale, origin_place, desination_place, outbound_partial_date, inbound_partial_data,
              api_key]

req = "http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/{}/{}/{}/{}/" \
      "{}/{}/{}?apiKey={}".format(*req_params)

print(req)
