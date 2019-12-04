import subprocess

def activate_license(serial_num):
    #if(sapphire):
        #path to sapphire license '"C:\\Program Files\\GenArts\\SapphireAE\\license-tool\\licence-tool"'
    #elif(bcc):
        #path to bcc license C:\Program Files\BorisFX\ContinuumAE\13\utilities\bfx-license-tool
    #elif(mocha):
        #path to bcc license
    cmd = '"C:\\Program Files\\BorisFX\ContinuumAE\\13\\utilities\\bfx-license-tool\\bfx-license-tool"' + ' --activate ' + serial_num
    #+ str(serial_num)
    ret_val = subprocess.call(cmd)

def find_license():
    #g = "C:\\Users\\Niall Buckley\\Desktop\\multihost.txt"
    with open( "C:\\Users\\Niall Buckley\\Desktop\\multihost.txt") as file:
        serial_num = file.readline()
    activate_license(serial_num)

if __name__ == "__main__":
    find_license()