# Download and Install MochaAE Script (Mac and Win)
# A NOTE ON rclone:
#       use / slashes for files paths!  Will not work otherwise
import shlex, subprocess
import os
# to tell if Mac/Win
import test_utils
import config
import logging

if test_utils.is_mac():
    import mac_utils as plat_utils
elif test_utils.is_win():
    import win_utils as plat_utils


def install_MochaAE():
    cmd = ''
    # list builds in store and filter by age to make naming consistent
    if test_utils.is_mac():
        cmd = config.ConfigParams.rclone_cmd + ' ls mac_auto_test:store/ReleaseBuilds/mocha-adobe/mac_uni/AutomatedBuilds --max-age 2M'
    elif test_utils.is_win():
        # for Auto_QA machine, auto-test-win has a different path: config.ConfigParams.rclone_cmd
        cmd = '"C:/Users/Niall Buckley/Documents/ae_test_env/rclone-v1.50.2-windows-amd64/rclone"' + ' ls win_auto_test:store/ReleaseBuilds/mocha-adobe/win_x86_64/AutomatedBuilds --max-age 2M'
    cmd2 = shlex.split(cmd)
    # store builds as a string
    print config.ConfigParams.rclone_cmd
    print cmd2
    installer_list = subprocess.check_output(cmd2)
    # splitting based off of only most recent file naming scheme
    import re
    split_list = re.split(' |-|\.', installer_list)
    i = 0
    build_str_list = []
    # confirm version number and put build number in build_str_list
    # find build version 5.6.1
    for word in split_list:
        if ((word == '7') and (split_list[i + 1] == '0') and (split_list[i + 2] == '3Prerelease')):
            build_str_list.append(split_list[i + 3])
        i += 1
    build_num_list = []
    j = 0
    # convert the build numbers to ints for sorting
    for num in build_str_list:
        build_num_list.append(int(build_str_list[j]))
        j += 1
    build_num_list.sort(reverse=True)
    # create a regex to find the git hash of the build
    searcher = r'(?<=MochaPro2020-Adobe-7.0.3Prerelease)-' + str(build_num_list[0]) + '\..*'
    # use the regex to sort the installer names
    hash_info = re.search(searcher, installer_list)
    # set the build number
    config.ConfigParams.build_num = build_num_list[0]
    m_installer_name = 'MochaPro2020-Adobe-7.0.3Prerelease' + hash_info.group(0)
    print 'Installing file:' + m_installer_name
    logging.info("Installing Mocha Build:{}".format(m_installer_name))
    #results.TestResults.installed_build = m_installer_name
    print("Quit AE if it is running")
    plat_utils.quit_ae(config.ConfigParams.target_app)
    # download and install newest 5.6.0 build
    if test_utils.is_mac():
        mac_copy_cmd = config.ConfigParams.rclone_cmd + ' copy mac_auto_test:store/ReleaseBuilds/mocha-adobe/mac_uni/AutomatedBuilds/' + m_installer_name + ' /Users/borisfx/Documents/ae_test_env'
        install_path = '/Users/borisfx/Documents/ae_test_env/' + m_installer_name
        s_copy_cmd = shlex.split(mac_copy_cmd)
        print install_path
        # Mac Only
        # remove the .dmg from the end of the disk-image name to get the installer name
        volume_name_mac = m_installer_name[:-4]
        # Mac pkg name:
        mocha_pkg_name = 'mochaAdobe.pkg'
        # copy over newest build to designated folder
        subprocess.call(s_copy_cmd)
        # mount disk image
        mount_cmd = 'hdiutil attach ' + install_path
        s_mount_cmd = shlex.split(mount_cmd)
        retVal = subprocess.call(s_mount_cmd)
        if (retVal != 0):
            raise Exception('Failed to run installer')
        # os.path.splitext(config.ConfigParams.installer_name)[0]
        # run the installer
        install_cmd = "installer -target / -package /Volumes/" + volume_name_mac + '/' + mocha_pkg_name
        full_cmd = "echo " + config.ConfigParams.mac_admin_password + " | sudo -S " + install_cmd
        retVal = os.system(full_cmd)
        if (retVal != 0):
            raise Exception('Failed to run installer')
        # unmount the installed volume
        unmount_cmd = shlex.split('hdiutil unmount ' + '/Volumes/' + volume_name_mac)
        subprocess.call(unmount_cmd)
    elif test_utils.is_win():
        # replace below line w/ reference to config? config.ConfigParams.rclone_cmd
        copy_cmd = '"C:/Users/Niall Buckley/Documents/ae_test_env/rclone-v1.50.2-windows-amd64/rclone"' + ' copy win_auto_test:store/ReleaseBuilds/mocha-adobe/win_x86_64/AutomatedBuilds/' + m_installer_name + ' "C:/Users/Niall Buckley/Documents/ae_test_env"'
        shlex.split(copy_cmd)
        # copy over newest build to designated folder
        print(copy_cmd)
        subprocess.call(copy_cmd)
        # silent install?
        install_cmd = 'msiexec /qb /i "C:\\Users\\Niall Buckley\\Documents\\ae_test_env\\' + m_installer_name + '"' + ' INSTALLLOCATION="C:\\Program Files\\Adobe\\Common\\Plug-ins\\7.0\\MediaCore" && echo "OK installed"'
        # install2 = shlex.split(install_cmd)
        print 'install cmd = ' + install_cmd
        # install Mocha AE in silent mode
        retVal = os.system(install_cmd)
        if (retVal != 0):
            raise Exception('Failed to run installer')
    print 'Mocha Install Done'
    return True


if __name__ == '__main__':
    install_MochaAE()
