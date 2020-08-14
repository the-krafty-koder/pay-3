import os
import requests

from math import radians, cos, sin, asin, sqrt

ACCU_APIKEY = os.environ.get('ACCUWEATHER_APIKEY')


class GetLocationDetails:

    """
    Return location details after obtaining  ip address.
    """

    def __init__(self):
        self.response = self.get_response()

    def get_response(self):

        response = requests.get("https://api.ipgeolocation.io/ipgeo?apiKey=6bc533e47ded411495dd13d07087b174")
        self.response = response.json()

        return self.response

    def get_timezone(self):

        return self.response['TimeZone']['Code'], self.response['TimeZone']['Name']

    def get_geoposition(self):

        return self.response['latitude'], self.response['longitude']


def haversine(lon1, lat1, lon2, lat2):
    """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, float(lon2), float(lat2)])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
    return c * r


def check_if_in_radius(center, test):
    """
        Check if location coordinates fall within radius
    """
    in_radius = haversine(center[1], center[0], test[1], test[0])
    if in_radius:
        return True

    return False
