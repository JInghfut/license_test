import config



def write_license_results():
    # current_serial = config.ConfigParams.file_line
    print("Important!! " + str(config.ConfigParams.file_line))
    # if serials:
    if config.ConfigParams.lic_test_type == 'server':
        file_path = "C:\\Users\\Niall Buckley\\Desktop\\HW.txt"
    elif  config.ConfigParams.lic_test_type == 'serial':
        file_path = "C:\\Users\\Niall Buckley\\Desktop\\multihost - Copy.txt"

    with open(file_path) as file:
        all_serials = file.readlines()
        # remove trailing new line (/n)
        for p in all_serials:
            print p
        current = all_serials[config.ConfigParams.file_line].rstrip()
        if config.ConfigParams.license_success:
            all_serials[config.ConfigParams.file_line] = str(
                current) + " " + config.ConfigParams.plugin_install + "---Success \n"
        else:
            all_serials[config.ConfigParams.file_line] = str(
                current) + " " + config.ConfigParams.plugin_install + "---Failure \n"
    with open(file_path, 'w') as k:
        k.writelines(all_serials)
        # k.close()
