import logging as log
from src import ConfigExtension as config
from src.API.Data.Extensions.HelperDecoratorsExtension import handleexceptions

log.basicConfig(level=log.INFO, format='%(asctime)s - %(message)s')


@handleexceptions
def build_api_url_ztm(api_key=None, vehicle_type=None, line=None, brigade=None, stop_id=None):
    """
    This function is used to build the url for the api.
    :param api_key: api key.
    :param vehicle_type: 1 for bus, 2 for tram.
    :param line: e.g. 512
    :param brigade: e.g. 1
    :param stop_id: e.g. 7000
    :return: url for the api.
    """
    bus_tram_url = config.load_config('api', 'api_urls', 'ztm_bus_tram_url')
    stop_url = config.load_config('api', 'api_urls', 'ztm_stop_url')

    if api_key is None:
        log.error('Api key is required')
        return None

    if stop_id is not None:
        url = (f'{stop_url}/?id=ab75c33d-3a26-4342-b36a-6e5fef0a3ac3'
               f'&apikey={api_key}&busstopId={stop_id}')
    else:
        url = (f'{bus_tram_url}?resource_id=f2e5503e927d-4ad3-9500-4ab9e55deb59'
               f'&apikey={api_key}&type={vehicle_type}&line={line}&brigade={brigade}')

    return url
