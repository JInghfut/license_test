import subprocess
import config
import render_test


def activate_license(serial_num):
    #config.ConfigParams.license_path
    cmd = config.ConfigParams.license_path + ' --activate ' + serial_num
    print(cmd)
    ret_val = subprocess.call(cmd)
    render_test._run_render_test()


def find_license():
    # g = "C:\\Users\\Niall Buckley\\Desktop\\multihost.txt"
    with open("C:\\Users\\Niall Buckley\\Desktop\\multihost.txt") as file:
        serial_num = file.readline()
    activate_license(serial_num)


if __name__ == "__main__":
    find_license()
