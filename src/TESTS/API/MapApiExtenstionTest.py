from pytest import fixture
from src.API.Data.Extensions.MapApiExtension import MapApiExtension
from unittest.mock import MagicMock


@fixture
def map_api_extension():
    return MapApiExtension()


@fixture
def mock_geocode(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr('API.Data.Extensions.MapApiExtension.Nominatim.geocode', mock)
    return mock


@fixture
def mock_reverse_geocode(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr('API.Data.Extensions.MapApiExtension.Nominatim.reverse', mock)
    return mock


@fixture
def mock_serial(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr('API.Data.Extensions.MapApiExtension.serial.Serial', mock)
    return mock


@fixture
def mock_socket(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr('API.Data.Extensions.MapApiExtension.socket.socket', mock)
    return mock


@fixture
def mock_requests(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr('API.Data.Extensions.MapApiExtension.requests.get', mock)
    return mock


@fixture
def mock_distance(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr('API.Data.Extensions.MapApiExtension.geodesic', mock)
    return mock


def test_get_geocode_data(map_api_extension, mock_geocode):
    map_api_extension.get_geocode_data('Warsaw')
    mock_geocode.assert_called_once_with('Warsaw')


def test_get_geocode_data_invalid_address(map_api_extension):
    geocode_data = map_api_extension.get_geocode_data('')
    assert geocode_data is None


def test_geocode_data_for_valid_address(map_api_extension, mock_geocode):
    mock_geocode.return_value = MagicMock(latitude=40.7128, longitude=-74.0060)
    result = map_api_extension.get_geocode_data('New York')
    assert result is not None
    assert result.latitude == 40.7128
    assert result.longitude == -74.0060


def test_get_reverse_geocode_data(map_api_extension, mock_reverse_geocode):
    map_api_extension.get_reverse_geocode_data(52.2296756, 21.0122287)
    mock_reverse_geocode.assert_called_once_with((52.2296756, 21.0122287))


def test_get_reverse_geocode_data_invalid_coordinates(map_api_extension):
    reverse_geocode_data = map_api_extension.get_reverse_geocode_data(0, 0)
    assert reverse_geocode_data is None


def test_reverse_geocode_data_for_valid_coordinates(map_api_extension, mock_reverse_geocode):
    mock_reverse_geocode.return_value = MagicMock(address='New York, NY, USA')
    result = map_api_extension.get_reverse_geocode_data(40.7128, -74.0060)
    assert result is not None
    assert result.address == 'New York, NY, USA'


def test_get_distance(map_api_extension):
    distance = map_api_extension.get_distance('Warsaw', 'Krakow', 'km')
    assert distance is not None
    assert distance.km > 0


def test_get_distance_invalid_units(map_api_extension):
    distance = map_api_extension.get_distance('Warsaw', 'Krakow', 'invalid')
    assert distance is None


def test_get_distance_invalid_origin(map_api_extension):
    distance = map_api_extension.get_distance('', 'Krakow', 'km')
    assert distance is None


def test_get_distance_invalid_destination(map_api_extension):
    distance = map_api_extension.get_distance('Warsaw', '', 'km')
    assert distance is None


def test_get_distance_invalid_origin_and_destination(map_api_extension):
    distance = map_api_extension.get_distance('', '', 'km')
    assert distance is None


def test_get_distance_invalid_origin_and_destination_and_units(map_api_extension):
    distance = map_api_extension.get_distance('', '', 'invalid')
    assert distance is None


def test_get_distance_invalid_origin_and_units(map_api_extension):
    distance = map_api_extension.get_distance('', 'Krakow', 'invalid')
    assert distance is None


def test_parse_gpgga_valid_data():
    data = ['$GPGGA', '123456.00', '3749.1234', 'N', '12225.1234', 'W', '1', '12', '1.0', '0.0', 'M', '0.0', 'M', '', '*47']
    result = MapApiExtension.parse_gpgga(data)
    assert result is not None
    assert result['latitude'] == 3749.1234
    assert result['longitude'] == -12225.1234


def test_parse_gpgga_invalid_data():
    data = []
    result = MapApiExtension.parse_gpgga(data)
    assert result is None

