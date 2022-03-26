import os, configparser
from PyQt5.QtWidgets import (QFileDialog, QLabel, QLineEdit, QSpinBox,
	QDoubleSpinBox, QCheckBox, QGroupBox, QComboBox, QPushButton)

from lib7i92 import loadss

config = configparser.ConfigParser(strict=False)
config.optionxform = str

def openini(parent, configName = ''):
	parent.mainTabs.setCurrentIndex(0)
	parent.machinePTE.clear()
	if not configName: # open file dialog
		if os.path.isdir(os.path.expanduser('~/linuxcnc/configs')):
			configsDir = os.path.expanduser('~/linuxcnc/configs')
		else:
			configsDir = os.path.expanduser('~/')
		fileName = QFileDialog.getOpenFileName(parent,
		caption="Select Configuration INI File", directory=configsDir,
		filter='*.ini', options=QFileDialog.DontUseNativeDialog,)
		iniFile = fileName[0]
	else: # we passed a file name
		configsDir = os.path.expanduser('~/linuxcnc/configs')
		iniFile = os.path.join(configsDir, configName, configName + '.ini')
		if not os.path.isfile(iniFile):
			msg = f'Create and Save the Default File\n{iniFile}'
			parent.errorMsgOk(msg, 'Not Found')
			return
	if iniFile:
		with open(iniFile) as f:
			contents = f.read()
			if 'PNCconf' in contents:
				parent.errorMsgOk('Can not open a PNCconf ini file!', 'Incompatable File')
				return
		parent.machinePTE.appendPlainText(f'Loading {iniFile[0]}')
	else:
		parent.machinePTE.appendPlainText('Open File Cancled')
		iniFile = ''
	if config.read(iniFile):
		if config.has_option('7i92', 'VERSION'):
			iniVersion = config['7i92']['VERSION']
			if iniVersion == parent.version:
				loadini(parent, iniFile)
			else:
				msg = (f'The ini file version is {iniVersion}\n'
					f'The Configuration Tool version is {parent.version}\n'
					'Try and open the ini?')
				if parent.errorMsg(msg, 'Version Difference'):
					loadini(parent, iniFile)
		else:
			msg = ('This ini file may have been built with an older version\n'
				'Try and open?')
			if parent.errorMsg(msg, 'No Version'):
				loadini(parent, iniFile)

def loadini(parent, iniFile):
	# Section, Item, Object Name
	iniList = []
	iniList.append(['7i92', 'CARD', 'cardCB'])
	iniList.append(['7i92', 'CONNECTOR', 'connectorCB'])

	iniList.append(['EMC', 'MACHINE', 'configName'])

	iniList.append(['EMC', 'DEBUG', 'debugCB'])

	iniList.append(['HOSTMOT2', 'IPADDRESS', 'ipAddressCB'])

	iniList.append(['DISPLAY', 'DISPLAY', 'guiCB'])
	iniList.append(['DISPLAY', 'EDITOR', 'editorCB'])
	iniList.append(['DISPLAY', 'POSITION_OFFSET', 'positionOffsetCB'])
	iniList.append(['DISPLAY', 'POSITION_FEEDBACK', 'positionFeedbackCB'])
	iniList.append(['DISPLAY', 'MAX_FEED_OVERRIDE', 'maxFeedOverrideSB'])
	iniList.append(['DISPLAY', 'DEFAULT_LINEAR_VELOCITY', 'defaultJogSpeedDSB'])

	iniList.append(['EMCMOT', 'SERVO_PERIOD', 'servoPeriodSB'])

	iniList.append(['TRAJ', 'LINEAR_UNITS', 'linearUnitsCB'])
	iniList.append(['TRAJ', 'COORDINATES', 'coordinatesLB'])
	iniList.append(['TRAJ', 'MAX_LINEAR_VELOCITY', 'maxLinearVel'])

	for i in range(5):
		iniList.append([f'JOINT_{i}', 'AXIS', f'axisCB_{i}'])
		iniList.append([f'JOINT_{i}', 'DRIVE', f'driveCB_{i}'])
		iniList.append([f'JOINT_{i}', 'STEPLEN', f'stepTime_{i}'])
		iniList.append([f'JOINT_{i}', 'STEPSPACE', f'stepSpace_{i}'])
		iniList.append([f'JOINT_{i}', 'DIRSETUP', f'dirSetup_{i}'])
		iniList.append([f'JOINT_{i}', 'DIRHOLD', f'dirHold_{i}'])
		iniList.append([f'JOINT_{i}', 'MIN_LIMIT', f'minLimit_{i}'])
		iniList.append([f'JOINT_{i}', 'MAX_LIMIT', f'maxLimit_{i}'])
		iniList.append([f'JOINT_{i}', 'MAX_VELOCITY', f'maxVelocity_{i}'])
		iniList.append([f'JOINT_{i}', 'MAX_ACCELERATION', f'maxAccel_{i}'])
		iniList.append([f'JOINT_{i}', 'SCALE', f'scale_{i}'])
		iniList.append([f'JOINT_{i}', 'HOME', f'home_{i}'])
		iniList.append([f'JOINT_{i}', 'HOME_OFFSET', f'homeOffset_{i}'])
		iniList.append([f'JOINT_{i}', 'HOME_SEARCH_VEL', f'homeSearchVel_{i}'])
		iniList.append([f'JOINT_{i}', 'HOME_LATCH_VEL', f'homeLatchVel_{i}'])
		iniList.append([f'JOINT_{i}', 'HOME_FINAL_VEL', f'homeFinalVelocity_{i}'])
		iniList.append([f'JOINT_{i}', 'HOME_USE_INDEX', f'homeUseIndex_{i}'])
		iniList.append([f'JOINT_{i}', 'HOME_IGNORE_LIMITS', f'homeIgnoreLimits_{i}'])
		iniList.append([f'JOINT_{i}', 'HOME_IS_SHARED', f'homeSwitchShared_{i}'])
		iniList.append([f'JOINT_{i}', 'HOME_SEQUENCE', f'homeSequence_{i}'])
		iniList.append([f'JOINT_{i}', 'P', f'p_{i}'])
		iniList.append([f'JOINT_{i}', 'I', f'i_{i}'])
		iniList.append([f'JOINT_{i}', 'D', f'd_{i}'])
		iniList.append([f'JOINT_{i}', 'FF0', f'ff0_{i}'])
		iniList.append([f'JOINT_{i}', 'FF1', f'ff1_{i}'])
		iniList.append([f'JOINT_{i}', 'FF2', f'ff2_{i}'])
		iniList.append([f'JOINT_{i}', 'DEADBAND', f'deadband_{i}'])
		iniList.append([f'JOINT_{i}', 'BIAS', f'bias_{i}'])
		iniList.append([f'JOINT_{i}', 'MAX_OUTPUT', f'maxOutput_{i}'])
		iniList.append([f'JOINT_{i}', 'MAX_ERROR', f'maxError_{i}'])

		iniList.append([f'JOINT_{i}', 'ENCODER_SCALE', f'encoderScale_{i}'])
		iniList.append([f'JOINT_{i}', 'ANALOG_SCALE_MAX', f'analogScaleMax_{i}'])
		iniList.append([f'JOINT_{i}', 'ANALOG_MIN_LIMIT', f'analogMinLimit_{i}'])
		iniList.append([f'JOINT_{i}', 'ANALOG_MAX_LIMIT', f'analogMaxLimit_{i}'])

	iniList.append(['SPINDLE', 'OUTPUT_TYPE', 'spindleTypeCB'])
	iniList.append(['SPINDLE', 'SCALE', 'spindleScale'])
	iniList.append(['SPINDLE', 'PWM_FREQUENCY', 'pwmFrequencySB'])
	iniList.append(['SPINDLE', 'MAX_RPM', 'spindleMaxRpm'])
	iniList.append(['SPINDLE', 'MIN_RPM', 'spindleMinRpm'])
	iniList.append(['SPINDLE', 'DEADBAND', 'deadband_s'])
	iniList.append(['SPINDLE', 'P', 'p_s'])
	iniList.append(['SPINDLE', 'I', 'i_s'])
	iniList.append(['SPINDLE', 'D', 'd_s'])
	iniList.append(['SPINDLE', 'FF0', 'ff0_s'])
	iniList.append(['SPINDLE', 'FF1', 'ff1_s'])
	iniList.append(['SPINDLE', 'FF2', 'ff2_s'])
	iniList.append(['SPINDLE', 'BIAS', 'bias_s'])
	iniList.append(['SPINDLE', 'MAX_ERROR', 'maxError_s'])

	for i in range(32):
		iniList.append(['INPUT_PB', f'INPUT_PB_{i}', f'inputPB_{i}'])
		iniList.append(['INPUT_PB', f'INPUT_INVERT_{i}', f'inputInvertCB_{i}'])

	for i in range(16):
		iniList.append(['OUTPUT_PB', f'OUTPUT_PB_{i}', f'outputPB_{i}'])

	iniList.append(['OPTIONS', 'INTRO_GRAPHIC', 'introGraphicLE'])
	iniList.append(['OPTIONS', 'INTRO_GRAPHIC_TIME', 'splashScreenSB'])
	iniList.append(['OPTIONS', 'MANUAL_TOOL_CHANGE', 'manualToolChangeCB'])
	iniList.append(['OPTIONS', 'CUSTOM_HAL', 'customhalCB'])
	iniList.append(['OPTIONS', 'POST_GUI_HAL', 'postguiCB'])
	iniList.append(['OPTIONS', 'SHUTDOWN_HAL', 'shutdownCB'])
	iniList.append(['OPTIONS', 'HALUI', 'haluiCB'])
	iniList.append(['OPTIONS', 'PYVCP', 'pyvcpCB'])
	iniList.append(['OPTIONS', 'GLADEVCP', 'gladevcpCB'])
	iniList.append(['OPTIONS', 'LADDER', 'ladderGB'])
	iniList.append(['OPTIONS', 'LADDER_RUNGS', 'ladderRungsSB'])
	iniList.append(['OPTIONS', 'BACKUP', 'backupCB'])
	iniList.append(['SSERIAL', 'SS_CARD', 'ssCardCB'])

#iniList.append(['', '', ''])
	# iniList section, item, value
	for item in iniList:
		if config.has_option(item[0], item[1]):
			if isinstance(getattr(parent, item[2]), QLabel):
				getattr(parent, item[2]).setText(config[item[0]][item[1]])
			elif isinstance(getattr(parent, item[2]), QLineEdit):
				getattr(parent, item[2]).setText(config[item[0]][item[1]])
			elif isinstance(getattr(parent, item[2]), QSpinBox):
				getattr(parent, item[2]).setValue(abs(int(config[item[0]][item[1]])))
			elif isinstance(getattr(parent, item[2]), QDoubleSpinBox):
				getattr(parent, item[2]).setValue(float(config[item[0]][item[1]]))
			elif isinstance(getattr(parent, item[2]), QCheckBox):
				getattr(parent, item[2]).setChecked(eval(config[item[0]][item[1]]))
			elif isinstance(getattr(parent, item[2]), QGroupBox):
				getattr(parent, item[2]).setChecked(eval(config[item[0]][item[1]]))
			elif isinstance(getattr(parent, item[2]), QComboBox):
				index = getattr(parent, item[2]).findData(config[item[0]][item[1]])
				if item[1] == 'DRIVE':
					index = getattr(parent, item[2]).findText(config[item[0]][item[1]])
				if index >= 0:
					getattr(parent, item[2]).setCurrentIndex(index)
			elif isinstance(getattr(parent, item[2]), QPushButton):
				getattr(parent, item[2]).setText(config[item[0]][item[1]])

	parent.machinePTE.appendPlainText(f'{iniFile} Loaded')

	if config.has_section('SSERIAL'):
		card = config.get('SSERIAL', 'ssCardCB')
		index = parent.ssCardCB.findText(card)
		if index > 0:
			parent.ssCardCB.setCurrentIndex(index)
		loadss.load(parent, config)
	parent.machinePTE.appendPlainText('Smart Serial file Loaded')
