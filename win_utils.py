# ----------------------------------------------------------------------
# (c) Copyright 2017, BorisFX, Inc.  All rights reserved.
# This file may contain proprietary and confidential information.
# DO NOT COPY or distribute in any form without prior written consent.
# Initial implementation by Steve Davis  2-10-2017
# -----------------------------------------------------------------------
#
# mac_utils has all utilities related to the mac platform
# currently the only necessary code is related to calling
# AE via applescript which is how we need to call AE on
# mac in order to pass a script file
#

import logging
import time
import os
import subprocess


def run_ae_script(script_file, application):
    """
    run_ae_script will call the passed in application
    passing it the passed in script.
    On win we pass the script on the command line

    :param script_file:  path to a script file
    :param application:  the Application name(full path)
    :return:  True or False
    """
    start_time = time.time()

    try:
        cmd = application + " -r " +  script_file
        print("Command " + cmd)
        ret_val = subprocess.call(cmd)
        print("run_ae_script: {} returned:{}".format(application, ret_val))
        return True

    except OSError:
        logging.error("run_ae_script(OSError): {}".format(OSError.message))
        duration = time.time() - start_time
        logging.info("Seconds to run script: {0:.2f}".format(duration))
        return False

    except ValueError:
        logging.error("run_ae_script(ValueError): {}".format(ValueError.message))
        duration = time.time() - start_time
        logging.info("Seconds to run script: {0:.2f}".format(duration))
        return False


def quit_ae(application):
    """
    quit_ae this function will use taskkill to tell AE to quit
    the reason there is a parameter is because this can be used with
    different versions of AE(hence different application name)
    :param application:  the application to quit
    :return: True or False
    """
    try:
        # if sapphire, also make sure to quit the preset-browser.exe
        logging.info('---***Quitting preset-browser.exe!***---')
        os.system("TASKKILL /f /im preset-browser.exe")
        time.sleep(15)

        logging.info('---***Quitting After Effects!***---')
        os.system("TASKKILL /F /IM " + os.path.basename(application))
        time.sleep(15)
        return True

    except OSError:
        logging.error("quit_ae(OSError): {}".format(OSError.message))
        return False

    except ValueError:
        logging.error("quit_ae(ValueError): {}".format(ValueError.message))
        return False


def start_ae(application):
    """
    start_ae this function will use subprocess to tell AE to startup
    :param application:  the application to start (full path)
    :return: True or False
    """

    try:
        ret_val = subprocess.Popen(application)
        print("start_ae: {} returned:{}".format(application, ret_val))
        # Subprocess returns right away so sleep
        time.sleep(45)
        return True

    except OSError:
        logging.error("start_ae(OSError): {}".format(OSError.message))
        return False

    except ValueError:
        logging.error("run_ae_script(ValueError): {}".format(ValueError.message))
        return False


def quit_ppro(ppro, ame):
    """
    quit_ae this function will use taskkill to tell AE to quit
    the reason there is a parameter is because this can be used with
    different versions of AE(hence different application name)
    :param application:  the application to quit
    :return: True or False
    """
    try:
        ppro_exe = os.path.basename(ppro)
        ppro_exe = '"' + ppro_exe + '.exe"'
        ame_exe = os.path.basename(ame)
        ame_exe = '"' + ame_exe + '.exe"'

        # if sapphire, also make sure to quit the preset-browser.exe
        logging.info('---***Quitting preset-browser.exe!***---')
        os.system("TASKKILL /f /im preset-browser.exe")
        time.sleep(15)

        logging.info('---***Quitting Premiere Pro!***---')
        os.system("TASKKILL /F /IM " + ppro_exe)
        time.sleep(15)
        # return True

        logging.info('---***Quitting AME!***---')
        os.system("TASKKILL /F /IM " + ame_exe)
        time.sleep(15)
        return True

    except OSError:
        logging.error("quit_ae(OSError): {}".format(OSError.message))
        return False

    except ValueError:
        logging.error("quit_ae(ValueError): {}".format(ValueError.message))
        return False

