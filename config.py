import os
import sys
import ConfigParser
import test_utils

class ConfigParams(object):
    """
    ConfigParams is a singleton class to load verify and store the config params

    """

    config_filename = ''

    # The Target Application, this name is the Applescript name
    # when in doubt you can open the mac applescript editor to get the app name
    # loaded
    target_app = ""
    base_directory = ""
    system_info = ""
    cpu_info = ""
    memory_info = ""
    gpu_info = ""
    installer_search_path = ""
    installer_name = ""
    mac_installer_package_name = ""
    mac_admin_password = ""

    #for accessing the projects shared on horton:
    proj_directory = ''
    results_directory = ''

    #For Horton saving results
    machine_name = ''
    copy_results = False
    horton_path = ''

    copy_mocha_results = False

    # results and logs
    html_results_subfolder = "html_results"  # path to put the html file
    html_results_filename = "BCC_test_results_"  # the date stamp will be appended
    log_file_subfolder = "python_logs"          # the path to the log file,
    log_file_name = "bcc_test_"          # the date stamp will be appended

    #ImageFormat
    use_tif_format = True
    use_exr_format = False
    # create_test_data Bool: true or false
    # if true the selected tests will be run and the expected data will be created, verification tests will be skipped
    # *****The results will need to be manually checked before the tests are run  *****
    create_test_data = False

    traverse_render_test_in_reverse = False
    if traverse_render_test_in_reverse:
        html_results_filename = 'BCC_test_results-rev'
    # AE seems to slow down after running a bunch of tests possibly related to AE caching frames, so we restart
    # AE every n renders. Set it to 1 if you'd like to have AE restart for each test, but it will slow down
    # the tests significantly on the order of 30sec per test(which typically takes about 4 seconds)-sd
    restart_ae_every_n_renders = 1

    # run_installed_plugin_test Bool: true or false
    # if true the tests to confirm that the proper number of effects are installed
    # also checks match name, display name and reports additional BCC Plugins found
    run_installed_plugins_test = True
    installed_plugin_script = ""
    installed_plugin_expected_results = ""

    installed_plugin_test_folder = ""
    installed_plugin_test_results = ""

    # run_render_test Bool: true or false
    # If true any AE Project file found in the render_test_directories array will be loaded, images rendered
    # and then compared with the expected results
    run_render_test = True

    # render_test_script is the python code calls to do the AE project renders
    render_test_script = ""

    # render_test_directories a list of paths for which the render tests will be run
    render_test_directories = []

    # render_config_path is the path to the config file(JSON format) to  be used by the AE script to do the render test
    render_config_path = ""

    # run_speed_test Bool: true or false
    # If true any AE Project file found in the speed_test_directories array will be loaded, comps rendered
    # and compared with known speed results
    run_speed_test = True

    # times_to_run_speed_test
    # the number of times to render, then average the render time
    times_to_run_speed_test = 5

    # render_test_script is the python code calls to do the AE project renders
    speed_test_script = ""

    # speed_test_directories a list of paths for which the render tests will be run
    speed_test_directories = []

    # speed_config_path is the path to the config file(JSON format) to  be used by the AE script to do the speed test
    speed_config_path = ""

    speed_test_tolerance_pct = 5.0

    #dirs for the mocha tests
    mocha_test_directories = []

    #setup mocha render test
    #mocha_render_test = False

    #Dirs for mochaAE performance test
    mocha_speed_directories = []

    #Dirs for the Sapphire tests
    sapphire_test_directories = []

    #Dirs for the Sapphire render test
    #sapphire_render_test = False

    #Dirs for the Sapphire performance test
    sapphire_speed_directories = []

    plugin_install = ''

    build_num = -1

    git_hash = ''
    xlsx_path = ''
    rclone_cmd = ''

    # defaults to 'AE'
    plugin_catagory = 'AE'

    # used to find the installer within the newest build folder
    sub_build_install_path = ''

    # ---- Premiere Pro Config Variables ---- #
    run_ppro_tests = False

    extendscript_cmd_mac = ''

    adobe_scripts_render = ''

    ppro_config_path = ''

    ppro_render_complete_path = ''

    # this var tracks if after the first run of a ppro test, that AME is already open and does not need to be loaded
    ppro_after_first_run = False

    media_encoder = ''
    ame_log_file = ''

    ppro_render_directories = []
    ppro_speed_directories = []

    # ---- Davinci Resolve Config Variables ---- #
    run_resolve_tests = False

    # ---- Nuke - OFX Config Variables ---- #
    run_nuke_tests = False
    nuke_bcc_render_directories = []
    nuke_bcc_speed_directories = []
    # sapphire in nuke:
    nuke_sapphire_render_directories = []
    nuke_sapphire_speed_directories = []

    installer_search_path_ofx = ''
    installer_name_ofx = ''

    nuke_app_path = ''
    nuke_py = ''

    license_success = False
    license_path = '"C:\\Program Files\\BorisFX\ContinuumAE\\13\\utilities\\bfx-license-tool\\bfx-license-tool"'

    #License paths
    sapphire_lic_test = []
    bcc_lic_test = []
    mocha_lic_test = []

    file_line = -1

    @staticmethod
    def init_config():
        """
        init will load the params from the config file and set the class variables
        it will also call the code to verify the config params(paths exist etc . . )
        """

        if len(ConfigParams.base_directory) != 0: #already inited, could happen if running from continuous integration
            return

        config = ConfigParser.ConfigParser()

        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(__file__)
        else:
            application_path = ""
            print("***Error: Can't find application path")

        # This section points to the local (not in the git repo) test.cfg file per machine (both machines of the same OS have the same paths)
        # This allows the Jenkins agent to run the scripts right from the git repo and the ae_test_env will not need any other changes (projects, logs, etc. can stay in the same place)
        # The only things that need to change are the shell scripts on Mac and powershell scripts on Win that need to point to the git repo install_and_run.py
        if test_utils.is_win():
            ConfigParams.config_filename = 'C:\\Users\\Niall Buckley\\Desktop\\license_test\\tests.cfg'
        elif test_utils.is_mac():
            ConfigParams.config_filename = '/Users/borisfx/Documents/ae_test_env/python_scripts/tests.cfg'

        print("config_path1: " + ConfigParams.config_filename)
        config_path = os.path.join(application_path, ConfigParams.config_filename)
        print("config_path2: " + config_path)
        config_path = os.path.abspath(config_path)
        print("config_path3: " + config_path)

        ConfigParams.plugin_install = 'BCC'

        with open(config_path, 'r') as configfile:
            config.readfp(configfile)

            #Get the hardware system info
            ConfigParams.system_info = config.get('Hardware', "system_info")
            ConfigParams.cpu_info = config.get('Hardware', "cpu_info")
            ConfigParams.gpu_info = config.get('Hardware', "gpu_info")
            ConfigParams.memory_info = config.get('Hardware', "memory_info")

            #Horton
            ConfigParams.machine_name = config.get('General', 'machine_name')
            ConfigParams.copy_results = config.get('General', 'copy_results')
            ConfigParams.horton_path = config.get('General', 'horton_path')

            #copy mocha to gdrive
            ConfigParams.copy_mocha_results = config.get('General', 'copy_mocha_results')

            # Load the General section
            if test_utils.is_mac():
                ConfigParams.target_app = config.get('General', "target_app_mac")
                ConfigParams.installer_search_path = config.get('General', "installer_search_path_mac")
                ConfigParams.installer_name = config.get('General', "installer_name_mac")
                ConfigParams.mac_installer_package_name = config.get('General', "installer_package_name")
                ConfigParams.mac_admin_password = config.get('General', "mac_admin_password")

            elif test_utils.is_win():
                ConfigParams.target_app = config.get('General', "target_app_win")
                ConfigParams.installer_search_path = config.get('General', "installer_search_path_win")
                ConfigParams.installer_name = config.get('General', "installer_name_win")

            ConfigParams.base_directory = config.get('General', "base_directory")
            # expand the path or some calls will fail
            ConfigParams.base_directory = os.path.expanduser(ConfigParams.base_directory)
            ConfigParams.base_directory = os.path.abspath(ConfigParams.base_directory)

            # Now that we've loaded the data from the config, fill in the paths that we create from the base_directory
            if not os.path.exists(ConfigParams.base_directory):
                print("***ConfigParams::init_config base_directory doesn't exist: " + ConfigParams.base_directory)

            # horton projects:
            ConfigParams.proj_directory = config.get('General', 'proj_directory')
            res_tmp = config.get('General', 'results_directory')
            ConfigParams.results_directory = os.path.join(ConfigParams.base_directory, res_tmp)

            ConfigParams.restart_ae_every_n_renders = config.getint('General', "restart_ae_every_n_renders")
            ConfigParams.create_test_data = config.getboolean('General', "create_test_data")

            # Load the TestToRun section
            ConfigParams.run_installed_plugins_test = config.getboolean('TestsToRun', "run_installed_plugins_test")
            ConfigParams.run_render_test = config.getboolean('TestsToRun', "run_render_test")
            ConfigParams.run_speed_test = config.getboolean('TestsToRun', "run_speed_test")
            ConfigParams.times_to_run_speed_test = config.getint('TestsToRun', "times_to_run_speed_test")
            ConfigParams.run_mocha_render_test = config.getboolean('TestsToRun', 'mocha_render_test')

            # Load the RenderTestDirectories section
            #render_directories = config.items('RenderTestDirectories')

            #temp
            render_directories = config.items('RenderTestDirectories')

            for item in render_directories:
                if item[0].find('render_dir') > -1:
                    the_path = os.path.join(ConfigParams.proj_directory, item[1])
                    the_path = os.path.abspath(the_path)
                    ConfigParams.render_test_directories.append(the_path)

            speed_directories = config.items('SpeedTestDirectories')

            for item in speed_directories:
                if item[0].find('speed_dir') > -1:
                    the_path = os.path.join(ConfigParams.proj_directory, item[1])
                    the_path = os.path.abspath(the_path)
                    ConfigParams.speed_test_directories.append(the_path)

            bcc_lic_test = config.items('BCCAELicTest')

            #create mocha file path?
            mocha_directories = config.items('MochaAERenderTestDirectories')

            for item in mocha_directories:
                if item[0].find('mocha_dir') > -1:
                    the_path = os.path.join(ConfigParams.proj_directory, item[1])
                    the_path = os.path.abspath(the_path)
                    ConfigParams.mocha_test_directories.append(the_path)

            mocha_speed_directories = config.items('MochaAEPerformanceTestDirectories')

            for item in mocha_speed_directories:
                if item[0].find('m_speed_dir') > -1:
                    the_path = os.path.join(ConfigParams.proj_directory, item[1])
                    the_path = os.path.abspath(the_path)
                    ConfigParams.mocha_speed_directories.append(the_path)

            mocha_lic_test = config.items('MochaAELicTest')

            #Sapphire file path iterators
            sapphire_directories = config.items('SapphireAERenderTestDirectories')

            for item in sapphire_directories:
                if item[0].find('sapphire_dir') > -1:
                    the_path = os.path.join(ConfigParams.proj_directory, item[1])
                    the_path = os.path.abspath(the_path)
                    ConfigParams.sapphire_test_directories.append(the_path)

            sapphire_speed_directories = config.items('SapphireAEPerformanceTestDirectories')

            for item in sapphire_speed_directories:
                if item[0].find('s_speed_dir') > -1:
                    the_path = os.path.join(ConfigParams.proj_directory, item[1])
                    the_path = os.path.abspath(the_path)
                    ConfigParams.sapphire_speed_directories.append(the_path)

            #Sapphire license test
            sapphire_lic_dirs = config.items('SapphireAELicTest')

            for item in sapphire_lic_dirs:
                if item[0].find('s_lic_test') > -1:
                    the_path = os.path.join(ConfigParams.proj_directory, item[1])
                    the_path = os.path.abspath(the_path)
                    ConfigParams.sapphire_lic_test.append(the_path)

            #Mocha license test
            mocha_lic_dirs = config.items('MochaAELicTest')

            for item in mocha_lic_dirs:
                if item[0].find('m_lic_test') > -1:
                    the_path = os.path.join(ConfigParams.proj_directory, item[1])
                    the_path = os.path.abspath(the_path)
                    ConfigParams.mocha_lic_test.append(the_path)

            #BCC license test
            bcc_lic_dirs = config.items('BCCAELicTest')

            for item in bcc_lic_dirs:
                if item[0].find('bcc_lic_test') > -1:
                    the_path = os.path.join(ConfigParams.proj_directory, item[1])
                    the_path = os.path.abspath(the_path)
                    ConfigParams.bcc_lic_test.append(the_path)

            # Premiere Pro Test Directories:
            # Doesn't exist in the tests.cfg file??
            '''ppro_directories = config.items('PProRenderTestDirectories')

            for item in ppro_directories:
                if item[0].find('ppro_render_dir') > -1:
                    the_path = os.path.join(ConfigParams.proj_directory, item[1])
                    the_path = os.path.abspath(the_path)
                    ConfigParams.ppro_render_directories.append(the_path)

            ppro_speed_directories = config.items('PProSpeedTestDirectories')

            for item in ppro_speed_directories:
                if item[0].find('ppro_speed_dir') > -1:
                    the_path = os.path.join(ConfigParams.proj_directory, item[1])
                    the_path = os.path.abspath(the_path)
                    ConfigParams.ppro_speed_directories.append(the_path)

            # Nuke Test Directories:
            nuke_directories = config.items('NukeRenderTestDirectories')

            for item in nuke_directories:
                if item[0].find('nuke_render_dir') > -1:
                    the_path = os.path.join(ConfigParams.proj_directory, item[1])
                    the_path = os.path.abspath(the_path)
                    ConfigParams.nuke_bcc_render_directories.append(the_path)

            nuke_directories = config.items('NukeSpeedTestDirectories')

            for item in nuke_directories:
                if item[0].find('nuke_speed_dir') > -1:
                    the_path = os.path.join(ConfigParams.proj_directory, item[1])
                    the_path = os.path.abspath(the_path)
                    ConfigParams.nuke_bcc_speed_directories.append(the_path)

            nuke_directories = config.items('NukeSapphireRenderTestDirectories')

            for item in nuke_directories:
                if item[0].find('nuke_sa_render_dir') > -1:
                    the_path = os.path.join(ConfigParams.proj_directory, item[1])
                    the_path = os.path.abspath(the_path)
                    ConfigParams.nuke_sapphire_render_directories.append(the_path)

            nuke_directories = config.items('NukeSapphireSpeedTestDirectories')

            for item in nuke_directories:
                if item[0].find('nuke_sa_speed_dir') > -1:
                    the_path = os.path.join(ConfigParams.proj_directory, item[1])
                    the_path = os.path.abspath(the_path)
                    ConfigParams.nuke_sapphire_speed_directories.append(the_path)'''


            ConfigParams.installed_plugin_script = os.path.join(ConfigParams.base_directory, "ae_scripts/verify_installed_plugins.jsx")
            ConfigParams.installed_plugin_script = os.path.abspath(ConfigParams.installed_plugin_script)

            if not os.path.exists(ConfigParams.installed_plugin_script):
                print("***ConfigParams::init_config installed_plugin_script doesn't exist: " + ConfigParams.installed_plugin_script)

            if ConfigParams.use_tif_format:
                ConfigParams.render_test_script = os.path.join(ConfigParams.base_directory, "ae_scripts/render_license_test.jsx")
            else:
                ConfigParams.render_test_script = os.path.join(ConfigParams.base_directory, "ae_scripts/render_test_openexr.jsx")
            ConfigParams.render_test_script = os.path.abspath(ConfigParams.render_test_script)

            ConfigParams.speed_test_script = os.path.join(ConfigParams.base_directory, "ae_scripts/render_speed_test.jsx")
            ConfigParams.speed_test_script = os.path.abspath(ConfigParams.speed_test_script)

            if not os.path.exists(ConfigParams.render_test_script):
                print("***ConfigParams::init_config render_test_script doesn't exist: " + ConfigParams.render_test_script)

            index = 0
            for path in ConfigParams.render_test_directories:
                ConfigParams.render_test_directories[index] = os.path.abspath(os.path.expanduser(path))

                if not os.path.exists(ConfigParams.render_test_directories[index]):
                    print("***ConfigParams::init_config render_test_directories[] doesn't exist: " + ConfigParams.render_test_directories[index])
                index += 1

            # Don't bother to verify since they might not exist yet
            ConfigParams.installed_plugin_expected_results = os.path.join(ConfigParams.base_directory, "installed_plugin_test/installed_plugins_expected.json")
            ConfigParams.installed_plugin_expected_results = os.path.abspath(ConfigParams.installed_plugin_expected_results)


            ConfigParams.installed_plugin_test_folder = os.path.join(ConfigParams.base_directory, "installed_plugin_test")
            ConfigParams.installed_plugin_test_folder = os.path.abspath(ConfigParams.installed_plugin_test_folder)

            ConfigParams.installed_plugin_test_results = os.path.join(ConfigParams.base_directory, "installed_plugin_test/installed_plugins_test_results.json")
            ConfigParams.installed_plugin_test_results = os.path.abspath(ConfigParams.installed_plugin_test_results)

            ConfigParams.render_config_path = os.path.join(ConfigParams.base_directory, "ae_scripts/config.json")
            ConfigParams.render_config_path = os.path.abspath(ConfigParams.render_config_path)

            ConfigParams.speed_config_path = os.path.join(ConfigParams.base_directory, "ae_scripts/speed_config.json")
            ConfigParams.speed_config_path = os.path.abspath(ConfigParams.speed_config_path)

            ConfigParams.xlsx_path = os.path.join(ConfigParams.base_directory, 'ARCHIVED_RESULTS')
            ConfigParams.xlsx_path = os.path.abspath(ConfigParams.xlsx_path)


            ConfigParams.sapphire_lic_path = os.path.join(ConfigParams.base_directory, "ae_shared_proj_results/license_test/Sapphire_AE/S_Render/S_Aurora")
            ConfigParams.sapphire_lic_path = os.path.abspath(ConfigParams.render_config_path)

            ConfigParams.mocha_lic_path = os.path.join(ConfigParams.base_directory, "ae_shared_proj_results/license_test/Mocha_AE/M_Insert")
            ConfigParams.sapphire_lic_path = os.path.abspath(ConfigParams.render_config_path)

            ConfigParams.mocha_lic_path = os.path.join(ConfigParams.base_directory, "ae_shared_proj_results/license_test/Mocha_AE/M_Insert")
            ConfigParams.sapphire_lic_path = os.path.abspath(ConfigParams.render_config_path)

            '''ConfigParams.rclone_cmd = config.get('General', 'rclone_cmd')'''

            # if running BCC-OFX test, change to the ofx paths:
            if test_utils.is_mac():
                ConfigParams.sub_build_install_path = "archive/SharedCode/artifacts/"
            else:
                ConfigParams.sub_build_install_path = "archive\SharedCode\Installers\win\Output"

            # Premiere Pro #
            ppro_config_folder = os.path.join(ConfigParams.base_directory, "ppro_scripts/")
            if not os.path.isdir(ppro_config_folder):
                os.mkdir(ppro_config_folder)

            ConfigParams.ppro_config_path = os.path.join(ConfigParams.base_directory, "ppro_scripts/config.json")
            ConfigParams.ppro_config_path = os.path.abspath(ConfigParams.ppro_config_path)

            ConfigParams.ppro_render_complete_path = os.path.join(ConfigParams.base_directory, "ppro_scripts/render_complete.txt")
            ConfigParams.ppro_render_complete_path = os.path.abspath(ConfigParams.ppro_render_complete_path)

            '''ConfigParams.extendscript_cmd_mac = config.get('General', 'extendscript_cmd_mac')'''

            # named adobe_script because the script only runs automatically when put in the 'Adobe Scripts' folder made by ExtendScript
            '''ConfigParams.adobe_scripts_render = config.get('General', 'adobe_scripts_render')'''

            '''ConfigParams.media_encoder = config.get('General', 'media_encoder')'''

            if test_utils.is_win():
                ConfigParams.ame_log_file = "C:\\Users\\Niall Buckley\\Documents\\Adobe\\Adobe Media Encoder\\13.0\\AMEEncodingLog.txt"
            else:
                ConfigParams.ame_log_file = '/Users/borisfx/Documents/Adobe/Adobe Media Encoder/12.0/AMEEncodingLog.txt'


            # --- Nuke - OFX --- #
            '''ConfigParams.installer_search_path_ofx = config.get('General', 'installer_search_path_ofx')
            ConfigParams.installer_name_ofx = config.get('General', 'installer_name_ofx')

            ConfigParams.nuke_app_path = config.get('General', 'nuke_app_path')
            ConfigParams.nuke_py = config.get('General', 'nuke_script_file')'''
