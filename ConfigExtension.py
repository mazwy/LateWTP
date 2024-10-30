import json
import logging as log
from functools import lru_cache

from API.Data.Extensions.HelperDecoratorsExtension import handleexceptions

log.basicConfig(level=log.INFO, format='%(asctime)s - %(message)s')
log.getLogger().setLevel(log.DEBUG)
log.disable(log.NOTSET)


@handleexceptions
@lru_cache(maxsize=32)
def load_config(section: str, subsection: str, key: str) -> str | None:
    """
    Load the config file
    :param section: The section of the config file.
    :param subsection: The subsection of the config file.
    :param key: The key of the config file.
    :return: The value of the key.
    """
    with open('conf.json') as file:
        data = json.load(file)
        value = data[section][subsection][key]
        if value is None:
            log.error(f'Value for {key} not found in {section}')
            return None

        return value


@handleexceptions
@lru_cache(maxsize=32)
def load_logging_config(subsection: str, key: str) -> str | None:
    """
    Load the logging config file
    :param subsection: The subsection of the config file.
    :param key: The key of the config file.
    :return: The value of the key.
    """
    with open('conf.json') as file:
        data = json.load(file)
        value = data['logging'][subsection][key]
        if value is None:
            log.error(f'Value for {key} not found in logging')
            return None

        return value
