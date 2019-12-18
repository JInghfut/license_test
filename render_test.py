import json
import os
import subprocess
import time
import config
import image_comp
import write_license_results

import test_utils
if test_utils.is_mac():
    import mac_utils as plat_utils
elif test_utils.is_win():
    import win_utils as plat_utils

def _run_render_test():
    """
    _run_render_test calls to write the ae scriptr file and uns the render test for a single ae project file

    :param project_file: path to the ae project file
    :param base_directory: path to the ae project directory
    :param config_file_path: path to the config file
    :param is_creating_test_data: a bool stating whether to create test data (written to the expected results folder)
    :return: none
    """
    if config.ConfigParams.run_ppro_tests:
        test_file_ext = '.prproj'
    elif config.ConfigParams.run_nuke_tests:
        test_file_ext = '.nk'
    else:
        test_file_ext = '.aep'

    #project_file =  "\\\\horton\\DedupedData\\ae_test_projects\\license_test\\Sapphire_AE\\S_Aurora\\S_Aurora.aep"
    project_file = config.ConfigParams.render_test_directories[0]
    print ("project file: " + project_file)

    for subdir, dirs, files in os.walk(project_file):
        res_tmp = subdir.replace(os.path.abspath(config.ConfigParams.proj_directory), '')
        base_directory = config.ConfigParams.results_directory + res_tmp
        if not os.path.isdir(base_directory):
            os.mkdir(base_directory)
        if subdir.find("Auto-Save") < 0:
            for proj_file in files:
                if proj_file.endswith(test_file_ext):
                    proj_file = os.path.join(subdir, proj_file)
                    print("proj_file " + proj_file)
                    project_file = proj_file

    config_file_path = config.ConfigParams.render_config_path
    #if (bcc)

    _write_config_file(project_file, base_directory, config_file_path, False)

    # this is a precautionary step to make sure the results folders exist, probably not necessary though
    exp_dir = os.path.join(base_directory, "expected_results")
    test_dir = os.path.join(base_directory, "test_results")
    if not os.path.isdir(exp_dir):
        os.mkdir(exp_dir)
    if not os.path.isdir(test_dir):
        os.mkdir(test_dir)

    if not plat_utils.run_ae_script(config.ConfigParams.render_test_script, config.ConfigParams.target_app):
       print("ERROR RENDERING")

    print("BD " + base_directory)
    _compare_and_report_results(base_directory)

def _compare_render_results(test_results_directory, expected_results_directory):
    """
    _compare_render_results will iterate through the test_results_directory and compare the images with the known
    good results in the expected_results_directory. For each image it will add a result record
    :param test_results_directory: path to the test result images
    :param expected_results_directory: path to the directory of known good results
    :return: none, but this function will enter a result in the results module with the results for each images
    """
    err_desc = ""

    #to corroborate that the below code is correct and to make sure that the missing tests come from AE or those scripts:
    if os.listdir(test_results_directory) != os.listdir(expected_results_directory) and os.listdir(test_results_directory):
        print('Test Results do not Match Expected results!!')
        for test_res in os.listdir(test_results_directory):
            if not test_res in os.listdir(expected_results_directory):
                print('**No expected result for: ' + test_res)

    for test_result_name in os.listdir(test_results_directory):
        if test_result_name.endswith('.exr') or test_result_name.endswith('.tif'):
            # For each file in the test results directory we need to find the matching file in the expected results folder

            #logging.info("Comparing results: " + test_result_name)
            #print("Comparing results: " + test_result_name)
            test_file = os.path.join(test_results_directory, test_result_name)
            expected_file = os.path.join(expected_results_directory, test_result_name)

            # If the matching bit depth file doesn't exist, try the float version
            if not os.path.exists(expected_file):
                if "_8_" in test_file:
                    expected_file = expected_file.replace("_8_", "_32_")
                elif "_16_" in test_file:
                    expected_file = expected_file.replace("_16_", "_32_")

            if os.path.exists(expected_file):
                # results_dict = image_utils.compare_image_files(test_file, expected_file)
                results_dict = image_comp.compare_image_files(test_file, expected_file)

                if results_dict.get("success"):
                    os.remove(test_file)
                    print("Comparing succeeded: " + os.path.basename(test_file))
                    config.ConfigParams.license_success = True
                else:
                    error_status_dict = results_dict.get("error_status")
                    err_desc = error_status_dict.get("message")
                    print(err_desc)
                    print("Comparing Failed: " + os.path.basename(test_file))
            else:
                err_desc = "Expected Result missing: {} ".format(os.path.basename(expected_file))

            # make the path a bit shorter for display
            test_file_path = test_file.replace(config.ConfigParams.base_directory, '')
            test_file_path = test_file_path.replace('test_results', '')
            #results.TestResults.add_render_result("Verify Render:{}".format(test_file_path), success, err_desc)


    if config.ConfigParams.license_success:
        # write to text file that this serial did work for this product and host
        print("License activated successfully")
        write_license_results.write_license_results()
        cmd = config.ConfigParams.license_path + ' --deactivate '
        ret_val = subprocess.call(cmd)
        config.ConfigParams.license_success = False
    else:
        # write to text file that this serial didn't work for this product and host
        write_license_results.write_license_results()
        print("License activated unsuccessfully")


def _compare_and_report_results(base_directory):
    """
    _compare_and_report_results does the setup in order to call _compare_render_results
    it will build the paths for the test results and expected results
    :param base_directory: the project directory that should contain directories named
    test_results and expected_results
    :return: none
    """
    test_results_directory = os.path.join(base_directory, "test_results")
    expected_results_directory = os.path.join(base_directory, "expected_results")

    _compare_render_results(test_results_directory, expected_results_directory)


def _write_config_file(project_file, base_directory, config_file_path, create_test_data):
    """
    _write_config_file writes a config file that will be read by the AE script in order to
    know which project file to open and where to put the results

    :param project_file: the AE project file path
    :param base_directory: the directory of the AE project path
    :param config_file_path: the path where the config file will be written
    :param create_test_data: a bool stating whether to create test data (written to the expected results folder)
    :return: none
    """

    # if(create_test_data):
    #    bit_depths = [32]
    # else:
    #    bit_depths = [8, 16, 32]

    # config_data = {'base_directory': base_directory, 'project_file': project_file, 'create_test_data':create_test_data, 'bit_depths':bit_depths}
    config_data = {'base_directory': base_directory, 'project_file': project_file, 'create_test_data': create_test_data}

    if os.path.isfile(config_file_path):
        with open(config_file_path, 'w') as outfile:
            json.dump(config_data, outfile, indent=4, sort_keys=True, separators=(',', ':'))

    else:
        print('Config JSON currently not available... testing again in 5s')
        for i in range(3):
            time.sleep(5)
            if os.path.isfile(config_file_path):
                with open(config_file_path, 'w') as outfile:
                    json.dump(config_data, outfile, indent=4, sort_keys=True, separators=(',', ':'))
                    break
            else:
                print('Still not available, trying again...')

if __name__ == "__main__":
    config.ConfigParams.init_config()
    _run_render_test()
