import os
import config
import subprocess
import shlex
#import logging
#import test_main
#import results
import send_email
#import argparse
#import html_result_writer
#import install_mocha_ae
#import install_sapphire_ae
from shutil import copy
#import copy_results
#import copy_mocha_results
import time
import sys

# grab the git hash from build.xml in jenkins jobs folder
import xml.etree.ElementTree as ET

try:
    import faulthandler
    faulthandler.enable()
    print 'Faulthandler activated!'
except ImportError:
    print 'No Faulthandler available!'

import test_utils
if test_utils.is_mac():
    import mac_utils as plat_utils
elif test_utils.is_win():
    import win_utils as plat_utils


def install_latest_bcc_build():

    print ("install_latest_bcc_build")
    if test_utils.is_mac():
        config.ConfigParams.sub_build_install_path = config.ConfigParams.sub_build_install_path.replace('BCCAE', 'BCCOFX')

    #Find the latest installer
    latest_installer = ""
    inst_name = ''
    if os.path.isdir(config.ConfigParams.installer_search_path):
        latest_installer = get_latest_build_path(config.ConfigParams.installer_search_path)
        if latest_installer:
            for item in os.listdir(latest_installer):
                if test_utils.is_mac():
                    if item.endswith('.dmg'):
                        inst_name = item
                else:
                    if item.endswith('.exe'):
                        inst_name = item
    if inst_name != config.ConfigParams.installer_name:
        print ('Found a different installer name in search dir (' + inst_name + ') : using that one instead of ' + config.ConfigParams.installer_name)
        config.ConfigParams.installer_name = inst_name

    latest_installer = os.path.join(latest_installer, config.ConfigParams.installer_name)
    print ("latest installer")
    print (os.path.join(latest_installer, ''))
    dest_path = os.path.join(config.ConfigParams.base_directory, config.ConfigParams.installer_name)
    if config.ConfigParams.installer_name in os.listdir(config.ConfigParams.base_directory):
        os.remove(os.path.join(config.ConfigParams.base_directory, config.ConfigParams.installer_name))
    if os.path.isfile(latest_installer):
        copy(latest_installer, dest_path)
    else:
        print("ERROR: Latest installer was not found")
        return False

    # TODO: change to quit_app (to quit any of the potential hosts, rather than just AE)
    print("Quit AE if it is running")
    plat_utils.quit_ae(config.ConfigParams.target_app)

    print("Installing BCC Build from:{}".format(latest_installer))
    print ("Installing BCC Build from:{}".format(latest_installer))
    #results.TestResults.installed_build = latest_installer

    install_build(dest_path)
    return True

def install_build(installer_path):

    if test_utils.is_mac():
        # good for all Mac test systems
        volumes_dir = '/Volumes'
        volume_name = ''
        bcc_pkg_name = ''

        # Mount the disc image
        mount_cmd = "hdiutil attach " + installer_path
        time.sleep(3)
        retVal = os.system(mount_cmd)

        if (retVal != 0):
            print 'Did not mount on first try!'
            time.sleep(5)
            retVal = os.system(mount_cmd)

            if (retVal != 0):
                raise Exception('Failed to mount installer disc image')

        for item in os.listdir(volumes_dir):
            if item.find('Continuum') > -1:
                # for BCC search for 'Adobe' rather than 'AE'
                if item.find(config.ConfigParams.plugin_catagory) > -1 or item.find('Adobe') > -1:
                    volume_name = item
        if volume_name:
            volume_name = os.path.join(volumes_dir, volume_name)
            for item in os.listdir(volume_name):
                if item.find('Continuum') > -1:
                    if item.find(config.ConfigParams.plugin_catagory) > -1 or item.find('Adobe') > -1:
                        bcc_pkg_name = '"' + item + '"'

        # run the installer
        install_cmd = "installer -target / -package /Volumes/" + os.path.splitext(config.ConfigParams.installer_name)[0]  +  "/" + bcc_pkg_name
        full_cmd = "echo " +  config.ConfigParams.mac_admin_password + " | sudo -S " + install_cmd
        print (full_cmd)
        retVal = os.system(full_cmd)

        if(retVal != 0):
            raise Exception('Failed to run installer')

        #wait for install to finish?

        #Un-mount the disc image
        unmount_cmd = 'hdiutil unmount /Volumes/' + os.path.splitext(config.ConfigParams.installer_name)[0]
        retVal = os.system(unmount_cmd)

        if (retVal != 0):
            raise Exception('Failed to unmount installer volume')

    else:
        # Run the installer in silent
        print(installer_path)
        #cmd = str(installer_path) + ' /VERYSILENT  /SP-'
        #works!
        cmd = '"C:\\Users\\Niall Buckley\\Documents\\ae_test_env\\BCC13_AE_WinESD.exe"' + ' /VERYSILENT  /SP-'
        ret_val = subprocess.call(cmd)
        print("Finished running the silent install")


def get_latest_build_path(base_folder):
    # sets latest builds to search in either builds or jenkins/jobs (jobs is the better option)
    use_builds = False
    if use_builds:
        thehighest=-1
        returnfolder = ""
        for subdir, dirs, files in os.walk(base_folder,topdown=False):
            for dir in dirs:
                candidatefolder = os.path.join(base_folder, dir)
                #print (candidatefolder)
                if os.path.isdir(candidatefolder):
                    underscore_index = dir.rfind("_")
                    thisdirint = dir[underscore_index + 1:]
                    if thisdirint.find('OGL') > -1:
                        thisdirint = thisdirint[:3]
                        # temp: to force testing OGLshader perf test
                        # return candidatefolder
                    thisdirint = int(thisdirint)
                    if (thisdirint > thehighest):
                        thehighest = thisdirint
                        returnfolder = candidatefolder
                    # print ("found one")
        if (thehighest > -1):
            return returnfolder
    else:
        thisdirint = -1
        thehighest = -1
        for dir in os.listdir(base_folder):
            # for dir in dirs:
            candidatefolder = os.path.join(base_folder, dir)
            candidatefolder2 = os.path.join(candidatefolder, config.ConfigParams.sub_build_install_path)
            if os.path.isdir(candidatefolder2):
                if dir.find('Build') < 0:
                    if dir.find('.DS_Store') > -1:
                        dir = str(0)
                    thisdirint = int(dir)
                if (thisdirint > thehighest):
                    thehighest = thisdirint
        if (thehighest > -1):
            returnfolder1 = os.path.join(base_folder, str(thehighest))

            # grab the git hash while here!
            xml_file = os.path.join(returnfolder1, 'build.xml')
            if os.path.isfile(xml_file):
                tree = ET.parse(xml_file)
                root = tree.getroot()

                search_xml(root, 'sha1')
                print('\nGitHash = ' + config.ConfigParams.git_hash + '\n')

            else:
                print ('build.xml not present, no Git Hash available!?!')
            returnfolder2 = os.path.join(returnfolder1, config.ConfigParams.sub_build_install_path)
            config.ConfigParams.build_num = thehighest
            return returnfolder2
    return ""

# recursively search the xml tree for sha1 git hash
def search_xml(parent, id):
    for child in parent:
        if child.tag == id:
            config.ConfigParams.git_hash = child.text
            return
        else:
            search_xml(child, id)


def uninstall():
    #subprocess.call(["C:\Program Files\GenArts\SapphireAE\unins000.exe",  "/verysilent"])
    cmd = '"C:\\Program Files\\BorisFX\\ContinuumAE\\unins000.exe"' + ' /VERYSILENT'
    # print('py2 said:', py2output)
    ret_val = subprocess.call(cmd)


if __name__ == "__main__":

    try:
        config.ConfigParams.init_config()

        install_complete = False
        if(install_latest_bcc_build()):
            install_complete = True

        #Install the latest build, if that succeeds, run the tests
        if(install_complete):
            print("successfully installed!")

        #uninstall()
    except Exception as error:
        print("install_and_run_tests: {0}".format(repr(error)))
        #logging.error("install_and_run_tests: {0}".format(repr(error)))
        #send_email.error_email("install_and_run_tests: {0}".format(repr(error)), "bot@borisfx.com",
        #                       "joe.bruni@borisfx.com", str(config.ConfigParams.machine_name))

    except:
        print("install_and_run_tests, Unknown error thrown")
        #logging.error("install_and_run_tests, Unknown error thrown")
        #send_email.error_email("install_and_run_tests, Unknown error thrown", "bot@borisfx.com",
        #                       "joe.bruni@borisfx.com", str(config.ConfigParams.machine_name))

