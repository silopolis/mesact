import os, sys, subprocess
from PyQt5.QtWidgets import QInputDialog, QLineEdit

def check_ip(parent):
	if not parent.ipAddressCB.currentData():
		parent.errorMsgOk('An IP address must be selected', 'Error!')
		return False
	return True

def check_emc():
	if "0x48414c32" in subprocess.getoutput('ipcs'):
		return True
	else:
		return False

def readpd(parent):
	if check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to read the {parent.board}', 'Error')
		return
	if check_ip(parent):
		ipAddress = parent.ipAddressCB.currentText()
		arguments = ["--device", parent.device, "--addr", ipAddress, "--print-pd"]
		parent.extcmd.job(cmd="mesaflash", args=arguments, dest=parent.machinePTE)

def readhmid(parent):
	if check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to read the {parent.board}', 'Error')
		return
	if check_ip(parent):
		ipAddress = parent.ipAddressCB.currentText()
		arguments = ["--device", parent.device, "--addr", ipAddress, "--readhmid"]

		parent.extcmd.job(cmd="mesaflash", args=arguments, dest=parent.machinePTE)

def flashCard(parent):
	arguments = []
	if check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to flash the {parent.board}', 'Error')
		return
	if parent.firmwareCB.currentData():
		firmware = os.path.join(parent.lib_path, parent.firmwareCB.currentData())
		if parent.boardType == 'eth':
			if check_ip(parent):
				ipAddress = parent.ipAddressCB.currentText()
				arguments = ["--device", parent.device, "--addr", ipAddress, "--write", firmware]
			else:
				return
		elif parent.boardType == 'pci':
			arguments = ["--device", parent.device, "--write", firmware]
		parent.statusbar.showMessage(f'Flashing the {parent.device}...')
		if parent.boardType == 'pci':
			parent.extcmd.sudojob(cmd="mesaflash", args=arguments, dest=parent.machinePTE)
		if parent.boardType == 'eth':
			parent.extcmd.job(cmd="mesaflash", args=arguments, dest=parent.machinePTE)

	else:
		parent.errorMsgOk('A firmware must be selected', 'Error!')
		return


def reloadCard(parent):
	if check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to reload the {board}', 'Error')
		return
	if check_ip(parent):
		ipAddress = parent.ipAddressCB.currentText()
		arguments = ["--device", parent.device, "--addr", ipAddress, "--reload"]
		parent.extcmd.job(cmd="mesaflash", args=arguments, dest=parent.machinePTE)

def verifyCard(parent):
	if check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to verify the {board}', 'Error')
		return
	if check_ip(parent):
		ipAddress = parent.ipAddressCB.currentText()
		firmware = os.path.join(parent.lib_path, parent.firmwareCB.currentData())
		arguments = ["--device", parent.device, "--addr", ipAddress, "--verify", firmware]
		parent.extcmd.job(cmd="mesaflash", args=arguments, dest=parent.machinePTE)

def getCardPins(parent):
	if check_ip(parent):
		with open('temp.hal', 'w') as f:
			f.write('loadrt hostmot2\n')
			f.write(f'loadrt hm2_eth board_ip={parent.ipAddressCB.currentData()}\n')
			f.write('quit')
		arguments = ["-f", "temp.hal"]
		parent.extcmd.job(cmd="halrun", args=arguments, dest=parent.pinsPTE, clean='temp.hal')

def savePins(parent):
	if parent.configName.text() == '':
		parent.errorMsgOk('A Configuration\nmust be loaded', 'Error')
		return
	if not "0x48414c32" in subprocess.getoutput('ipcs'):
		parent.errorMsgOk(f'LinuxCNC must be running\nthe {parent.configName.text()} configuration', 'Error')
		return
	parent.results = subprocess.getoutput('halcmd show pin')
	fp = os.path.join(parent.configPath, parent.configNameUnderscored + '-pins.txt')
	with open(fp, 'w') as f:
		f.writelines(parent.results)
	parent.statusbar.showMessage(f'Pins saved to {fp}')

def saveSignals(parent):
	if parent.configName.text() == '':
		parent.errorMsgOk('A Configuration\nmust be loaded', 'Error')
		return
	if not "0x48414c32" in subprocess.getoutput('ipcs'):
		parent.errorMsgOk(f'LinuxCNC must be running\nthe {parent.configName.text()} configuration', 'Error')
		return
	parent.results = subprocess.getoutput('halcmd show sig')
	fp = os.path.join(parent.configPath, parent.configNameUnderscored + '-sigs.txt')
	with open(fp, 'w') as f:
		f.writelines(parent.results)
	parent.statusbar.showMessage(f'Signals saved to {fp}')

def saveParameters(parent):
	if parent.configName.text() == '':
		parent.errorMsgOk('A Configuration\nmust be loaded', 'Error')
		return
	if not "0x48414c32" in subprocess.getoutput('ipcs'):
		parent.errorMsgOk(f'LinuxCNC must be running\nthe {parent.configName.text()} configuration', 'Error')
		return
	parent.results = subprocess.getoutput('halcmd show parameter')
	fp = os.path.join(parent.configPath, parent.configNameUnderscored + '-parameters.txt')
	with open(fp, 'w') as f:
		f.writelines(parent.results)
	parent.statusbar.showMessage(f'Parameters saved to {fp}')

def firmwarePins(parent):
	if parent.firmwareCB.currentData():
		bitFile = os.path.join(parent.firmware_path, parent.firmwareCB.currentData())
		pinFile = os.path.splitext(bitFile)[0]+'.pin'
		if os.path.exists(pinFile):
			parent.machinePTE.clear()
			with open(pinFile, 'r') as file:
				data = file.read()
			parent.machinePTE.appendPlainText(data)
		else:
			parent.machinePTE.clear()
			parent.machinePTE.appendPlainText(f'No pin file found for {os.path.basename(bitFile)}')
	else:
		parent.machinePTE.clear()
		parent.machinePTE.appendPlainText('Select a Firmware to view pins')
