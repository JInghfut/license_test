# Activate the license using .lic file placed into local server - used for server license testing

import os
import subprocess
import render_test
import config

def setup_license():
    g = "C:\\Users\\Niall Buckley\\Desktop\\server_licenses"
    for subdir, dirs, files in os.walk(g):
        for license_file in files:
            print (license_file)
            cmd = 'robocopy "C:\\Users\\Niall Buckley\\Desktop\\server_licenses" "C:\\Program Files\\BorisFX\\rlm" ' + str(license_file)
            subprocess.call(cmd)
            #print(cmd + " LAA " + str(retVal))
            refresh_server()
            config.ConfigParams.file_line += 1
            render_test._run_render_test()
            remove_license(license_file)
            refresh_server()
            # remove license_file
            # refresh
        # mv g to C:\Program Files\BorisFX\rlm

def refresh_server():
    refreshCmd = 'curl localhost:5054/goforms/rlmreread_process'
    subprocess.call(refreshCmd)

def remove_license(license_file):
    deleteCmd ='del ' + '"C:\\Program Files\\BorisFX\\rlm\\' + str(license_file) + '"'
    subprocess.call(deleteCmd, shell=True)