import csv
import datetime
import logging as log
from typing import List, Dict
from API.Data.Extensions.HelperDecoratorsExtension import handleexceptions

log.basicConfig(level=log.INFO, format='%(asctime)s - %(message)s')
log.getLogger().setLevel(log.DEBUG)
log.disable(log.NOTSET)


@handleexceptions
def save_to_csv(data: List[Dict[str, str]] | List[List[Dict[str, str]]], file_name: str) -> None:
    """
    This function is used to save the data to a csv file.
    :param data: The data to save.
    :param file_name: The name of the file.
    """
    if not data:
        log.error('No data to save')
        return

    date = datetime.datetime.now().strftime('%H%M%S')
    file_name = f'LLM/Data/Files/data_{file_name}_{date}.csv'

    if isinstance(data[0], dict):
        keys = data[0].keys()

        with open(file_name, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

    elif isinstance(data[0], list) and isinstance(data[0][0], dict):
        keys = data[0][0].keys()

        with open(file_name, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()

            for d in data:
                dict_writer.writerows(d)

    else:
        log.error('Invalid data format')
        return

    log.info(f'Data saved to {file_name}')

