# ----------------------------------------------------------------------
# (c) Copyright 2017, BorisFX, Inc.  All rights reserved.
# This file may contain proprietary and confidential information.
# DO NOT COPY or distribute in any form without prior written consent.
# Initial implementation by Steve Davis  2-10-2017
# ----------------------------------------------------------------------
#
# test_utils is the place for general functions that don't belong anywhere else
#

import platform
import time
import config
#import results
import os
import logging
import datetime

def get_date_string():
    """
    get_date_string
    :return:  a formatted date string
    """
    return time.strftime("%d/%m/%Y")


def get_current_time_string():
    """
    get_current_time_string
    :return: a formatted time string
    """
    return time.strftime("%H:%M:%S")


def get_platforrm_string():
    """
    get_platforrm_string
    :return: string name of the platform
    """
    if is_mac():
        return "Macintosh"
    elif is_win():
        return "Windows"


def get_platforrm_version_string():
    """
    get_platforrm_version_string
    :return:  string of the platform version
    """
    '''Returns the OS version of the current OS'''
    if is_mac():
        return platform.mac_ver()[0]
    return "??"


def is_mac():
    """
    is_mac
    :return: Bool, true if on mac platform
    """
    if platform.system() == "Darwin":
        return True
    else:
        return False


def is_win():
    """
    is_win
    :return: Bool, true if on windows platform
    """
    if platform.system() == "Windows":
        return True
    else:
        return False

def get_node():
    return platform.node()

def setup_logfile():
    if len(results.TestResults.log_file_name) == 0:
        # Setup the Log File
        log_path = os.path.join(config.ConfigParams.base_directory, config.ConfigParams.log_file_subfolder)
        # Create the log folder if it doesn't exist
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        start_time = time.time()
        results.TestResults.result_time_stamp = datetime.datetime.fromtimestamp(start_time).strftime(
            '%Y-%m-%d_%H-%M-%S')
        results.TestResults.log_file_name = config.ConfigParams.log_file_name + results.TestResults.result_time_stamp + ".log"
        log_path = os.path.join(log_path, results.TestResults.log_file_name)
        logging.basicConfig(filename=log_path, format='%(levelname)s:%(message)s', level=logging.INFO)
        print("Log File:{}".format(log_path))
        logging.info("Log File:{}".format(log_path))
