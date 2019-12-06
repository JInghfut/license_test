import shlex, subprocess, shutil
import os
import re
import logging
# to tell if Mac/Win
import test_utils
import config
if test_utils.is_mac():
	import mac_utils as plat_utils
elif test_utils.is_win():
	import win_utils as plat_utils

def install_SapphireAE():
	split_list = []
	#list builds in store and filter by age to make naming consistent
	if test_utils.is_mac():
		install_path = '/Users/borisfx/Desktop/Engineering/tmp/buildbot-builds/master-sapphire-mac-ae'
	else:
		# should work for all Win test machines even if Engineering assigned as a different letter drive:
		# master-sapphire-win-ae
		install_path = '\\\\horton\\Engineering\\tmp\\buildbot-builds\\v20-maint-sapphire-win-ae'
	if config.ConfigParams.plugin_catagory == 'OFX':
		install_path = install_path.replace('-ae', '-ofx')
	split_list = os.listdir(install_path)
	# split_list = installer_list
	s_dates = [0, 0, 0, 0]
	i = 0
	current_dir = [0, 0, 0, 0]
	#try - and - except should be improved
	try:
		for dates in split_list:
			print("Dates = " + dates)
			print("Current Dir = " + str(current_dir))
			if dates == '.DS_Store':
				dates = '0'
			str_dates = (dates.split('-'))
			for num in str_dates:
				if num:
					s_dates[i] = int(num)
					i += 1
			if s_dates[0] > current_dir[0]:
				current_dir = s_dates
			elif s_dates[0] == current_dir[0]:
				if s_dates[1] > current_dir[1]:
					current_dir = s_dates
				elif s_dates[1] == current_dir[1]:
					if s_dates[2] > current_dir[2]:
						current_dir = s_dates
					elif s_dates[2] == current_dir[2]:
						if s_dates[3] > current_dir[3]:
							current_dir = s_dates
			s_dates = [0, 0, 0, 0]
			i = 0
	except ValueError:
		print("Current Dir2 = " + str(current_dir))
	#print 'current_dir:'
	print("Current Dir3 = " + str(current_dir))
	s_installer_name = ''
	i = 0
	for item in current_dir:
		if i < 3:
			if item < 10:
				s_installer_name += '0' + str(item) + '-'
			else:
				s_installer_name += str(item) + '-'
		else:
			if item < 100000:
				s_installer_name += '0' + str(item)
			else:
				s_installer_name += str(item)
		i+=1
	config.ConfigParams.build_num = s_installer_name
	print 'Installing file at: ' + os.path.join(install_path, s_installer_name)
	installer_source = os.path.join(install_path, s_installer_name)
	latest_installer = os.path.abspath(installer_source)
	print("Installing Sapphire Build from: {}".format(latest_installer))
	logging.info("Installing BCC Build from:{}".format(latest_installer))
	# results.TestResults.installed_build = latest_installer
	# find the name of the installer (either .exe or .dmg)
	pkg_name = ''
	if test_utils.is_win():
		inst_extension = '.exe'
	else:
		inst_extension = '.dmg'
	for item in os.listdir(latest_installer):
		if item.endswith(inst_extension):
			pkg_name = item
	##SHOULD HAVE THIS!##
	print("Quit AE if it is running")
	plat_utils.quit_ae(config.ConfigParams.target_app)
	#download and install newest 5.6.0 build
	if test_utils.is_mac():
		#Mac dest
		copy_dest = '/Users/borisfx/Documents/ae_test_env/'
		volume_name = ''
		sa_pkg_name = ''
		# good for all Mac test systems
		volumes_dir = '/Volumes'
		#copy over newest build to designated folder
		installer_source = os.path.join(latest_installer, pkg_name)
		print 'copying... ' + installer_source
		shutil.copy(installer_source, config.ConfigParams.base_directory)
		inst_dest = os.path.join(config.ConfigParams.base_directory, pkg_name)
		#mount disk image
		mount_cmd = 'hdiutil attach ' + inst_dest
		s_mount_cmd = shlex.split(mount_cmd)
		retVal = subprocess.call(s_mount_cmd)
		if (retVal != 0):
			raise Exception('Failed to mount pkg')
		for item in os.listdir(volumes_dir):
			if item.find('Sapphire') > -1:
				if item.find(config.ConfigParams.plugin_catagory) > -1:
					volume_name = item
		if volume_name:
			volume_name = os.path.join(volumes_dir, volume_name)
			for item in os.listdir(volume_name):
				if item.find('Sapphire') > -1:
					if item.find(config.ConfigParams.plugin_catagory) > -1:
						sa_pkg_name = item
		#os.path.splitext(config.ConfigParams.installer_name)[0]
		#run the installer
		if sa_pkg_name:
			sa_pkg_path = os.path.join(volume_name, sa_pkg_name)
			install_cmd = "installer -target / -package " + sa_pkg_path
			full_cmd = "echo " +  config.ConfigParams.mac_admin_password + " | sudo -S " + install_cmd
			retVal = os.system(full_cmd)
			if (retVal != 0):
				raise Exception('Failed to run installer')
			# unmount the installed volume
			unmount_cmd = shlex.split('hdiutil unmount ' + volume_name)
			subprocess.call(unmount_cmd)
		else:
			logging.error('No installer mounted!')
			return False
	elif test_utils.is_win():
		#Win dest
		copy_dest = 'C:\Users\\qa\\Documents\\ae_test_env\\installers'
		exe_name = pkg_name
		copy_path = os.path.join(latest_installer, exe_name)
		# print 'copying...'
		installer = os.path.abspath(copy_path)
		if exe_name in os.listdir(config.ConfigParams.base_directory):
			os.remove(os.path.join(config.ConfigParams.base_directory, exe_name))
		shutil.copy(installer, config.ConfigParams.base_directory)
		installer_path = os.path.join(config.ConfigParams.base_directory, exe_name)
		print installer_path
		cmd = '"C:\\Users\\Niall Buckley\\Documents\\ae_test_env\\sapphire-ae-install-2020.01.exe"' + ' /VERYSILENT /SP-'
		retVal = subprocess.call(cmd)
		if (retVal != 0):
			raise Exception('Failed to run installer')
		print("Finished running the silent install")
	print 'Sapphire Install Done'
	#delete old installer?
	return True

# FOR TESTING:
if __name__ == '__main__':
	config.ConfigParams.init_config()
	install_SapphireAE()