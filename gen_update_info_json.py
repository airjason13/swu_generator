import glob
import hashlib
import json
from global_def import *


class SwuJsonData(object):
    def __init__(self, fname, md5):
        self.name = fname
        self.md5sum = md5

    def swu_json_decoder(obj):
        return SwuJsonData(obj['name'], obj['md5sum'])

    def get_infomations(self):
        return self.name, self.md5sum


# get the swu & json flies list
def get_swu_json_files_list(path=SWU_INSTALL_FOLDER) -> list:
    json_list = []
    tmp_json_list = []
    swu_list = []
    json_search_key = path + "/*.json"
    swu_search_key = path + "/*.swu"
    for fname in sorted(glob.glob(json_search_key), reverse=True):
        tmp_json_list.append(fname)
    print("before json_list : %s " % tmp_json_list)
    for fname in sorted(glob.glob(swu_search_key), reverse=True):
        swu_list.append(fname)
    print("before swu_list : %s " % swu_list)

    for i in range(len(tmp_json_list)):
        print("i : %d" % i)
        if tmp_json_list[i].replace(".json", ".swu") in swu_list:
            json_list.append(tmp_json_list[i])

    print("rework json_list : %s " % json_list)
    return json_list


def get_update_jsons_list():
    ''' least_data = {"least_swu_file_json": SwuJsonData("aaaa", "md5").get_infomations()}
    older_data = {"old_ver_swu_file_jsons": [SwuJsonData("aaaa", "md5").get_infomations(),
                                            SwuJsonData("aaaa", "md5").get_infomations(),
                                            SwuJsonData("aaaa", "md5").get_infomations()]
                    } '''
    total_data = {"least_swu_file_json": [],
                  "old_ver_swu_file_jsons": []}
    json_list = get_swu_json_files_list()

    for i in range(len(json_list)):
        if i == 0:
            # Open,close, read file and calculate MD5 on its contents
            with open(json_list[i], 'rb') as file_to_check:
                # read contents of the file
                data = file_to_check.read()
                # pipe contents of the file through
                md5_returned = hashlib.md5(data).hexdigest()
            tmp_name, tmp_md5 = SwuJsonData(json_list[i], md5_returned).get_infomations()
            data_dict = {"name": tmp_name, "md5": tmp_md5}
            total_data["least_swu_file_json"].append(data_dict)
        else:
            # Open,close, read file and calculate MD5 on its contents
            with open(json_list[i], 'rb') as file_to_check:
                # read contents of the file
                data = file_to_check.read()
                # pipe contents of the file through
                md5_returned = hashlib.md5(data).hexdigest()
            tmp_name, tmp_md5 = SwuJsonData(json_list[i], md5_returned).get_infomations()
            data_dict = {"name": tmp_name, "md5": tmp_md5}
            total_data["old_ver_swu_file_jsons"].append(data_dict)
    print(total_data)
    json_file = open("{}/{}".format(SWU_INSTALL_FOLDER, 'Eudarts_update_data.json'), "w")
    json.dump(total_data, json_file, indent=2)


if __name__ == '__main__':
    with open('test.json') as json_file:
        #data = json.load(json_file)

        #print(" data :\n", dict(data['least_swu_file_json'][0]))
        #print(" data_list :\n", dict(data['old_ver_swu_file_jsons'][0]))

        #get_swu_json_files_list()
        get_update_jsons_list()

'''
json file format:
{

  "least_swu_file_json": [
    {
      "name": "Eudarts_YYYY_MM_DD_MAJOR_MINOR.json",
      "md5sum": "md5sum of Eudarts_YYYY_MM_DD_MAJOR_MINOR.json"
    }
  ],
  "old_ver_swu_file_jsons": [
    {
      "name": "Eudarts_YYYY_MM_DD_MAJOR_MINOR.json",
      "md5sum": "md5sum of Eudarts_YYYY_MM_DD_MAJOR_MINOR.json"
    },
    {
      "name": "Eudarts_YYYY_MM_DD_MAJOR_MINOR.json",
      "md5sum": "md5sum of Eudarts_YYYY_MM_DD_MAJOR_MINOR.json"
    },
    {
      "name": "Eudarts_YYYY_MM_DD_MAJOR_MINOR.json",
      "md5sum": "md5sum of Eudarts_YYYY_MM_DD_MAJOR_MINOR.json"
    }
  ]
}
'''
