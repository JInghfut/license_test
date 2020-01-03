# Activate the license using .lic file placed into local server - used for server license testing

import os
import subprocess
import render_test
import config
import mac_utils


def setup_license():
    print("base directory " + config.ConfigParams.base_directory)
    print("proj dir " + config.ConfigParams.proj_directory)
    # Need to find place for licenses.
    # g = config.ConfigParams.proj_directory + "license_test/Licenses/server_licenses"
    g = "/Users/borisfx/Desktop/server_licenses"
    # g = "C:\\Users\\Niall Buckley\\Desktop\\server_licenses"
    for subdir, dirs, files in os.walk(g, topdown=False):
        for license_file in files:
            if license_file != ".DS_Store":
                # copyCmd = 'robocopy "C:\\Users\\Niall Buckley\\Desktop\\server_licenses" "C:\\Program Files\\BorisFX\\rlm" ' + str(license_file)
                # subprocess.call(copyCmd)
                copyCmd = 'cp ' + str(g) + '/' + str(license_file) + " " + """ "/Library/Application Support/BorisFX/rlm/" """
                print("Command "+copyCmd)
                #copyCmd = 'cp /Users/borisfx/Desktop/DedupedData/ae_test_projects/license_test/Licenses/server_licenses/multiSapph.lic "/Library/Application Support/BorisFX/rlm/"'
                os.system(copyCmd)
                #subprocess.call(copyCmd)
                refresh_server()
                config.ConfigParams.file_line += 1
                render_test._run_render_test()
                # mac only issue!
                mac_utils.quit_ae(config.ConfigParams.target_app)
                remove_license(license_file)
                refresh_server()
                # remove license_file
                # refresh
            # mv g to C:\Program Files\BorisFX\rlm

def refresh_server():
    refreshCmd = 'curl localhost:5054/goforms/rlmreread_process'
    os.system(refreshCmd)

def remove_license(license_file):
    #deleteCmd ='del ' + '"C:\\Program Files\\BorisFX\\rlm\\' + str(license_file) + '"'
    deleteCmd = 'rm ' + '"/Library/Application Support/BorisFX/rlm/' + str(license_file) + '"'
    #subprocess.call(deleteCmd, shell=True)
    os.system(deleteCmd)