import argparse
import os
import config
import subprocess
import activate_license
import sapphire_install
import shlex
# import logging
# import test_main
# import results
# import send_email
# import argparse
# import html_result_writer
# import install_mocha_ae
# import install_sapphire_ae
from shutil import copy
# import copy_results
# import copy_mocha_results
import time
# import sys

# grab the git hash from build.xml in jenkins jobs folder
import xml.etree.ElementTree as ET

import server_license

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


def handle_cmd_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mocha", help="override config file to run tests for mocha", action='store_true')
    parser.add_argument('--sapphire', help='override config file to run tests for Sapphire', action='store_true')
    parser.add_argument('--pprobcc', help='override config file to run tests for Premiere Pro render test',
                        action='store_true')
    parser.add_argument('--pprosapphire', help='override config file to run tests for Premiere Pro render test',
                        action='store_true')
    parser.add_argument("--mochaserver", help="override config file to run tests for mocha", action='store_true')
    parser.add_argument("--sapphireserver", help="override config file to run tests for mocha", action='store_true')
    parser.add_argument("--bccserver", help="override config file to run tests for mocha", action='store_true')

    # OFX cmds:
    parser.add_argument("--nukerender", help='', action='store_true')
    parser.add_argument("--nukesapphirerender", help='', action='store_true')

    args = parser.parse_args()

    if args.mocha:
        #config.ConfigParams.html_results_filename = "MPP4BCC-AE_render_results_"
        #config.ConfigParams.log_file_name = 'mpp4ae_render_'
        config.ConfigParams.plugin_install = 'Mocha-AE'
        config.ConfigParams.run_installed_plugins_test = False
        config.ConfigParams.lic_test_type = 'serial'
        config.ConfigParams.render_test_directories = config.ConfigParams.mocha_lic_test
        config.ConfigParams.copy_mocha_results = True
        config.ConfigParams.copy_results = False
        # config.ConfigParams.license_path = '"C:\\Program Files\\Adobe\\Common\\Plug-ins\\7.0\\MediaCore\\BorisFX\\MochaPro2020.5\\SharedResources\\bfx-license-tool\\bfx-license-tool"' + ' --feature mocha'
        config.ConfigParams.license_path = config.ConfigParams.mocha_licensing_path

    elif args.mochaserver:
        #config.ConfigParams.html_results_filename = "MPP4BCC-AE_render_results_"
        #config.ConfigParams.log_file_name = 'mpp4ae_render_'
        config.ConfigParams.plugin_install = 'Mocha-AE'
        config.ConfigParams.run_installed_plugins_test = False
        config.ConfigParams.lic_test_type = 'server'
        config.ConfigParams.render_test_directories = config.ConfigParams.mocha_lic_test
        config.ConfigParams.copy_mocha_results = True
        config.ConfigParams.copy_results = False
        # config.ConfigParams.license_path = '"C:\\Program Files\\Adobe\\Common\\Plug-ins\\7.0\\MediaCore\\BorisFX\\MochaPro2020.5\\SharedResources\\bfx-license-tool\\bfx-license-tool"' + ' --feature mocha'
        config.ConfigParams.license_path = config.ConfigParams.mocha_licensing_path

    elif args.sapphire:
        #config.ConfigParams.html_results_filename = "Sapphire_render_results_"
        #config.ConfigParams.log_file_name = 'sapphire_render_'
        config.ConfigParams.plugin_install = 'Sapphire-AE'
        config.ConfigParams.run_installed_plugins_test = False
        # config.ConfigParams.mocha_render_test = True
        config.ConfigParams.lic_test_type = 'serial'
        config.ConfigParams.render_test_directories = config.ConfigParams.sapphire_lic_test
        # print('config.ConfigParams.render_test_directories ' + str(config.ConfigParams.render_test_directories))
        # config.ConfigParams.license_path = '"C:\\Program Files\\GenArts\\SapphireAE\\license-tool\\license-tool"'
        config.ConfigParams.license_path = config.ConfigParams.sapph_licensing_path
        # shortens the proj length to 5 frames for the render tests
        #   Come back to!!!! OKKKAAYYy
        # config.ConfigParams.render_test_script = os.path.join(config.ConfigParams.base_directory, "ae_scripts/render_sapph_test_tiff.jsx")

    elif args.sapphireserver:
        #config.ConfigParams.html_results_filename = "Sapphire_render_results_"
        #config.ConfigParams.log_file_name = 'sapphire_render_'
        config.ConfigParams.plugin_install = 'Sapphire-AE'
        config.ConfigParams.run_installed_plugins_test = False
        # config.ConfigParams.mocha_render_test = True
        config.ConfigParams.lic_test_type = 'server'
        config.ConfigParams.render_test_directories = config.ConfigParams.sapphire_lic_test
        # print('config.ConfigParams.render_test_directories ' + str(config.ConfigParams.render_test_directories))
        # config.ConfigParams.license_path = '"C:\\Program Files\\GenArts\\SapphireAE\\license-tool\\license-tool"'
        config.ConfigParams.license_path = config.ConfigParams.sapph_licensing_path
        # shortens the proj length to 5 frames for the render tests
        #   Come back to!!!!
        # config.ConfigParams.render_test_script = os.path.join(config.ConfigParams.base_directory, "ae_scripts/render_sapph_test_tiff.jsx")
        # Delete This also This This This This This This This

    elif args.bccserver:
        config.ConfigParams.render_test_directories = config.ConfigParams.bcc_lic_test
        config.ConfigParams.license_path = config.ConfigParams.bcc_licensing_path
        config.ConfigParams.plugin_install = 'BCC-AE'
        config.ConfigParams.lic_test_type = 'server'

    elif args.pprobcc:
        config.ConfigParams.html_results_filename = "ppro_render_test_results"
        config.ConfigParams.log_file_name = 'ppro_render'
        # config.ConfigParams.plugin_install = 'BCC'
        config.ConfigParams.run_installed_plugins_test = False
        # Set the application and tests to run to premiere pro:
        config.ConfigParams.license_path = config.ConfigParams.bcc_licensing_path
        config.ConfigParams.run_ppro_tests = True

    else:
        config.ConfigParams.render_test_directories = config.ConfigParams.bcc_lic_test
        # config.ConfigParams.license_path = '"C:\\Program Files\\BorisFX\ContinuumAE\\13\\utilities\\bfx-license-tool\\bfx-license-tool"' + ' --feature bcc'
        config.ConfigParams.license_path = config.ConfigParams.bcc_licensing_path
        config.ConfigParams.plugin_install = 'BCC-AE'
        config.ConfigParams.lic_test_type = 'serial'


def install_latest_bcc_build():
    print ("install_latest_bcc_build")
    if test_utils.is_mac():
        config.ConfigParams.sub_build_install_path = config.ConfigParams.sub_build_install_path.replace('BCCAE',
                                                                                                        'BCCOFX')

    # Find the latest installer
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
        print (
                    'Found a different installer name in search dir (' + inst_name + ') : using that one instead of ' + config.ConfigParams.installer_name)
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
    # results.TestResults.installed_build = latest_installer

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
        install_cmd = "installer -target / -package /Volumes/" + os.path.splitext(config.ConfigParams.installer_name)[
            0] + "/" + bcc_pkg_name
        full_cmd = "echo " + config.ConfigParams.mac_admin_password + " | sudo -S " + install_cmd
        print (full_cmd)
        retVal = os.system(full_cmd)

        if (retVal != 0):
            raise Exception('Failed to run installer')

        # wait for install to finish?

        # Un-mount the disc image
        unmount_cmd = 'hdiutil unmount /Volumes/' + os.path.splitext(config.ConfigParams.installer_name)[0]
        retVal = os.system(unmount_cmd)

        if (retVal != 0):
            raise Exception('Failed to unmount installer volume')

    else:
        # Run the installer in silent
        print(installer_path)
        # cmd = str(installer_path) + ' /VERYSILENT  /SP-'
        # works!
        cmd = '"C:\\Users\\Niall Buckley\\Documents\\ae_test_env\\BCC13_AE_WinESD.exe"' + ' /VERYSILENT  /SP-'
        ret_val = subprocess.call(cmd)
        print("Finished running the silent install")
        # activate_license.activate_license(1397-3766-7629-7051)
        activate_license.find_license()


def get_latest_build_path(base_folder):
    # sets latest builds to search in either builds or jenkins/jobs (jobs is the better option)
    use_builds = False
    if use_builds:
        thehighest = -1
        returnfolder = ""
        for subdir, dirs, files in os.walk(base_folder, topdown=False):
            for dir in dirs:
                candidatefolder = os.path.join(base_folder, dir)
                # print (candidatefolder)
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
    # subprocess.call(["C:\Program Files\GenArts\SapphireAE\unins000.exe",  "/verysilent"])
    cmd = '"C:\\Program Files\\BorisFX\\ContinuumAE\\unins000.exe"' + ' /VERYSILENT'
    # print('py2 said:', py2output)
    ret_val = subprocess.call(cmd)


if __name__ == "__main__":

    try:
        config.ConfigParams.init_config()

        # Handle command line args
        handle_cmd_args()

        install_complete = True

        # Install the latest build, if that succeeds, run the tests

        # check if Mocha install or BCC install
        # if (config.ConfigParams.plugin_install == 'Mocha-AE'):
        #    if (install_mocha_ae.install_MochaAE()):
        #        # point to correct file structue here?
        #        install_complete = True
        #        email_mocha = True

        #if (config.ConfigParams.plugin_install == 'Sapphire'):
        #    if (sapphire_install.install_SapphireAE()):
        #        install_complete = True

        #if config.ConfigParams.plugin_install == 'BCC':
        #    if install_latest_bcc_build():
        #       install_complete = True

        if (install_complete):
            print("successfully installed!")
            # need change name to from activate_license to serial_license
            if config.ConfigParams.lic_test_type == 'server':
                server_license.setup_license()
            elif config.ConfigParams.lic_test_type == 'serial':
                activate_license.find_license()
            # if server test:

        # uninstall()
    except Exception as error:
        print("install_and_run_tests: {0}".format(repr(error)))
        # logging.error("install_and_run_tests: {0}".format(repr(error)))
        # send_email.error_email("install_and_run_tests: {0}".format(repr(error)), "bot@borisfx.com",
        #                       "joe.bruni@borisfx.com", str(config.ConfigParams.machine_name))

    except:
        print("install_and_run_tests, Unknown error thrown")
        # logging.error("install_and_run_tests, Unknown error thrown")
        # send_email.error_email("install_and_run_tests, Unknown error thrown", "bot@borisfx.com",
        #                       "joe.bruni@borisfx.com", str(config.ConfigParams.machine_name))
