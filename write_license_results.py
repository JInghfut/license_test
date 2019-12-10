import config


def write_license_results():
    #current_serial = config.ConfigParams.file_line
    print("Important!! " + str(config.ConfigParams.file_line))
    with open("C:\\Users\\Niall Buckley\\Desktop\\multihost - Copy.txt") as file:
        all_serials = file.readlines()
        #remove trailing new line (/n)
        for p in all_serials:
            print p
        current = all_serials[config.ConfigParams.file_line].rstrip()
        if config.ConfigParams.license_success:
            all_serials[config.ConfigParams.file_line] = str(current) + " " + config.ConfigParams.plugin_install + "---Success \n"
        else:
            all_serials[config.ConfigParams.file_line] = str(current) + " " + config.ConfigParams.plugin_install + "---Failure \n"
    with open("C:\\Users\\Niall Buckley\\Desktop\\multihost - Copy.txt", 'w') as k:
        k.writelines(all_serials)
        #k.close()