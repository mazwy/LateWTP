from API.Data.Extensions import CsvDataExtension
from API.Data.Extensions.ZtmApiExtension import ZtmApiExtension
from API.Data.Extensions.MapApiExtension import MapApiExtension


def main():
    # api_extension = ZtmApiExtension()
    # bus_512 = api_extension.get_vehicles_location_data('512', 1, 100)
    #
    # CsvDataExtension.save_to_csv(bus_512, 'bus_512')
    print(MapApiExtension().get_geocode_data('Warszawa'))


if __name__ == '__main__':
    main()
