from settings import auto_config as config
from sync import reader
from asynchronous import reader as areader
from common import timeit 
import json


@timeit
def download_sync():

    url_list = [f"{config.C4C_URL}/sap/c4c/odata/v1/customer/CorporateAccountCollection?$select=AccountID" for _ in range(20)]
    data = reader.read_from_odata((f'{config.C4C_USER}',f'{config.C4C_PWD}'), url_list)

    with open('test/files/test.json', 'w') as file:
        json.dump(data, file)


@timeit
def download_sync_chunk():

    url_list = [f"{config.C4C_URL}/sap/c4c/odata/v1/customer/CorporateAccountCollection?$select=AccountID" for _ in range(20)]
    data = reader.read_all_chunks_from_odata((f'{config.C4C_USER}',f'{config.C4C_PWD}'), url_list)

    with open('test/files/test_chunk.json', 'w') as file:
        json.dump(data, file)

   
@timeit
def download_async():
    url_list = [f"{config.C4C_URL}/sap/c4c/odata/v1/customer/CorporateAccountCollection?$select=AccountID" for _ in range(20)]
    data = areader.read_from_odata((f'{config.C4C_USER}',f'{config.C4C_PWD}'), url_list)

    with open('test/files/async_test_chunk.json', 'w') as file:
        json.dump(data, file)


def get_menu_option(min, max):
    while True:
        try:
            option = int(input('Option:'))
            if option < min or option > max:
                raise ValueError
            break
        except ValueError:
            print("Incorrect option")
    return option


def print_menu(options):
    for key,value in options.items():
        print(f"{key}. {value['label']}")
        

def menu():
    options = {
        1 : {'label' : 'Run sync', 'function' : download_sync}, 
        2 : {'label' : 'Run sync chunk', 'function' : download_sync_chunk}, 
        3 : {'label' : 'Run async', 'function' : download_async}, 
        4 : {'label' : 'Exit', 'function' : None},
    }
    print_menu(options)
    option = get_menu_option(1, len(options.keys()))
    return options[option]['function']


if __name__ == '__main__':

    while True:
        selected_option = menu()
        if selected_option is None:
            break
        selected_option()
        