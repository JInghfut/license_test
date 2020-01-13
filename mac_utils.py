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

#from Foundation import *
import applescript
import logging
import time

import subprocess


def run_ae_script(script_file, application):
    """
    call_applescript will call the passed in application
    passing it the passed in script.
    On mac this is how we ask AE to run a script file

    :param script_file:  path to a script file
    :param application:  the Application name(apple script name)
    :return:  True or False
    """
    print("SF and APP: " + script_file + " " + application)
    script_command = """
        set scriptfile to (POSIX file (\"%s\"))
        with timeout of 3000 seconds
            tell application \"%s\"
                DoScriptFile scriptfile
            end tell
        end timeout
        """ % (script_file, application)

    # The timeout is long because some test projects may have many comps to render out
    # We want to make sure not to abort the script before it is finished
    start_time = time.time()

    try:

        scpt = applescript.AppleScript(script_command)
        print("Applescript returned:{}".format(scpt.run()))
        return True

    except applescript.ScriptError:

        logging.error("call_applescript error thrown")
        logging.error("ScriptError: {}".format(applescript.ScriptError.message))
        print("ScriptError: {}".format(applescript.ScriptError.message))
        duration = time.time() - start_time
        logging.info("Seconds to run applescript: {0:.2f}".format(duration))
        logging.info(script_command)

        return False


def quit_ae(application):
    """
    quit_ae this function will use applescript to tell AE to quit
    the reason there is a parameter is because this can be used with
    different versions of AE(hence different applescript name)
    :param application:  the application to quit
    :return: True or False
    """

    script_command = """
 
        set appName to \"%s\"
        with timeout of 1000 seconds
            if application appName is running then
                tell application appName to quit
            end if
        end timeout

        with timeout of 1000 seconds
           if application "ExtendScript Toolkit" is running then
                tell application "ExtendScript Toolkit" to quit
            end if
        end timeout
       """ % application

    start_time = time.time()

    try:
        scpt = applescript.AppleScript(script_command)
        scpt.run()
        # the script returns right away so often the next script run will fail because
        # AE has not finished quitting, so we'll sleep for a bit
        time.sleep(5)
        return True

    except applescript.ScriptError:

        logging.error("quit_ae error thrown")
        logging.error("ScriptError: {}".format(applescript.ScriptError.message))
        print("ScriptError: {}".format(applescript.ScriptError.message))
        duration = time.time() - start_time
        logging.info("Seconds to run applescript: {0:.2f}".format(duration))
        logging.info(script_command)

        return False


def start_ae(application):
    """
    start_ae this function will use applescript to tell AE to startup
    the reason there is a parameter is because this can be used with
    different versions of AE(hence different applescript name)
    :param application:  the application to start
    :return: True or False
    """

    script_command = """

        set appName to \"%s\"
        if application appName is running then
            tell application appName to activate
        end if
        """ % application

    try:

        scpt = applescript.AppleScript(script_command)
        scpt.run()
        return True

    except applescript.ScriptError:
        logging.error("start_ae error thrown")
        logging.error("ScriptError: {}".format(applescript.ScriptError.message))
        print("ScriptError: {}".format(applescript.ScriptError.message))
        logging.info(script_command)

        return False

def quit_ppro(ppro, media_encoder):
    """
    quit_ae this function will use applescript to tell AE to quit
    the reason there is a parameter is because this can be used with
    different versions of AE(hence different applescript name)
    :param application:  the application to quit
    :return: True or False
    """

    script_command = """

        set appName to \"%s\"
        with timeout of 1000 seconds
            if application appName is running then
                tell application appName to quit
            end if
        end timeout

        with timeout of 1000 seconds
           if application "ExtendScript Toolkit" is running then
                tell application "ExtendScript Toolkit" to quit
            end if
        end timeout
       """ % ppro

    script_command2 = """

            set appName to \"%s\"
            with timeout of 1000 seconds
                if application appName is running then
                    tell application appName to quit
                end if
            end timeout

           """ % media_encoder

    start_time = time.time()

    try:
        print("script 1: " + str(script_command))
        scpt = applescript.AppleScript(script_command)
        scpt.run()
        # the script returns right away so often the next script run will fail because
        # AE has not finished quitting, so we'll sleep for a bit
        time.sleep(5)

        print("script 2: "+ str(script_command2))
        scpt = applescript.AppleScript(script_command2)
        scpt.run()
        # the script returns right away so often the next script run will fail because
        # AE has not finished quitting, so we'll sleep for a bit
        time.sleep(5)
        return True

    except applescript.ScriptError:

        logging.error("quit_ae error thrown")
        logging.error("ScriptError: {}".format(applescript.ScriptError.message))
        print("ScriptError: {}".format(applescript.ScriptError.message))
        duration = time.time() - start_time
        logging.info("Seconds to run applescript: {0:.2f}".format(duration))
        logging.info(script_command)

        return False


def start_ppro(application):
    """
    start_ae this function will use applescript to tell AE to startup
    the reason there is a parameter is because this can be used with
    different versions of AE(hence different applescript name)
    :param application:  the application to start
    :return: True or False
    """

    script_command = """

        set appName to \"%s\"
        if application appName is running then
            tell application appName to activate
        end if
        """ % application

    try:

        # scpt = applescript.AppleScript(script_command)
        # scpt.run()
        cmd = '/Applications/Adobe\ Premiere\ Pro\ CC\ 2019/Adobe\ Premiere\ Pro\ CC\ 2019.app/Contents/MacOS/Adobe\ Premiere\ Pro\ CC\ 2019'

        subprocess.Popen(cmd, shell=True)

        time.sleep(40)

        return True

    except applescript.ScriptError:
        logging.error("start_ae error thrown")
        logging.error("ScriptError: {}".format(applescript.ScriptError.message))
        print("ScriptError: {}".format(applescript.ScriptError.message))
        logging.info(script_command)

        return False


if __name__ == '__main__':
    if quit_ppro('Adobe Premiere Pro CC 2018', 'Adobe Media Encoder CC 2018'):
        print 'Success!'

