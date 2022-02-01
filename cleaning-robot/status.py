from db import get_db
from services import air_service, robot_service


def get_status():
    data = {}

    # getting air
    air = air_service.get_air()
    data['air'] = air

    # getting the settings
    cleaning = robot_service.get_cleaning()['data']
    if cleaning is None:
        data['cleaning'] = 2
        data['settings'] = None
    else:
        settings = None
        if cleaning['type'] == 0:
            settings = robot_service.get_vacuum_settings(cleaning['settings_v'])
        else:
            settings = robot_service.get_vacuum_settings(cleaning['settings_m'])

    # getting the bin level
    bin_data = robot_service.get_bin_level()['data']
    data['bin_level'] = bin_data

    # getting the resource level
    resource_data = robot_service.get_resource_level()['data']
    data['resource_level'] = resource_data

    # getting the battery level
    battery_data = robot_service.get_battery_level()['data']
    data['battery_level'] = battery_data

    return {
        'data': data
    }
