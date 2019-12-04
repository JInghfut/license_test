import json
import os
import time
import config

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
    project_file =  "\\\\horton\DedupedData\\ae_test_projects\\license_test\\BCC_AE\\BCC11_3D_Objects\\BCC_Extruded_Spline\\480x270_Sq\\480x270_Sq.aep"
    base_directory = 'C:\\Users\\Niall Buckley\\Documents\\ae_test_env\\ae_shared_proj_results\\license_test\\BCC_AE\\BCC11_3D_Objects\\BCC_Extruded_Spline\\480x270_Sq'
    config_file_path = "C:\\Users\\Niall Buckley\\Documents\\ae_test_env\\ae_scripts\\config.json"
    is_creating_test_data = False
    #if (bcc)

    _write_config_file(project_file, base_directory, config_file_path, is_creating_test_data)

    # this is a precautionary step to make sure the results folders exist, probably not necessary though
    exp_dir = os.path.join(base_directory, "expected_results")
    test_dir = os.path.join(base_directory, "test_results")
    if not os.path.isdir(exp_dir):
        os.mkdir(exp_dir)
    if not os.path.isdir(test_dir):
        os.mkdir(test_dir)
#C:\Users\Niall Buckley\Documents\ae_test_env\ae_shared_proj_results\license_test\BCC_AE\BCC11_3D_Objects\BCC_Extruded_Spline\480x270_sq
#C:\Users\Niall Buckley\Documents\ae_test_env\ae_shared_proj_results\license_test\BCC_AE\BCC11_3D_Objects\BCC_Extruded_Spline\480x270_sq\expected_results
    if not plat_utils.run_ae_script(config.ConfigParams.render_test_script, config.ConfigParams.target_app):
       print("ERROR RENDERING")

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
