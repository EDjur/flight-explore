import requests
import json

market = "GB"
currency = "GBP"
locale = "en-GB"
origin_place = "LON"
destination_place = "anywhere"
outbound_partial_date = "2018-01"
inbound_partial_date = ""
api_key = "prtl6749387986743898559646983194"
req_params = [market, currency, locale, origin_place, destination_place, outbound_partial_date, inbound_partial_date,
              api_key]

search_request_url = "http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/{}/{}/{}/{}/" \
      "{}/{}/{}?apiKey={}".format(*req_params)

skyscanner_base_url = """http://partners.api.skyscanner.net/apiservices"""

# print(url)


def request_sky_json():
    """
    Top-level items: Quotes, Places, Carriers, Currencies
    :return:
    """

    response = json.loads(requests.get(search_request_url).text)
    # print(response)
    quotes = response['Quotes']
    places = response['Places']
    carriers = response['Carriers']
    currencies = response['Currencies']

    return quotes, places, carriers, currencies


def send_booking_url(dest, outbound_date):
    country = market

    booking_url = f"""/referral/v1.0/{country}/{currency}/{locale}/{origin_place}/{dest}/{outbound_date}/{inbound_partial_date}?apiKey={api_key}"""
    booking_url = skyscanner_base_url + booking_url

    return booking_url


# request_sky_json()
