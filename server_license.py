# Activate the license using .lic file placed into local server - used for server license testing

import os
import subprocess
import render_test
import config
import mac_utils
import test_utils


def setup_license():
    print("base directory " + config.ConfigParams.base_directory)
    print("proj dir " + config.ConfigParams.proj_directory)
    # Need to find place for licenses.
    # g = config.ConfigParams.proj_directory + "license_test/Licenses/server_licenses"
    # g = "~/Desktop/server_licenses" 
    g = config.ConfigParams.license_test_dir + "\\server_licenses"
    print(g)
    # g = "C:\\Users\\Niall Buckley\\Desktop\\server_licenses"
    for subdir, dirs, files in os.walk(g, topdown=False):
        for license_file in files:
            if license_file != ".DS_Store":
                if test_utils.is_mac():
                    copyCmd = 'cp ' + str(g) + '/' + str(license_file) + " " + """ "/Library/Application Support/BorisFX/rlm/" """
                    print("Command " + copyCmd)
                    os.system(copyCmd)
                elif test_utils.is_win():
                    copyCmd = 'robocopy "C:\\Users\\Niall Buckley\\Desktop\\server_licenses" "C:\\Program Files\\BorisFX\\rlm" ' + str(license_file)
                    subprocess.call(copyCmd)
                # copyCmd = 'robocopy "C:\\Users\\Niall Buckley\\Desktop\\server_licenses" "C:\\Program Files\\BorisFX\\rlm" ' + str(license_file)
                # subprocess.call(copyCmd)
                #copyCmd = 'cp /Users/borisfx/Desktop/DedupedData/ae_test_projects/license_test/Licenses/server_licenses/multiSapph.lic "/Library/Application Support/BorisFX/rlm/"'
                #subprocess.call(copyCmd)
                refresh_server()
                config.ConfigParams.file_line += 1
                render_test._run_render_test()
                if test_utils.is_mac():
                    mac_utils.quit_ae(config.ConfigParams.target_app)
                remove_license(license_file)
                # refresh_server()

def refresh_server():
    refreshCmd = 'curl localhost:5054/goforms/rlmreread_process'
    if test_utils.is_win():
        subprocess.call(refreshCmd)
    elif test_utils.is_mac():
        os.system(refreshCmd)

def remove_license(license_file):
    #deleteCmd ='del ' + '"C:\\Program Files\\BorisFX\\rlm\\' + str(license_file) + '"'
    if test_utils.is_win():
        deleteCmd = 'del ' + '"C:\\Program Files\\BorisFX\\rlm\\' + str(license_file) + '"'
        subprocess.call(deleteCmd, shell=True)
    elif test_utils.is_mac():
        deleteCmd = 'rm ' + '"/Library/Application Support/BorisFX/rlm/' + str(license_file) + '"'
        os.system(deleteCmd)