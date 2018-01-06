from analysis import domain
from data_requests import sky_client
from geopy.distance import vincenty
import json


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

    return flights


def get_flights(start_date, end_date="", price_cutoff=20):
    quotes, places, carriers, currencies = sky_client.request_sky_json()
    if price_cutoff:
        quotes = filter_on_price(quotes, price_cutoff)
    result = collate_result(quotes, places)
    return result


def rank_by_price_distance(flights):
    for flight in flights:
        price_per_km = flight.price / flight.distance
        flight.price_per_km = round(price_per_km * 100, 4)

    # Sort flights by price per km
    flights = sorted(flights, key=lambda flight: flight.price_per_km)
    flights = [flight for flight in flights if flight.price_per_km < 2.5]
    return flights


def calculate_distance(flights):
    with open("airport_data/airports.json", encoding='utf-8') as file:
        airports = json.load(file)
    origin_coordinates = (airports['LHR']['latitude'], airports['LHR']['longitude'])

    for flight in flights:
        try:
            dest_coordinates = (airports[flight.iata_code]['latitude'], airports[flight.iata_code]['longitude'])
        except KeyError as e:
            continue
        distance = round(vincenty(origin_coordinates, dest_coordinates).kilometers)
        flight.distance = distance

    return flights
