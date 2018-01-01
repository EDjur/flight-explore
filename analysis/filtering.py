from analysis import domain
from data_requests import sky_client


def filter_on_price(quotes, price_cutoff=20):
    quotes = [quote for quote in quotes if quote['MinPrice'] <= price_cutoff]
    print(quotes)
    return quotes


def collate_result(quotes, places):
    """
    Builds a result dict of following format:
    [
        {
            'Destination': dest,
            'Outbound Date': outbound_date,
            'Price': price,
        }
    ]
    """

    def get_placename_from_id(id):
        """Gets a destination name from a destination id. Has access to places variable."""

        # Remove name index for full info
        destination_name = next((place['Name'] for place in places if place["PlaceId"] == id), False)
        return destination_name

    def get_iata_from_id(id):
        """Gets a destination name from a destination id. Has access to places variable."""

        # Remove name index for full info
        iata_code = next((place['IataCode'] for place in places if place["PlaceId"] == id), False)
        return iata_code

    def get_country_from_id(id):
        """Gets a destination name from a destination id. Has access to places variable."""

        # Remove name index for full info
        country = next((place['CountryName'] for place in places if place["PlaceId"] == id), False)
        return country

    print(places)
    result = [
        {
            'iata_code': get_iata_from_id(quote['OutboundLeg']['DestinationId']),
            'destination': get_placename_from_id(quote['OutboundLeg']['DestinationId']),
            'country': get_country_from_id(quote['OutboundLeg']['DestinationId']),
            'origin_airport': get_placename_from_id(quote['OutboundLeg']['OriginId']),
            'outbound_date': quote['OutboundLeg']['DepartureDate'],
            'price': quote['MinPrice'],
        }
        for quote in quotes
    ]

    flights = [domain.Flight(flight) for flight in result]
    print(flights)

    return flights


def get_flights(start_date, end_date="", price_cutoff=20):
    quotes, places, carriers, currencies = sky_client.request_sky_json()
    filtered_quotes = filter_on_price(quotes, price_cutoff)
    result = collate_result(filtered_quotes, places)
    return result

# if __name__ == '__main__':
#     quotes, places, carriers, currencies = sky_client.request_sky_json()
#
#     result = collate_result(filtered_quotes, places)
#
#     print(json.dumps(result, indent=4))
