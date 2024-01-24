import json
from global_def import *

test_swu_json_dic = {
    "swu_info_json_file_name": "json_file_name",
    "swu_file_name": "xxxx_xxxx_xxxx.swu",
}

'''
Definitions of json
'''
SUPPORT_SOC_BOARD_ANY = "any"
SUPPORT_MCU_BOARD_ANY = "any"
SUPPORT_SENSOR_BOARD_ANY = "any"
SUPPORT_SOC_SW_VERSION_ANY = "any"
SUPPORT_MCU_SW_VERSION_ANY = "any"

target_swu_json_dic = {
    "swu_info_json_file_name": "json_file_name",
    "swu_file_name": "xxxx_xxxx_xxxx.swu",
    "swu_file_uri": "/home/xxxx/xxxx/swu_file_name.swu",
    "swu_file_md5": "the md5sum of swu file",
    "supported_soc_board": ["any"],
    "supported_mcu_board": ["any"],
    "supported_sensor_board": ["any"],
    "supported_soc_sw_version": ["any"],
    "supported_mcu_sw_version": ["any"]
}


def gen_json_of_swu_info(**kwargs):
    # compare target_swu_json_dic and k
    keys = set(test_swu_json_dic.keys()).union(kwargs.keys())
    for key in keys:
        if not key in kwargs:
            print("missing key : %s" % key)
            return None

    # directly generate in install folde, no need to copy
    json_file = open("{}/{}".format(SWU_INSTALL_FOLDER, kwargs.get('swu_info_json_file_name')), "w")
    json.dump(kwargs, json_file, indent=2)
    return json_file


if __name__ == "__main__":
    gen_json_of_swu_info(swu_info_json_file_name="swu_info.json", swu_file_name="swu_version")


'''
json file format:

{
    "swu_inf_json_file_name" : "json_file_name",
    "swu_file_name" : "xxxx_xxxx_xxxx.swu", 
    "swu_file_uri" : "/home/xxxx/xxxx/swu_file_name.swu",
    "swu_file_md5" : "the md5sum of swu file" ,
    "swu_json_file_md5" : "the md5sum of swu json file", 
    "supported_soc_board" : [ "any" ],
    "supported_mcu_board" : [ "any" ],
    "supported_sensor_board" : [ "any" ],
    "supported_soc_sw_version" : [ "any" ],
    "supported_mcu_sw_version" : [ "any" ]
    
}
'''