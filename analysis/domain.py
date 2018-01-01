from dateutil import parser
from data_requests import sky_client


class Flight:
    def __init__(self, input_dict):
        for k, v in input_dict.items():
            setattr(self, k, v)

        self.outbound_date = parser.parse(self.outbound_date).date()
        self.booking_url = sky_client.send_booking_url(self.iata_code, self.outbound_date)
        self.price_per_km = None
        self.distance = 1

        # self.dest = destination
        # self.origin = origin_airport
        # self.date = outbound_date
        # self.price = price
