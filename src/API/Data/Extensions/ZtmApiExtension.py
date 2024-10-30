import time
import logging as log
from src import ConfigExtension as config
import warsaw_data_api as wda_api
from warsaw_data_api.ztm.models import ZtmVehicle, ZtmSchedule
from typing import Optional, List, Dict

from src.API.Data.Extensions.HelperDecoratorsExtension import handleexceptions


class ZtmApiExtension:
    """
    This class is used to get data from the ZTM api.
    """

    def __init__(self) -> None:
        self.api_key = config.load_config('api', 'api_keys', 'ztm_key')
        self.ztm = wda_api.ztm(self.api_key)
        log.basicConfig(level=log.INFO, format='%(asctime)s - %(message)s')
        log.getLogger().setLevel(log.DEBUG)
        log.disable(log.NOTSET)

    def get_vehicles_location_data(
            self, line: str, vehicle_type: [1, 2], amount: int = 1
    ) -> List[List[Dict[str, str]]]:
        """
        This function is used to get the location of buses or trams with given line number from the api.
        :param line: e.g. 512
        :param vehicle_type: 1 for bus, 2 for tram.
        :param amount: number of calls.
        :return: data from the api as a list.
        """
        data = []

        for _ in range(amount):
            try:
                vehicle_data = self.ztm.get_buses_location(line=line) if vehicle_type == 1 \
                    else self.ztm.get_trams_location(line=line)
            except Exception as e:
                log.error(f"Error getting data: {e}")
                vehicle_data = []
                amount += 1

            if not vehicle_data:
                log.error(f'No data to save - Data {len(data)}/{amount}')
                continue

            converted_vehicle_data = [self.__ztm_vehicle_to_dict_conversion(vehicle) for vehicle in vehicle_data]

            data.append(converted_vehicle_data)
            log.info(f"Got data {len(data)}/{amount}")
            time.sleep(22)

        log.info(f'Finished getting data for {line}')
        return data

    def get_lat_lon_for_vehicle(self, line: str, vehicle_type: [1, 2], amount: int = 1) -> List[Dict[str, float]]:
        """
        This function is used to get the location of buses or trams with given line number from the api.
        :param line:
        :param vehicle_type:
        :param amount:
        :return:
        """
        data = []

        for _ in range(amount):
            try:
                vehicle_data = self.ztm.get_buses_location(line=line) if vehicle_type == 1 \
                    else self.ztm.get_trams_location(line=line)
            except Exception as e:
                log.error(f"Error getting data: {e}")
                vehicle_data = []
                amount += 1

            if not vehicle_data:
                log.error(f'No data to save - Data {len(data)}/{amount}')
                continue

            lat_lon_data = [{'Lat': vehicle.location.latitude, 'Lon': vehicle.location.longitude}
                            for vehicle in vehicle_data]

            data.extend(lat_lon_data)
            log.info(f"Got data {len(data)}/{amount}")
            time.sleep(22)

        log.info(f'Finished getting data for {line}')
        return data

    def get_stop_schedule_data(
            self, line: str, stop_nr: str, amount: int = 1, stop_id: Optional[str] = None,
            stop_name: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        This function is used to get the schedule data for certain stop based on the provided data.
        :param line: e.g. 512
        :param stop_nr: e.g. 02
        :param amount: number of calls.
        :param stop_id: e.g. 7000
        :param stop_name: e.g. 'pl. Bankowy'
        :return: data from the api as a list.
        """
        data = []

        for _ in range(amount):
            try:
                stop_data = self.ztm.get_bus_stop_schedule_by_id(bus_stop_id=stop_id, bus_stop_nr=stop_nr,
                                                                 line=line) if stop_id is not None \
                    else self.ztm.get_bus_stop_schedule_by_name(bus_stop_name=stop_name, bus_stop_nr=stop_nr, line=line)
            except Exception as e:
                log.error(f"Error getting data: {e}")
                stop_data = []
                amount += 1

            if not stop_data:
                log.info('No data to save')
                continue

            converted_stop_data = self.__ztm_schedule_to_dict_conversion(stop_data)

            data.append(converted_stop_data)
            log.info(f"Got data {len(data)}/{amount}")
            time.sleep(22)

        log.info(f'Finished getting data for stop: {stop_id}')
        return data

    def get_lines_for_bus_stop(
            self, stop_nr: str, stop_id: Optional[str] = None, stop_name: Optional[str] = None
    ) -> List[Optional[str]]:
        """
        This function is used to get the lines for certain stop.
        :param stop_name: e.g. 'pl. Bankowy'
        :param stop_nr: e.g. 02
        :param stop_id: e.g. 7000
        :return: list of lines.
        """
        if stop_id is None and stop_name is not None:
            stop_id = self.ztm.get_bus_stop_id_by_bus_stop_name(bus_stop_name=stop_name)

        return self.ztm.get_lines_for_bus_stop_id(bus_stop_id=stop_id, bus_stop_nr=stop_nr)

    @staticmethod
    @handleexceptions
    def __ztm_vehicle_to_dict_conversion(vehicle: ZtmVehicle) -> Dict[str, str]:
        """
        This function is used to convert ZtmVehicle object to dictionary.
        :param vehicle: vehicle object.
        :return: dictionary.
        """
        return {
            "Lines": vehicle.lines,
            "Lon": vehicle.location.longitude,
            "Lat": vehicle.location.latitude,
            "VehicleNumber": vehicle.vehicle_number,
            "Time": vehicle.time,
            "Brigade": vehicle.brigade
        }

    @staticmethod
    @handleexceptions
    def __ztm_schedule_to_dict_conversion(schedule: ZtmSchedule) -> Dict[str, str]:
        """
        This function is used to convert ZtmSchedule object to dictionary.
        :param schedule: schedule object.
        :return: dictionary.
        """
        return {
            "Line": schedule.line,
            "BusStopId": schedule.bus_stop_id,
            "BusStopNr": schedule.bus_stop_nr,
            "Rides": schedule.rides
        }
