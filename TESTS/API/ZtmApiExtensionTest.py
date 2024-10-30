from pytest import fixture
from API.Data.Extensions.ZtmApiExtension import ZtmApiExtension


@fixture
def ztm_api():
    return ZtmApiExtension()


def test_get_vehicles_location_data(ztm_api):
    data = ztm_api.get_vehicles_location_data('512', 1, 1)
    assert data is not None


def test_get_lat_lon_for_vehicle(ztm_api):
    data = ztm_api.get_lat_lon_for_vehicle('512', 1, 1)
    assert data is not None


def test_get_vehicles_location_data_invalid_line(ztm_api):
    data = ztm_api.get_vehicles_location_data('', 1, 1)
    assert data == []


def test_get_lat_lon_for_vehicle_invalid_line(ztm_api):
    data = ztm_api.get_lat_lon_for_vehicle('', 1, 1)
    assert data == []


def test_get_vehicles_location_data_invalid_vehicle_type(ztm_api):
    data = ztm_api.get_vehicles_location_data('512', 3, 1)
    assert data == []


def test_get_lat_lon_for_vehicle_invalid_vehicle_type(ztm_api):
    data = ztm_api.get_lat_lon_for_vehicle('512', 3, 1)
    assert data == []


def test_get_vehicles_location_data_invalid_amount(ztm_api):
    data = ztm_api.get_vehicles_location_data('512', 1, 0)
    assert data == []


def test_get_lat_lon_for_vehicle_invalid_amount(ztm_api):
    data = ztm_api.get_lat_lon_for_vehicle('512', 1, 0)
    assert data == []


def test_get_vehicles_location_data_invalid_line_vehicle_type(ztm_api):
    data = ztm_api.get_vehicles_location_data('', 3, 1)
    assert data == []


def test_get_lat_lon_for_vehicle_invalid_line_vehicle_type(ztm_api):
    data = ztm_api.get_lat_lon_for_vehicle('', 3, 1)
    assert data == []


def test_get_vehicles_location_data_tram(ztm_api):
    data = ztm_api.get_vehicles_location_data('13', 2, 1)
    assert data is not None


def test_get_lat_lon_for_vehicle_tram(ztm_api):
    data = ztm_api.get_lat_lon_for_vehicle('13', 2, 1)
    assert data is not None


def test_get_vehicles_location_data_invalid_line_tram(ztm_api):
    data = ztm_api.get_vehicles_location_data('', 2, 1)
    assert data == []


def test_get_stop_schedule_data(ztm_api):
    data = ztm_api.get_stop_schedule_data('01', '01', 1)
    assert data is not None


def test_get_stop_schedule_data_invalid_stop(ztm_api):
    data = ztm_api.get_stop_schedule_data('', '01', 1)
    assert data == []


def test_get_lines_for_bus_stop(ztm_api):
    data = ztm_api.get_lines_for_bus_stop('01')
    assert data is not None
