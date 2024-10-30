import logging as log
import requests
import socket
import serial
import re
from geopy import distance
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.units import km, m
from typing import Dict
from API.Data.Extensions.HelperDecoratorsExtension import logfunction, handleexceptions


class MapApiExtension:
    """
    This class is used to get data from the Google Maps api.
    """
    def __init__(self):
        self.maps_nominatim = Nominatim(user_agent='LocationListener')
        log.basicConfig(level=log.INFO, format='%(asctime)s - %(message)s')
        log.getLogger().setLevel(log.DEBUG)
        log.disable(log.NOTSET)

    @handleexceptions
    def get_geocode_data(self, address: str) -> dict | None:
        """
        This function is used to get the geocode data for the provided address.
        :param address: The address for which to get the geocode data.
        :return: The geocode data.
        """
        geocode_data = self.maps_nominatim.geocode(address)

        if not geocode_data:
            log.error(f'Geocode data not found for address: {address}')
            return None

        return geocode_data

    @handleexceptions
    def get_reverse_geocode_data(self, latitude: float, longitude: float) -> dict | None:
        """
        This function is used to get the reverse geocode data for the provided latitude and longitude.
        :param latitude: The latitude.
        :param longitude: The longitude.
        :return: The reverse geocode data.
        """
        reverse_geocode_data = self.maps_nominatim.reverse((latitude, longitude))

        if not reverse_geocode_data:
            log.error(f'Reverse geocode data not found for latitude: {latitude} and longitude: {longitude}')
            return None

        return reverse_geocode_data

    @handleexceptions
    def get_distance(self, origin: str, destination: str, measure_units: [km, m]) -> geodesic | None:
        """
        This function is used to get the distance between two points in km.
        :param origin: The origin point.
        :param destination: The destination point.
        :param measure_units: The measure units in which the result will be returned.
        :return: The distance between the two points in km or m.
        """
        if measure_units not in [km, m]:
            log.error(f'Invalid measure units: {measure_units}')
            return None

        origin_data = self.get_geocode_data(origin)

        if not origin_data:
            log.error(f'Failed to get geocode data for origin: {origin}')
            return None

        destination_data = self.get_geocode_data(destination)

        if not destination_data:
            log.error(f'Failed to get geocode data for destination: {destination}')
            return None

        origin_location = (origin_data.latitude, origin_data.longitude)
        destination_location = (destination_data.latitude, destination_data.longitude)

        dist = distance.distance(origin_location, destination_location)

        if measure_units == km:
            return dist.km
        elif measure_units == m:
            return dist.m

        return dist

    @staticmethod
    @logfunction
    @handleexceptions
    def parse_gpgga(data: list) -> Dict[str, float] | None:
        """
        This function is used to parse the GPGGA data.
        :param data: The data to parse.
        :return: The parsed data.
        """
        latitude = float(data[2])
        lat_direction = data[3]
        longitude = float(data[4])
        lon_direction = data[5]

        if lat_direction == 'S':
            latitude = -latitude
        if lon_direction == 'W':
            longitude = -longitude

        return {'latitude': latitude, 'longitude': longitude}

    @staticmethod
    @handleexceptions
    def get_gps_location(
            serial_port: str = '/dev/ttyUSB0', baud_rate: int = 9600, timeout: int = 10
    ) -> Dict[str, float] | None:
        """
        This function is used to get the GPS location.
        :param serial_port: The serial port.
        :param baud_rate: The baud rate.
        :param timeout: The timeout.
        :return: The GPS location.
        """
        ser = serial.Serial(serial_port, baud_rate, timeout=timeout)
        ser.flush()

        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='replace').strip()
                if re.match(r'\$GPGGA', line):
                    data = line.split(',')
                    gps_data = MapApiExtension.parse_gpgga(data)
                    return gps_data
            else:
                return None

    @staticmethod
    @logfunction
    @handleexceptions
    def get_location_of_the_client_request() -> dict | None:
        """
        This function is used to get the location of the client. (It kinda sucks)
        :return: The location of the client.
        """
        # https://ipinfo.io/widget/demo/ipaddress
        ip = socket.gethostbyname(socket.gethostname())
        response = requests.get(f'https://ipinfo.io/widget/demo/{ip}')
        location = response.json()

        if location['error']:
            log.error(f'Failed to get location of the client')
            location = requests.get('https://ipinfo.io')

        client_location = location['data']['loc']

        if not client_location:
            log.error(f'Failed to get location of the client')
            return None

        client_location_dict = {'lat': client_location.split(',')[0], 'lon': client_location.split(',')[1]}

        return client_location_dict
