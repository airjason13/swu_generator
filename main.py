# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import re
import sys
import hashlib
from global_def import *


def get_sample_gen_swu():
    root_dir = os.path.dirname(sys.modules['__main__'].__file__)
    with open(os.path.join(root_dir, "materials/sample_gen_swu.sh"), "r") as f:
        lines = f.readlines()
    f.close()
    return lines


def get_sample_sw_description():
    root_dir = os.path.dirname(sys.modules['__main__'].__file__)
    with open(os.path.join(root_dir, "materials/sample-sw-description"), "r") as f:
        lines = f.readlines()
    f.close()
    return lines


def get_sample_run_eduarts():
    root_dir = os.path.dirname(sys.modules['__main__'].__file__)
    with open(os.path.join(root_dir, "materials/sample_run_EDUARTS.sh"), "r") as f:
        lines = f.readlines()
    f.close()
    return lines


def get_file_sha256sum(file_name):
    root_dir = os.path.dirname(sys.modules['__main__'].__file__)
    sha256_hash = hashlib.sha256()
    with open(os.path.join(root_dir, file_name), "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


def write_sw_descrption(lines):
    root_dir = os.path.dirname(sys.modules['__main__'].__file__)
    with open(os.path.join(root_dir, "materials/sw-description"), "w") as f:
        f.writelines(lines)
        f.flush()
        f.truncate()
        f.close()


def rework_sw_description_lines(tmp_lines, rework_file_name, is_source_code=False):
    update_sh_sha256sum = get_file_sha256sum(rework_file_name)
    print("rework_file_name:", rework_file_name)
    print("sha255sum = ", update_sh_sha256sum)
    real_file_name = rework_file_name.split("/")[1]
    b_update_sha256sum = False
    for n in range(len(tmp_lines)):
        if is_source_code is True:
            if SOURCE_CODE_FOLDER_PREFIX in tmp_lines[n] and "filename" in tmp_lines[n]:
                old_fname = tmp_lines[n].split("=")[1]
                print("old_fname:", old_fname)
                tmp_lines[n] = tmp_lines[n].replace(old_fname, ' "' + real_file_name + '"; \n')
                b_update_sha256sum = True
            elif SOURCE_CODE_FOLDER_PREFIX in tmp_lines[n] and "path" in tmp_lines[n]:
                m = tmp_lines[n].split("/")
                old_fname = m[len(m) - 1]
                print("old_fname:", old_fname)
                tmp_lines[n] = tmp_lines[n].replace(old_fname,  real_file_name + '"; \n')
        else:
            if real_file_name in tmp_lines[n]:
                b_update_sha256sum = True
        if b_update_sha256sum is True:
            if "sha256 = " in tmp_lines[n]:
                tmp = tmp_lines[n].split("=")[1]
                # print("tmp :", tmp)
                tmp_lines[n] = tmp_lines[n].replace(tmp, ' "' + update_sh_sha256sum + '"; \n')
                print("replace")
                b_update_sha256sum = False
    return tmp_lines


def rework_update_sh(scode_folder_name):
    update_sh_lines = ["#!/bin/sh \n",
                       "tar -xvf /home/eduarts/swupdate_binary/"
                       + scode_folder_name + ".tar.gz "
                       + "-C /home/eduarts/geany_code/ \n",
                       "cp /home/eduarts/swupdate_binary/run_EDUARTS.sh /usr/bin/ \n",
                       "echo update.... \n"]
    print("update_sh_lines = ", update_sh_lines)
    with open(os.path.join(root_dir, "materials/update.sh"), "w") as f:
        f.writelines(update_sh_lines)
        f.flush()
        f.truncate()
        f.close()


def rework_run_eduarts_script(tmp_lines : list[str], scode_folder_name):
    for n in range(len(tmp_lines)):
        if "cd /home/eduarts/geany_code" in tmp_lines[n]:
            tmp_str_list = tmp_lines[n].split("/")
            old_folder_name = tmp_str_list[len(tmp_str_list) - 1]
            tmp_lines[n] = tmp_lines[n].replace(old_folder_name, scode_folder_name + '\n')

    with open(os.path.join(root_dir, "materials/run_EDUARTS.sh"), "w") as f:
        f.writelines(tmp_lines)
        f.flush()
        f.truncate()
        f.close()


def get_source_code_version(scode_folder_name):
    ver_year = ""
    ver_month = ""
    ver_day = ""
    ver_major = ""
    ver_minor = ""

    print("scode_folder_name :", scode_folder_name)
    print("scode_folder_name :", os.path.join(root_dir, scode_folder_name + "/CONST.py"))
    with open(os.path.join(root_dir, scode_folder_name + "/CONST.py" ), "r") as f:
        lines = f.readlines()
        for line in lines :
            if line.startswith("VER_MAJOR"):
                ver_major = line.split(" = ")[1].strip("\n")
            if line.startswith("VER_MINOR"):
                ver_minor = line.split(" = ")[1].strip("\n")
            if line.startswith("VER_YEAR"):
                ver_year = line.split(" = ")[1].strip("\n")
            if line.startswith("VER_MONTH"):
                ver_month = line.split(" = ")[1].strip("\n")
            if line.startswith("VER_DAY"):
                ver_day = line.split(" = ")[1].strip("\n")

    print("ver_major : ", ver_major)
    print("ver_minor : ", ver_minor)
    print("ver_year : ", ver_year)
    print("ver_month : ", ver_month)
    print("ver_day : ", ver_day)

    return ver_year, ver_month, ver_day, ver_major, ver_minor


def rework_gen_swu(tmp_lines: list[str], update_file_lists, yyyy, mm, dd, major, minor):
    for n in range(len(tmp_lines)):
        if tmp_lines[n].startswith("CONTAINER_VER"):
            tmp_lines[n] = 'CONTAINER_VER="' + yyyy + '_' + mm + '_' + dd + '_' + major + '_' + minor + '"\n'
        if tmp_lines[n].startswith("FILES="):
            tmp_lines[n] = "FILES=" + '"sw-description \\\n'
            tmp_lines.insert(n + 1, '       ' + "sw-description.sig \\\n")
            for l in range(len(update_file_lists)):
                if l == len(update_file_lists) - 1:
                    tmp_lines.insert(n + 2 + l, '       ' + update_file_lists[l] + ' "\n')
                else:
                    tmp_lines.insert(n + 2 + l, '       ' + update_file_lists[l] + ' \\\n')

    with open(os.path.join(root_dir, "materials/gen_swu.sh"), "w") as f:
        f.writelines(tmp_lines)
        f.flush()
        f.truncate()
        f.close()


def get_update_files_list(sw_desc_lines: list[str]):
    files_list = []
    for n in sw_desc_lines:
        if n.strip(" ").startswith("filename"):
            # print("n : ", n)
            fname = n.split('"')[1]
            # print("fname : ", fname)
            files_list.append(fname)
    return files_list


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    '''Handle the source code'''
    '''Find the source first'''
    source_code_folder_name = None
    # root_dir = os.path.dirname(sys.modules['__main__'].__file__)
    for f in os.listdir(root_dir):
        if f.startswith(SOURCE_CODE_FOLDER_PREFIX):
            source_code_folder_name = f
            cmd = "tar -czf materials/" + source_code_folder_name + ".tar.gz " + source_code_folder_name
            os.system(cmd)
            os.sync()

    '''get source code version '''
    (edb_source_code_ver_year, edb_source_code_ver_month, edb_source_code_ver_day,
     edb_source_code_ver_major, edb_source_code_ver_minor) = get_source_code_version(source_code_folder_name)

    '''Handle the update.sh & run_EDUARTS.sh'''
    rework_update_sh(source_code_folder_name)
    run_eduarts_sh_lines = get_sample_run_eduarts()
    rework_run_eduarts_script(run_eduarts_sh_lines, source_code_folder_name)

    ''' Handle sw-description '''
    sw_description_lines = get_sample_sw_description()
    print(sw_description_lines)

    sw_description_lines = rework_sw_description_lines(sw_description_lines,
                                                       "materials/" + source_code_folder_name + ".tar.gz",
                                                       is_source_code=True)
    sw_description_lines = rework_sw_description_lines(sw_description_lines,
                                                       "materials/update.sh")
    sw_description_lines = rework_sw_description_lines(sw_description_lines,
                                                       "materials/system_update_fhd.mp4")
    sw_description_lines = rework_sw_description_lines(sw_description_lines,
                                                       "materials/run_EDUARTS.sh")
    sw_description_lines = rework_sw_description_lines(sw_description_lines,
                                                       "materials/show")
    sw_description_lines = rework_sw_description_lines(sw_description_lines,
                                                       "materials/pre-install.sh")
    sw_description_lines = rework_sw_description_lines(sw_description_lines,
                                                       "materials/post-install.sh")

    write_sw_descrption(sw_description_lines)

    '''TODO: Get update file list from sw-description'''
    update_file_list = get_update_files_list(sw_description_lines)
    print("update_file_list : ", update_file_list)

    '''rework gen_swu.sh'''
    gen_swu_sample_lines = get_sample_gen_swu()
    print(gen_swu_sample_lines)
    rework_gen_swu(gen_swu_sample_lines, update_file_list, edb_source_code_ver_year,
                   edb_source_code_ver_month, edb_source_code_ver_day,
                   edb_source_code_ver_major, edb_source_code_ver_minor)







