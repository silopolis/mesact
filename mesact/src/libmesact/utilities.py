import os, subprocess, requests
from packaging import version
from functools import partial
from datetime import datetime

from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtGui import QPixmap

from libmesact import firmware

MAIN_BOARDS = ['5i25', '7i80db_16', '7i80db_25', '7i80hd_16', '7i80hd_25',
	'7i92', '7i93', '7i98']

def isNumber(s):
	try:
		s[-1].isdigit()
		float(s)
		return True
	except ValueError:
		return False

def checks(parent):
	try:
		subprocess.check_output('mesaflash', encoding='UTF-8')
		try:
			version = subprocess.check_output(['mesaflash', '--version'], encoding='UTF-8')[-6:]
			if int(version.replace('.', '')) >= 342:
				parent.machinePTE.appendPlainText(f'Mesaflash Version: {version}')
		except:
			t = ('Mesaflash version is less than 3.4.2\n'
				'The Mesa Configuration Tool requires 3.4.2 or later.\n'
				'Go to https://github.com/LinuxCNC/mesaflash\n'
				'for installation/update instructions.')
			parent.machinePTE.appendPlainText(t)
	except FileNotFoundError:
		#parent.errorMsgOk(('Mesaflash not found go to\n'
		#	'https://github.com/LinuxCNC/mesaflash\n'
		#	'for installation instructions.'), 'Notice! Can Not Flash Firmware')
		t = ('Mesaflash not found go to\n'
			'https://github.com/LinuxCNC/mesaflash\n'
			'for installation instructions.')
		parent.machinePTE.appendPlainText(t)
		parent.firmwareCB.setEnabled(False)
		parent.firmwarePinsPB.setEnabled(False)
		parent.readPB.setEnabled(False)
		parent.flashPB.setEnabled(False)
		parent.reloadPB.setEnabled(False)
		parent.statusbar.showMessage('Mesaflash not found!')

def configNameChanged(parent, text):
	if text:
		parent.configNameUnderscored = text.replace(' ','_').lower()
		parent.configPath = os.path.expanduser('~/linuxcnc/configs') + '/' + parent.configNameUnderscored
		parent.pathLabel.setText(parent.configPath)
	else:
		parent.pathLabel.setText('')

def boardChanged(parent):
	if parent.boardCB.currentData():
		parent.machinePTE.clear()
		parent.daughterCB_0.clear()
		parent.daughterCB_1.clear()
		parent.board = parent.boardCB.currentData()
		if parent.boardCB.currentData() == '7i76e':
			parent.device = '7i76e-16'
		else:
			parent.device = parent.boardCB.currentData()

		# firmware combobox
		parent.firmwareCB.clear()
		path = os.path.join(parent.firmware_path, parent.boardCB.currentData())
		files = sorted([entry.path for entry in os.scandir(path) if entry.is_file()])
		bitFiles = False

		for file in files:
			if os.path.splitext(file)[1] == '.bit':
				# might want to do ('Default', False) for 7i76e, 7i95, 7i96, 7i97
				parent.firmwareCB.addItem('Select', False)
				bitFiles = True
				break

		for file in files:
			if os.path.splitext(file)[1] == '.bit':
				parent.firmwareCB.addItem(os.path.basename(file), file)

		if bitFiles:
			parent.machinePTE.appendPlainText(f'Firmware for {parent.boardCB.currentText()} Loaded')
			parent.machinePTE.appendPlainText('Select Firmware for Daughter Cards')
			parent.machinePTE.appendPlainText('Not all Firmware has a dictionary entry for Daughter Cards')
		else:
			parent.machinePTE.appendPlainText(f'No Firmware found {parent.boardCB.currentText()}!')
			parent.machinePTE.appendPlainText(f'No Daughter Cards are available for {parent.boardCB.currentText()}')

		if parent.boardCB.currentData() == '5i25':
			parent.boardType = 'pci'
			parent.cardType_0 = ''
			parent.mainTabs.setTabEnabled(3, False)
			parent.mainTabs.setTabEnabled(4, False)
			for i in range(32):
				getattr(parent, f'inputDebounceCB_{i}').setEnabled(False)
			parent.boardTW.setTabText(0, '5i25')
			parent.ipAddressCB.setEnabled(False)
			parent.daughterCB_0.setEnabled(True)
			parent.daughterCB_1.setEnabled(True)
			parent.ipAddressCB.setCurrentIndex(0)
			pixmap = QPixmap(os.path.join(parent.image_path, '5i25-card.png'))
			parent.boardLB.setPixmap(pixmap)
			info = ('')
			parent.boardInfoLB.setText(info)
			parent.daughterLB_0.setText('P2')
			parent.daughterLB_1.setText('P3')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('N/A', False)
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)

		# 5 axes of step & dir 32 sinking inputs and 16 sourcing outputs
		elif parent.boardCB.currentData() == '7i76e':
			parent.machinePTE.appendPlainText('Field Power is required for the I/O')
			parent.machinePTE.appendPlainText('Default Firmware is 7i76e_7i76x1D.bit')
			parent.boardType = 'eth'
			parent.cardType_0 = 'step'
			parent.mainTabs.setTabEnabled(3, True)
			parent.mainTabs.setTabEnabled(4, True)
			for i in range(32):
				getattr(parent, f'inputPB_{i}').setEnabled(True)
				getattr(parent, f'inputInvertCB_{i}').setEnabled(True)
				getattr(parent, f'inputDebounceCB_{i}').setEnabled(False)
			for i in range(16):
				getattr(parent, f'outputPB_{i}').setEnabled(True)
			parent.cardTabs.setTabText(0, '7i76e')
			parent.jointTabs_0.setTabEnabled(5, False)
			parent.boardTW.setTabText(0, '7i76e')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i76e-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('5', False)
			for i in range(4, -1, -1):
				parent.stepgensCB.addItem(f'{i}', f'{i}')
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)
			for i in range(5):
				getattr(parent, f'c0_stepgenGB_{i}').setVisible(True)
				getattr(parent, f'c0_analogGB_{i}').setVisible(False)
				getattr(parent, f'c0_encoderGB_{i}').setVisible(False)

		elif parent.boardCB.currentData() == '7i80db_16':
			parent.boardType = 'eth'
			parent.cardType_0 = ''
			parent.mainTabs.setTabEnabled(3, False)
			parent.mainTabs.setTabEnabled(4, False)
			parent.boardTW.setTabText(0, '7i80DB')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i80db-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.daughterLB_0.setText('J2')
			parent.daughterLB_1.setText('J3')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('N/A', False)
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)

		elif parent.boardCB.currentData() == '7i80db_25':
			parent.boardType = 'eth'
			parent.cardType_0 = ''
			parent.mainTabs.setTabEnabled(3, False)
			parent.mainTabs.setTabEnabled(4, False)
			parent.boardTW.setTabText(0, '7i80DB')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i80db-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.daughterLB_0.setText('J2')
			parent.daughterLB_1.setText('J3')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('N/A', False)
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)

		elif parent.boardCB.currentData() == '7i80hd_16':
			parent.boardType = 'eth'
			parent.cardType_0 = ''
			parent.mainTabs.setTabEnabled(3, False)
			parent.mainTabs.setTabEnabled(4, False)
			parent.boardTW.setTabText(0, '7i80HD')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i80hd-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			instructions = (
			'Firmware Notes\n'
			'SV = Servo\n'
			'ST = Step\n'
			'SS = SmartSerial\n'
			'RM = Resolver\n'
			'FA = Fanuc Absolute\n'
			'BI = BISS\n'
			'UA = UART\n')
			parent.machinePTE.appendPlainText(instructions)
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('N/A', False)
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)

		elif parent.boardCB.currentData() == '7i80hd_25':
			parent.boardType = 'eth'
			parent.cardType_0 = ''
			parent.mainTabs.setTabEnabled(3, False)
			parent.mainTabs.setTabEnabled(4, False)
			parent.boardTW.setTabText(0, '7i80HD')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i80hd-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			instructions = (
			'Firmware Notes\n'
			'SV = Servo\n'
			'ST = Step\n'
			'SS = SmartSerial\n'
			'RM = Resolver\n'
			'FA = Fanuc Absolute\n'
			'BI = BISS\n'
			'UA = UART\n')
			parent.machinePTE.appendPlainText(instructions)
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('N/A', False)
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)

		elif parent.boardCB.currentData() == '7i92':
			parent.boardType = 'eth'
			parent.cardType_0 = ''
			parent.mainTabs.setTabEnabled(3, False)
			parent.mainTabs.setTabEnabled(4, False)
			parent.boardTW.setTabText(0, '7i92')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i92-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('N/A', False)
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)

		elif parent.boardCB.currentData() == '7i93':
			parent.boardType = 'eth'
			parent.cardType_0 = ''
			parent.mainTabs.setTabEnabled(3, False)
			parent.mainTabs.setTabEnabled(4, False)
			parent.boardTW.setTabText(0, '7i93')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i93-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('N/A', False)
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)

		# 6 axes of step & dir 24 isolated inputs 6 isolated outputs
		elif parent.boardCB.currentData() == '7i95':
			parent.boardType = 'eth'
			parent.cardType_0 = 'step'
			parent.mainTabs.setTabEnabled(3, True)
			parent.mainTabs.setTabEnabled(4, True)
			for i in range(24):
				getattr(parent, f'inputPB_{i}').setEnabled(True)
				getattr(parent, f'inputInvertCB_{i}').setEnabled(True)
			for i in range(6):
				getattr(parent, f'outputPB_{i}').setEnabled(True)
			for i in range(24,32):
				getattr(parent, f'inputPB_{i}').setEnabled(False)
				getattr(parent, f'inputInvertCB_{i}').setEnabled(False)
			for i in range(32):
				getattr(parent, f'inputDebounceCB_{i}').setEnabled(False)
			for i in range(6,16):
				getattr(parent, f'outputPB_{i}').setEnabled(False)
			parent.cardTabs.setTabText(0, '7i95')
			parent.jointTabs_0.setTabEnabled(5, True)
			parent.mainTabs.setTabEnabled(4, True)
			parent.boardTW.setTabText(0, '7i95')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i95-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('N/A')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('6', False)
			for i in range(5, -1, -1):
				parent.stepgensCB.addItem(f'{i}', f'{i}')
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)
			for i in range(5):
				getattr(parent, f'c0_stepgenGB_{i}').setVisible(True)
				getattr(parent, f'c0_analogGB_{i}').setVisible(False)
				getattr(parent, f'c0_encoderGB_{i}').setVisible(False)

		# 5 axes of step & dir 11 isolated inputs 6 isolated outputs
		elif parent.boardCB.currentData() == '7i96':
			parent.boardType = 'eth'
			parent.cardType_0 = 'step'
			parent.mainTabs.setTabEnabled(3, True)
			parent.mainTabs.setTabEnabled(4, True)
			for i in range(11):
				getattr(parent, f'inputPB_{i}').setEnabled(True)
				getattr(parent, f'inputInvertCB_{i}').setEnabled(True)
			for i in range(6):
				getattr(parent, f'outputPB_{i}').setEnabled(True)
			for i in range(32):
				getattr(parent, f'inputDebounceCB_{i}').setEnabled(False)
			for i in range(11,32):
				getattr(parent, f'inputPB_{i}').setEnabled(False)
				getattr(parent, f'inputInvertCB_{i}').setEnabled(False)
			for i in range(6,16):
				getattr(parent, f'outputPB_{i}').setEnabled(False)
			parent.cardTabs.setTabText(0, '7i96')
			parent.jointTabs_0.setTabEnabled(5, False)
			parent.boardTW.setTabText(0, '7i96')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i96-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('N/A')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('5', False)
			for i in range(4, -1, -1):
				parent.stepgensCB.addItem(f'{i}', f'{i}')
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)
			for i in range(5):
				getattr(parent, f'c0_stepgenGB_{i}').setVisible(True)
				getattr(parent, f'c0_analogGB_{i}').setVisible(False)
				getattr(parent, f'c0_encoderGB_{i}').setVisible(False)

		# 5 axes of step & dir 11 isolated inputs 6 isolated outputs
		elif parent.boardCB.currentData() == '7i96s':
			parent.boardType = 'eth'
			parent.cardType_0 = 'step'
			parent.mainTabs.setTabEnabled(3, True)
			parent.mainTabs.setTabEnabled(4, True)
			for i in range(11):
				getattr(parent, f'inputPB_{i}').setEnabled(True)
				getattr(parent, f'inputInvertCB_{i}').setEnabled(True)
				getattr(parent, f'inputDebounceCB_{i}').setEnabled(True)
			for i in range(6):
				getattr(parent, f'outputPB_{i}').setEnabled(True)
			for i in range(11,32):
				getattr(parent, f'inputPB_{i}').setEnabled(False)
				getattr(parent, f'inputInvertCB_{i}').setEnabled(False)
				getattr(parent, f'inputDebounceCB_{i}').setEnabled(False)
			for i in range(6,16):
				getattr(parent, f'outputPB_{i}').setEnabled(False)
			parent.cardTabs.setTabText(0, '7i96S')
			parent.jointTabs_0.setTabEnabled(5, False)
			parent.boardTW.setTabText(0, '7i96S')
			parent.ipAddressCB.setEnabled(True)
			#pixmap = QPixmap(os.path.join(parent.image_path, '7i96s-card.png'))
			#parent.boardLB.setPixmap(pixmap)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('N/A')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('5', False)
			for i in range(4, -1, -1):
				parent.stepgensCB.addItem(f'{i}', f'{i}')
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)
			for i in range(5):
				getattr(parent, f'c0_stepgenGB_{i}').setVisible(True)
				getattr(parent, f'c0_analogGB_{i}').setVisible(False)
				getattr(parent, f'c0_encoderGB_{i}').setVisible(False)

		# 6 axes of analog servo 16 isolated inputs 6 isolated outputs
		elif parent.boardCB.currentData() == '7i97':
			parent.boardType = 'eth'
			parent.cardType_0 = 'servo'
			parent.mainTabs.setTabEnabled(3, True)
			parent.mainTabs.setTabEnabled(4, True)
			for i in range(16):
				getattr(parent, f'inputPB_{i}').setEnabled(True)
				getattr(parent, f'inputInvertCB_{i}').setEnabled(True)
				getattr(parent, f'inputDebounceCB_{i}').setEnabled(True)
			for i in range(6):
				getattr(parent, f'outputPB_{i}').setEnabled(True)
			for i in range(16,32):
				getattr(parent, f'inputPB_{i}').setEnabled(False)
				getattr(parent, f'inputInvertCB_{i}').setEnabled(False)
				getattr(parent, f'inputDebounceCB_{i}').setEnabled(False)
			for i in range(6,16):
				getattr(parent, f'outputPB_{i}').setEnabled(False)
			parent.cardTabs.setTabText(0, '7i97')
			parent.jointTabs_0.setTabEnabled(5, True)
			parent.boardTW.setTabText(0, '7i97')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i97-card.png'))
			parent.boardLB.setPixmap(pixmap)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i97-schematic-0.png'))
			parent.schematicLB_0.setPixmap(pixmap)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('N/A')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('N/A', False)
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('6', False)
			for i in range(5, -1, -1):
				parent.pwmgensCB.addItem(f'{i}', f'{i}')
			parent.encodersCB.clear()
			parent.encodersCB.addItem('6', False)
			for i in range(5, -1, -1):
				parent.encodersCB.addItem(f'{i}', f'{i}')
			for i in range(5):
				getattr(parent, f'c0_stepgenGB_{i}').setVisible(False)
				getattr(parent, f'c0_analogGB_{i}').setVisible(True)
				getattr(parent, f'c0_encoderGB_{i}').setVisible(True)

		elif parent.boardCB.currentData() == '7i98':
			parent.boardType = 'eth'
			parent.cardType_0 = ''
			parent.mainTabs.setTabEnabled(3, False)
			parent.mainTabs.setTabEnabled(4, False)
			parent.boardTW.setTabText(0, '7i98')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i98-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('N/A', False)
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)

	else: # No Board Selected
		parent.board = ''
		parent.boardType = ''
		parent.ipAddressCB.setEnabled(False)
		parent.daughterCB_0.setEnabled(False)
		parent.daughterCB_1.setEnabled(False)
		parent.board = ''
		parent.firmwareCB.clear()
		parent.daughterLB_0.setText('N/A')
		parent.daughterLB_1.setText('N/A')
		parent.mainTabs.setTabText(2, 'N/A')
		parent.mainTabs.setTabText(3, 'N/A')
		parent.mainTabs.setTabEnabled(2, False)
		parent.mainTabs.setTabEnabled(3, False)
		parent.stepgensCB.clear()
		parent.pwmgensCB.clear()
		parent.encodersCB.clear()


	'''
	elif parent.boardCB.currentData() == '7i92':
		parent.ipAddressCB.setEnabled(True)
		parent.daughterCB_0.setEnabled(True)
		parent.daughterCB_1.setEnabled(True)
		pixmap = QPixmap(os.path.join(parent.lib_path, '7i92.png'))
		parent.boardLB.setPixmap(pixmap)
		info = ('IP Address 10.10.10.10 is recommended to avoid conflicts on your LAN\n'
						'10.10.10.10 W5 Down W6 Up\n'
						'192.168.1.121 W5 Down W6 Down')
		parent.boardInfoLB.setText(info)
		parent.daughterLB_0.setText('P1')
		parent.daughterLB_1.setText('P2')
		parent.mainTabs.setTabText(2, 'P1')
		parent.mainTabs.setTabText(3, 'P2')
	'''

def firmwareChanged(parent):
	if parent.firmwareCB.currentData():
		#print(parent.boardCB.currentData())
		if parent.boardCB.currentData() in MAIN_BOARDS:

			#print(parent.firmwareCB.currentText()) here
			daughters = getattr(firmware, f'd{parent.board}')(parent)
			if parent.firmwareCB.currentText() in daughters:
				cards = daughters[parent.firmwareCB.currentText()]
				parent.daughterCB_0.clear()
				if cards[0]:
					parent.daughterCB_0.addItem('Select', False)
					parent.daughterCB_0.addItem(cards[0], cards[0])
				parent.daughterCB_1.clear()
				if cards[1]:
					parent.daughterCB_1.addItem('Select', False)
					parent.daughterCB_1.addItem(cards[1], cards[1])
			path = os.path.splitext(parent.firmwareCB.currentData())[0]
			bitfile = os.path.join(path + '.pin')
			if os.path.exists(bitfile):
				with open(bitfile, 'r') as file:
					data = file.read()
				parent.machinePTE.clear()
				parent.machinePTE.setPlainText(data)
			else:
				parent.machinePTE.clear()
				parent.machinePTE.setPlainText(f'No pin file found for {parent.firmwareCB.currentText()}')
			options = getattr(firmware, f'o{parent.board}')(parent)
			# options stepgens, pwmgens, qcount
			if parent.firmwareCB.currentText() in options:
				#print(options[parent.firmwareCB.currentText()])
				parent.stepgensCB.clear()
				if options[parent.firmwareCB.currentText()][0]:
					for i in range(options[parent.firmwareCB.currentText()][0], -1, -1):
						parent.stepgensCB.addItem(f'{i}', f'{i}')
					#parent.stepgensCB.addItem(options[parent.firmwareCB.currentText()][0])
				parent.pwmgensCB.clear()
				if options[parent.firmwareCB.currentText()][1]:
					for i in range(options[parent.firmwareCB.currentText()][1], -1, -1):
						parent.pwmgensCB.addItem(f'{i}', f'{i}')
					#parent.pwmgensCB.addItem(options[parent.firmwareCB.currentText()][1])
				parent.encodersCB.clear()
				if options[parent.firmwareCB.currentText()][2]:
					for i in range(options[parent.firmwareCB.currentText()][2], -1, -1):
						parent.encodersCB.addItem(f'{i}', f'{i}')
	else:
		parent.machinePTE.clear()

def daughterCardChanged(parent):
	if parent.sender().currentData() == None:
		return
	#motherBoards = ['5i25', '7i80db', '7i80hd', '7i92', '7i93', '7i98']
	axes = {'7i33': '4', '7i47': '6', '7i76': '5', '7i77': '6', '7i78': '4', '5ABOB': '5'}
	inputs = {'7i76': '32', '7i77': '32', '7i78': '0', '5ABOB': '5'}
	outputs = {'7i76': '16', '7i77': '16', '7i78': '0', '5ABOB': '1'}
	stepper = ['7i76', '7i78']
	servo = ['7i77']
	cardType = {'7i33': 'servo', '7i47': 'step', '7i76': 'step', '7i77': 'servo', '7i78': 'step', '5ABOB': 'step'}

	if parent.sender().currentText() == 'Select':
		parent.daughterCB_0.setEnabled(True)
		parent.daughterCB_1.setEnabled(True)
		parent.mainTabs.setTabEnabled(3, False)
		parent.mainTabs.setTabEnabled(4, False)
	else:
		if parent.sender().objectName() == 'daughterCB_0':
			parent.daughterCB_1.setEnabled(False)
		elif parent.sender().objectName() == 'daughterCB_1':
			parent.daughterCB_0.setEnabled(False)
		parent.mainTabs.setTabEnabled(3, True)
		parent.mainTabs.setTabEnabled(4, True)

		parent.cardTabs.setTabText(0, parent.sender().currentData())
		parent.cardType_0 = cardType[parent.sender().currentData()]

		if axes[parent.sender().currentData()] == '6':
			parent.jointTabs_0.setTabEnabled(4, True)
			parent.jointTabs_0.setTabEnabled(5, True)
		elif axes[parent.sender().currentData()] == '5':
			parent.jointTabs_0.setTabEnabled(4, True)
			parent.jointTabs_0.setTabEnabled(5, False)
		elif axes[parent.sender().currentData()] == '4':
			parent.jointTabs_0.setTabEnabled(4, False)
			parent.jointTabs_0.setTabEnabled(5, False)

		if parent.daughterCB_0.currentData():
			if cardType[parent.daughterCB_0.currentData()] == 'step':
				for i in range(5):
					getattr(parent, f'c0_stepgenGB_{i}').setVisible(True)
					getattr(parent, f'c0_analogGB_{i}').setVisible(False)
					getattr(parent, f'c0_encoderGB_{i}').setVisible(False)
			elif cardType[parent.daughterCB_0.currentData()] == 'servo':
				for i in range(5):
					getattr(parent, f'c0_stepgenGB_{i}').setVisible(False)
					getattr(parent, f'c0_analogGB_{i}').setVisible(True)
					getattr(parent, f'c0_encoderGB_{i}').setVisible(True)

		if parent.daughterCB_1.currentData():
			if cardType[parent.daughterCB_1.currentData()] == 'step':
				for i in range(5):
					getattr(parent, f'c0_stepgenGB_{i}').setVisible(True)
					getattr(parent, f'c0_analogGB_{i}').setVisible(False)
					getattr(parent, f'c0_encoderGB_{i}').setVisible(False)
			elif cardType[parent.daughterCB_1.currentData()] == 'servo':
				for i in range(5):
					getattr(parent, f'c0_stepgenGB_{i}').setVisible(False)
					getattr(parent, f'c0_analogGB_{i}').setVisible(True)
					getattr(parent, f'c0_encoderGB_{i}').setVisible(True)


	'''

			for i in range(32):
				getattr(parent, f'inputDebounceCB_{i}').setEnabled(False)


		#parent.mainTabs.setTabEnabled(4, True)
		# only allow one daughter card



			if parent.boardCB.currentData() in motherBoards:


			parent.cardType_1 = cardType[parent.sender().currentData()]
			if parent.boardCB.currentData() in motherBoards:
				parent.mainTabs.setTabEnabled(3, True)
				parent.cardTabs.setTabText(1, parent.sender().currentData())
				parent.cardTabs.setCurrentIndex(1)
				if axes[parent.sender().currentData()] == '6':
					parent.jointTabs_1.setTabEnabled(4, True)
					parent.jointTabs_1.setTabEnabled(5, True)
				elif axes[parent.sender().currentData()] == '5':
					parent.jointTabs_1.setTabEnabled(4, True)
					parent.jointTabs_1.setTabEnabled(5, False)
				elif axes[parent.sender().currentData()] == '4':
					parent.jointTabs_1.setTabEnabled(4, False)
					parent.jointTabs_1.setTabEnabled(5, False)


			parent.cardTabs.setTabEnabled(0, True)

		else:
			parent.cardTabs.setTabEnabled(0, False)
		if parent.daughterCB_1.currentData():
			parent.cardTabs.setTabEnabled(1, True)
			if cardType[parent.daughterCB_1.currentData()] == 'step':
				for i in range(5):
					getattr(parent, f'c1_stepgenGB_{i}').setVisible(True)
					getattr(parent, f'c1_analogGB_{i}').setVisible(False)
					getattr(parent, f'c1_encoderGB_{i}').setVisible(False)
			elif cardType[parent.daughterCB_1.currentData()] == 'servo':
				for i in range(5):
					getattr(parent, f'c1_stepgenGB_{i}').setVisible(False)
					getattr(parent, f'c1_analogGB_{i}').setVisible(True)
					getattr(parent, f'c1_encoderGB_{i}').setVisible(True)
			dinput = int(inputs[parent.daughterCB_1.currentData()])
			doutput = int(outputs[parent.daughterCB_1.currentData()])

			for i in range(dinput):
				getattr(parent, f'inputPB_{i}').setEnabled(True)
			for i in range(doutput):
				getattr(parent, f'outputPB_{i}').setEnabled(True)
			for i in range(dinput,32):
				getattr(parent, f'inputPB_{i}').setEnabled(False)
			for i in range(doutput,16):
				getattr(parent, f'outputPB_{i}').setEnabled(False)
		else:
			parent.cardTabs.setTabEnabled(1, False)
	else:
			parent.daughterCB_0.setEnabled(True)
			parent.daughterCB_1.setEnabled(True)


	if parent.daughterCB_0.currentText() != 'Select':
		parent.mainTabs.setTabEnabled(2, True)
	else:
		parent.mainTabs.setTabEnabled(2, False)

	if parent.daughterCB_1.currentText() != 'Select':
		parent.mainTabs.setTabEnabled(3, True)
	else:
		parent.mainTabs.setTabEnabled(3, False)

	if getattr(parent, f'{parent.sender().objectName()}').currentText() == '7i76':
		if parent.sender().objectName() == 'daughterCB_0':
			parent.jointTabs_0.setTabEnabled(5, False)
			parent.joints = 5
			for i in range(5):
				getattr(parent, f'p1_stepgenGB_{i}').setVisible(True)
				getattr(parent, f'p1_analogGB_{i}').setVisible(False)
				getattr(parent, f'p1_encoderGB_{i}').setVisible(False)

		if parent.sender().objectName() == 'daughterCB_1':
			parent.jointTabs_1.setTabEnabled(5, False)
			parent.joints = 5
			for i in range(5):
				getattr(parent, f'p2_stepgenGB_{i}').setVisible(True)
				getattr(parent, f'p2_analogGB_{i}').setVisible(False)
				getattr(parent, f'p2_encoderGB_{i}').setVisible(False)

	if getattr(parent, f'{parent.sender().objectName()}').currentText() == '7i77':
		if parent.sender().objectName() == 'daughterCB_0':
			parent.jointTabs_0.setTabEnabled(4, True)
			parent.jointTabs_0.setTabEnabled(5, True)
			parent.joints = 6
			for i in range(6):
				getattr(parent, f'p1_analogGB_{i}').setVisible(True)
				getattr(parent, f'p1_encoderGB_{i}').setVisible(True)
				getattr(parent, f'p1_stepgenGB_{i}').setVisible(False)

		if parent.sender().objectName() == 'daughterCB_1':
			parent.jointTabs_1.setTabEnabled(4, True)
			parent.jointTabs_1.setTabEnabled(5, True)
			parent.joints = 6
			for i in range(6):
				getattr(parent, f'p2_analogGB_{i}').setVisible(True)
				getattr(parent, f'p2_encoderGB_{i}').setVisible(True)
				getattr(parent, f'p2_stepgenGB_{i}').setVisible(False)

	if getattr(parent, f'{parent.sender().objectName()}').currentText() == '7i78':
		if parent.sender().objectName() == 'daughterCB_0':
			parent.jointTabs_0.setTabEnabled(4, False)
			parent.jointTabs_0.setTabEnabled(5, False)
			parent.joints = 6
			for i in range(6):
				getattr(parent, f'p1_analogGB_{i}').setVisible(False)
				getattr(parent, f'p1_encoderGB_{i}').setVisible(False)
				getattr(parent, f'p1_stepgenGB_{i}').setVisible(True)

		if parent.sender().objectName() == 'daughterCB_1':
			parent.jointTabs_1.setTabEnabled(4, False)
			parent.jointTabs_1.setTabEnabled(5, False)
			parent.joints = 6
			for i in range(6):
				getattr(parent, f'p2_analogGB_{i}').setVisible(False)
				getattr(parent, f'p2_encoderGB_{i}').setVisible(False)
				getattr(parent, f'p2_stepgenGB_{i}').setVisible(True)
	'''

def connectorChanged(parent):
	if parent.connectorCB.currentText() == 'P1':
		parent.ioPort = '3'
		parent.analogPort = '4'
	if parent.connectorCB.currentText() == 'P2':
		parent.ioPort = '0'
		parent.analogPort = '1'

def updateAxisInfo(parent):
	if parent.sender().objectName() == 'actionOpen':
		return
	card = parent.sender().objectName()[:2]
	joint = parent.sender().objectName()[-1]
	scale = getattr(parent, f'{card}_scale_' + joint).text()
	if scale and isNumber(scale):
		scale = float(scale)
	else:
		return

	maxVelocity = getattr(parent, f'{card}_maxVelocity_' + joint).text()
	if maxVelocity and isNumber(maxVelocity):
		maxVelocity = float(maxVelocity)
	else:
		return

	maxAccel = getattr(parent, f'{card}_maxAccel_' + joint).text()
	if maxAccel and isNumber(maxAccel):
		maxAccel = float(maxAccel)
	else:
		return

	if parent.linearUnitsCB.currentData():
		accelTime = maxVelocity / maxAccel
		getattr(parent, f'{card}_timeJoint_' + joint).setText(f'{accelTime:.2f} seconds')
		accelDistance = accelTime * 0.5 * maxVelocity
		getattr(parent, f'{card}_distanceJoint_' + joint).setText(f'{accelDistance:.2f} {parent.linearUnitsCB.currentData()}')
		stepRate = scale * maxVelocity
		getattr(parent, f'{card}_stepRateJoint_' + joint).setText(f'{abs(stepRate):.0f} pulses')

def unitsChanged(parent):
	if parent.linearUnitsCB.currentData() == 'mm':
		parent.maxLinearVelLB.setText('mm/sec')
		parent.defaultJogSpeedDSB.setSuffix(' mm/sec')
		parent.jogSpeedLB.setText(f'{parent.defaultJogSpeedDSB.value() * 60} m/min')
		for i in range(6):
			getattr(parent, f'c0_unitsLB_{i}').setText('Vel & Acc\nmm/sec')
	if parent.linearUnitsCB.currentData() == 'inch':
		parent.maxLinearVelLB.setText('in/sec')
		parent.defaultJogSpeedDSB.setSuffix(' in/sec')
		parent.jogSpeedLB.setText(f'{parent.defaultJogSpeedDSB.value() * 60} in/min')
		for i in range(6):
			getattr(parent, f'c0_unitsLB_{i}').setText('Vel & Acc\nin/sec')
	if not parent.linearUnitsCB.currentData():
		parent.maxLinearVelLB.setText('')
		parent.defaultJogSpeedDSB.setSuffix('')
		parent.jogSpeedLB.setText('')
		for i in range(6):
			getattr(parent, f'c0_unitsLB_{i}').setText('Select Units\nMachine Tab')

def axisChanged(parent):
	connector = parent.sender().objectName()[:3]
	joint = parent.sender().objectName()[-1]
	axis = parent.sender().currentText()
	if axis in ['X', 'Y', 'Z', 'U', 'V', 'W']:
		getattr(parent, f'{connector}axisType_{joint}').setText('LINEAR')
	elif axis in ['A', 'B', 'C']:
		getattr(parent, f'{connector}axisType_{joint}').setText('ANGULAR')
	else:
		getattr(parent, f'{connector}axisType_{joint}').setText('')
	coordList = []

	for i in range(6): # Card 0
		axisLetter = getattr(parent, f'c0_axisCB_{i}').currentText()
		if axisLetter != 'Select':
			coordList.append(axisLetter)
		parent.coordinatesLB.setText(''.join(coordList))
		parent.axes = len(parent.coordinatesLB.text())

	for i in range(6): # Card 1
		axisLetter = getattr(parent, f'c1_axisCB_{i}').currentText()
		if axisLetter != 'Select':
			coordList.append(axisLetter)
		parent.coordinatesLB.setText(''.join(coordList))
		parent.axes = len(parent.coordinatesLB.text())

def maxVelChanged(parent, text):
	if text:
		if isNumber(text):
			val = float(text)
			parent.maxVelMinLB.setText(F'{val * 60} units/min')
		else:
			parent.maxVelMinLB.setText('ERROR')
	else:
		parent.maxVelMinLB.setText('  units/min')

def ferrorSetDefault(parent):
	if not parent.linearUnitsCB.currentData():
		QMessageBox.warning(parent,'Warning', 'Machine Tab\nLinear Units\nmust be selected', QMessageBox.Ok)
		return
	connector = parent.sender().objectName()[:2]
	joint = parent.sender().objectName()[-1]
	if parent.linearUnitsCB.currentData() == 'inch':
		getattr(parent, f'{connector}_ferror_{joint}').setText(' 0.0002')
		getattr(parent, f'{connector}_min_ferror_{joint}').setText(' 0.0001')
	else:
		getattr(parent, f'{connector}_ferror_{joint}').setText(' 0.005')
		getattr(parent, f'{connector}_min_ferror_{joint}').setText(' 0.0025')

def pidSetDefault(parent):
	connector = parent.sender().objectName()[:2]
	joint = parent.sender().objectName()[-1]
	if not parent.linearUnitsCB.currentData():
		QMessageBox.warning(parent,'Warning', 'Machine Tab\nLinear Units\nmust be selected', QMessageBox.Ok)
		return
	if joint == 's':
		getattr(parent, 'p_s').setValue(0)
		getattr(parent, 'i_s').setValue(0)
		getattr(parent, 'd_s').setValue(0)
		getattr(parent, 'ff0_s').setValue(1)
		getattr(parent, 'ff1_s').setValue(0)
		getattr(parent, 'ff2_s').setValue(0)
		getattr(parent, 'bias_s').setValue(0)
		getattr(parent, 'maxOutput_s').setValue(0)
		getattr(parent, 'maxError_s').setValue(0)
		getattr(parent, 'deadband_s').setValue(0)
		return

	p = int(1000/(int(parent.servoPeriodSB.cleanText())/1000000))
	getattr(parent,  f'{connector}_p_{joint}').setText(f'{p}')
	getattr(parent, f'{connector}_i_{joint}').setText('0')
	getattr(parent, f'{connector}_d_{joint}').setText('0')
	getattr(parent, f'{connector}_ff0_{joint}').setText('0')
	getattr(parent, f'{connector}_ff1_{joint}').setText('1')
	getattr(parent, f'{connector}_ff2_{joint}').setText('0')
	getattr(parent, f'{connector}_bias_{joint}').setText('0')
	getattr(parent, f'{connector}_maxOutput_{joint}').setText('0')
	if parent.linearUnitsCB.itemData(parent.linearUnitsCB.currentIndex()) == 'inch':
		maxError = '0.0005'
	else:
		maxError = '0.0127'
	getattr(parent, f'{connector}_maxError_{joint}').setText(maxError)
	getattr(parent, f'{connector}_deadband_{joint}').setText('0')

def analogSetDefault(parent): # think this is broken...
	#tab = parent.sender().objectName()[-1]
	connector = parent.sender().objectName()[:2]
	joint = parent.sender().objectName()[-1]
	getattr(parent, f'{connector}_analogMinLimit_{joint}').setText('-10')
	getattr(parent, f'{connector}_analogMaxLimit_{joint}').setText('10')
	getattr(parent, f'{connector}_analogScaleMax_{joint}').setText('10')

def driveChanged(parent):
	timing = parent.sender().itemData(parent.sender().currentIndex())
	connector = parent.sender().objectName()[:3]
	joint = parent.sender().objectName()[-1]
	if timing:
		getattr(parent, f'{connector}stepTime_{joint}').setText(timing[0])
		getattr(parent, f'{connector}stepSpace_{joint}').setText(timing[1])
		getattr(parent, f'{connector}dirSetup_{joint}').setText(timing[2])
		getattr(parent, f'{connector}dirHold_{joint}').setText(timing[3])
		getattr(parent, f'{connector}stepTime_{joint}').setEnabled(False)
		getattr(parent, f'{connector}stepSpace_{joint}').setEnabled(False)
		getattr(parent, f'{connector}dirSetup_{joint}').setEnabled(False)
		getattr(parent, f'{connector}dirHold_{joint}').setEnabled(False)
	else:
		getattr(parent, f'{connector}stepTime_{joint}').setEnabled(True)
		getattr(parent, f'{connector}stepSpace_{joint}').setEnabled(True)
		getattr(parent, f'{connector}dirSetup_{joint}').setEnabled(True)
		getattr(parent, f'{connector}dirHold_{joint}').setEnabled(True)

def plcOptions():
	return ['ladderRungsSB', 'ladderBitsSB', 'ladderWordsSB',
	'ladderTimersSB', 'iecTimerSB', 'ladderMonostablesSB', 'ladderCountersSB',
	'ladderInputsSB', 'ladderOutputsSB', 'ladderExpresionsSB',
	'ladderSectionsSB', 'ladderSymbolsSB', 'ladderS32InputsSB',
	'ladderS32OuputsSB', 'ladderFloatInputsSB', 'ladderFloatOutputsSB']

def updateJointInfo(parent):
	if parent.sender().objectName() == 'actionOpen':
		return
	joint = parent.sender().objectName()[-1]
	scale = getattr(parent, 'scale_' + joint).text()
	if scale and isNumber(scale):
		scale = float(scale)
	else:
		return

	maxVelocity = getattr(parent, 'maxVelocity_' + joint).text()
	if maxVelocity and isNumber(maxVelocity):
		maxVelocity = float(maxVelocity)
	else:
		return

	maxAccel = getattr(parent, 'maxAccel_' + joint).text()
	if maxAccel and isNumber(maxAccel):
		maxAccel = float(maxAccel)
	else:
		return

	if not parent.linearUnitsCB.currentData():
		parent.errorDialog('Machine Tab:\nLinear Units must be selected')
		return
	accelTime = maxVelocity / maxAccel
	getattr(parent, 'timeJoint_' + joint).setText(f'{accelTime:.2f} seconds')
	accelDistance = accelTime * 0.5 * maxVelocity
	getattr(parent, 'distanceJoint_' + joint).setText(f'{accelDistance:.2f} {parent.linearUnitsCB.currentData()}')
	if parent.cardCB.currentData() == '7i76':
		stepRate = scale * maxVelocity
		getattr(parent, 'stepRateJoint_' + joint).setText(f'{abs(stepRate):.0f} pulses')
	else:
		getattr(parent, 'stepRateJoint_' + joint).setText('N/A')

def spindleTypeChanged(parent): 
	if parent.spindleTypeCB.currentData():
		parent.spindleGB.setEnabled(True)
		parent.spindleInfoGB.setEnabled(True)
		parent.encoderGB.setEnabled(True)
		parent.spindlepidGB.setEnabled(True)
		if parent.spindleTypeCB.itemData(parent.spindleTypeCB.currentIndex()) == '1':
			parent.spindleInfo1Lbl.setText("PWM on Step 4")
			parent.tb2p3LB.setText("PWM +")
			parent.tb2p2LB.setText("PWM -")
			parent.spindleInfo2Lbl.setText("Direction on Dir 4")
			parent.tb2p5LB.setText("Direction +")
			parent.tb2p4LB.setText("Direction -")
			parent.spindleInfo3Lbl.setText("Select Enable on the Outputs tab")
		if parent.spindleTypeCB.itemData(parent.spindleTypeCB.currentIndex()) == '2':
			parent.spindleInfo1Lbl.setText("UP on Step 4")
			parent.tb2p3LB.setText("UP +")
			parent.tb2p2LB.setText("UP -")
			parent.spindleInfo2Lbl.setText("Down on Dir 4")
			parent.tb2p5LB.setText("DOWN +")
			parent.tb2p4LB.setText("DOWN -")
			parent.spindleInfo3Lbl.setText("Select Enable on the Outputs tab")
		if parent.spindleTypeCB.itemData(parent.spindleTypeCB.currentIndex()) == '3':
			parent.spindleInfo1Lbl.setText("PDM on Step 4")
			parent.tb2p3LB.setText("PDM +")
			parent.tb2p2LB.setText("PDM -")
			parent.spindleInfo2Lbl.setText("Direction on Dir 4")
			parent.tb2p5LB.setText("Direction +")
			parent.tb2p4LB.setText("Direction -")
			parent.spindleInfo3Lbl.setText("Select Enable on the Outputs tab")
		if parent.spindleTypeCB.itemData(parent.spindleTypeCB.currentIndex()) == '4':
			parent.spindleInfo1Lbl.setText("Direction on Step 4")
			parent.tb2p3LB.setText("Direction +")
			parent.tb2p2LB.setText("Direction -")
			parent.spindleInfo2Lbl.setText("PWM on Dir 4")
			parent.tb2p5LB.setText("PWM +")
			parent.tb2p4LB.setText("PWM -")
			parent.spindleInfo3Lbl.setText("Select Enable on the Outputs tab")

def ssCardChanged(parent):
	sscards = {
	'Select':'No Card Selected',
	'7i64':'24 Outputs, 24 Inputs',
	'7i69':'48 Digital I/O Bits',
	'7i70':'48 Inputs',
	'7i71':'48 Sourcing Outputs',
	'7i72':'48 Sinking Outputs',
	'7i73':'Pendant Card',
	'7i84':'32 Inputs 16 Outputs',
	'7i87':'8 Analog Inputs'
	}

	sspage = {
	'Select':0,
	'7i64':1,
	'7i69':2,
	'7i70':3,
	'7i71':4,
	'7i72':5,
	'7i73':6,
	'7i84':7,
	'7i87':8
	}
	parent.smartSerialInfoLbl.setText(sscards[parent.ssCardCB.currentText()])
	parent.smartSerialSW.setCurrentIndex(sspage[parent.ssCardCB.currentText()])


def ss7i73Changed(parent):
	if parent.ss7i73lcdCB.currentData() == 'w7d': # no LCD
		parent.ss7i73w7Lbl.setText('W7 Down')
		lcd = False
	elif parent.ss7i73lcdCB.currentData() == 'w7u': # LCD
		parent.ss7i73w7Lbl.setText('W7 Up')
		lcd = True
	if parent.ss7i73_keypadCB.currentData()[0] == 'w5d':
		if parent.ss7i73_keypadCB.currentData()[1] == 'w6d': # no keypad
			parent.ss7i73w5Lbl.setText('W5 Down')
			parent.ss7i73w6Lbl.setText('W6 Down')
			keypad = False
		elif parent.ss7i73_keypadCB.currentData()[1] == 'w6u': # 4x8 keypad
			parent.ss7i73w5Lbl.setText('W5 Down')
			parent.ss7i73w6Lbl.setText('W6 Up')
			keypad = True
			keys = '4x8'
	elif parent.ss7i73_keypadCB.currentData()[0] == 'w5u': # 8x8 keypad
			parent.ss7i73w5Lbl.setText('W5 Up')
			parent.ss7i73w6Lbl.setText('W6 Down')
			keypad = True
			keys = '8x8'

	# No LCD No Keypad
	if not lcd and not keypad:
		for i in range(8):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Output {i+10}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(8,16):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Input {i+8}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(inputs, menu)
			button.setMenu(menu)
		for i in range(8):
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(8,12):
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+10}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)

	# LCD No Keypad
	if lcd and not keypad:
		for i in range(8):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Output {i+6}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(8,16):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Input {i+8}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(inputs, menu)
			button.setMenu(menu)
		for i in range(4):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(4,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'LCD {i}')
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(False)

	# LCD 4x8 Keypad
	if lcd and keypad and keys == '4x8':
		for i in range(4):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Output {i+6}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(4,16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(False)
		for i in range(5):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(4,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'LCD {i}')
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(False)

	# LCD 8x8 Keypad
	if lcd and keypad and keys == '8x8':
		for i in range(16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(False)
		for i in range(5):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(4,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'LCD {i}')
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(False)

	# No LCD 4x8 Keypad
	if not lcd and keypad and keys == '4x8':
		for i in range(4):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Output {i+10}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)

		for i in range(4,16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(False)
		for i in range(8):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(8,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+6}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)

	# No LCD 8x8 Keypad
	if not lcd and keypad and keys == '8x8':
		for i in range(16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(False)
		for i in range(12):
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)

def backupFiles(parent):
	if not os.path.exists(parent.configPath):
		parent.machinePTE.setPlainText('Nothing to Back Up')
		return
	backupDir = os.path.join(parent.configPath, 'backups')
	if not os.path.exists(backupDir):
		os.mkdir(backupDir)
	p1 = subprocess.Popen(['find',parent.configPath,'-maxdepth','1','-type','f','-print'], stdout=subprocess.PIPE)
	backupFile = os.path.join(backupDir, f'{datetime.now():%m-%d-%y-%H:%M:%S}')
	p2 = subprocess.Popen(['zip','-j',backupFile,'-@'], stdin=p1.stdout, stdout=subprocess.PIPE)
	p1.stdout.close()
	parent.machinePTE.appendPlainText('Backing up Confguration')
	output = p2.communicate()[0]
	parent.machinePTE.appendPlainText(output.decode())

def fileNew(parent):
	parent.errorMsgOk('Close the Tool,\n Then open', 'Info!')

def fileSaveAs(parent):
	parent.errorMsgOk('Change the Name,\n Then Save', 'Info!')

def copyOutput(parent):
	qclip = QApplication.clipboard()
	qclip.setText(parent.machinePTE.toPlainText())
	parent.statusbar.showMessage('Output copied to clipboard')

def copyhelp(ui, parent):
	qclip = QApplication.clipboard()
	qclip.setText(ui.helpPTE.toPlainText())
	parent.statusbar.showMessage('Output copied to clipboard')

def add_menu(data, menu_obj):
	if isinstance(data, dict):
		for k, v in data.items():
			sub_menu = QMenu(k, menu_obj)
			menu_obj.addMenu(sub_menu)
			add_menu(v, sub_menu)
	elif isinstance(data, list):
		for element in data:
			add_menu(element, menu_obj)
	else:
		action = menu_obj.addAction(data)
		action.setIconVisibleInMenu(False)

def setup(parent):
	parent.mainTabs.setTabEnabled(3, False)
	for i in range(1,4):
		parent.cardTabs.setTabEnabled(i, False)
	pixmap = QPixmap(os.path.join(parent.lib_path, '7i76.png'))
	parent.card7i76LB.setPixmap(pixmap)
	pixmap = QPixmap(os.path.join(parent.lib_path, '7i77.png'))
	parent.card7i77LB.setPixmap(pixmap)

