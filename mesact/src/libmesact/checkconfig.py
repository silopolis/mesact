
def checkit(parent):
	parent.mainTabs.setCurrentIndex(0)
	configErrors = []
	tabError = False
	nextHeader = 0

	# check the Machine Tab for errors
	if not parent.configName.text():
		tabError = True
		configErrors.append('\tA configuration name must be entered')
	if parent.linearUnitsCB.currentText() == 'Select':
		tabError = True
		configErrors.append('\tLinear Units must be selected')
	if not parent.maxLinearVel.text():
		tabError = True
		configErrors.append('\tMaximum Linear Velocity must be set')
	if parent.boardCB.currentData() and not parent.firmwareCB.currentData():
		tabError = True
		configErrors.append(f'\tFirmware must be selected for {parent.board}')
	if not parent.boardCB.currentData():
		tabError = True
		configErrors.append('\tA Board must be selected')
	if parent.boardType == 'eth' and parent.ipAddressCB.currentText() == 'Select':
		tabError = True
		configErrors.append('\tAn IP address must be selected, 10.10.10.10 is recommended')

	if tabError:
		configErrors.insert(nextHeader, 'Machine Tab:')
		nextHeader = len(configErrors)
		tabError = False
	# end of Machine Tab

	# check the Display Tab for errors
	if parent.guiCB.currentText() == 'Select':
		tabError = True
		configErrors.append('\tA GUI must be selected')
	if parent.positionOffsetCB.currentText() == 'Select':
		tabError = True
		configErrors.append('\tA Position Offset must be selected')
	if parent.positionFeedbackCB.currentText() == 'Select':
		tabError = True
		configErrors.append('\tA Position Feedback must be selected')
	if parent.maxFeedOverrideSB.value() == 0.0:
		tabError = True
		configErrors.append('\tThe Max Feed Override must be greater than zero, 1.2 is suggested')
	if parent.frontToolLatheCB.isChecked() and parent.backToolLatheCB.isChecked():
		configErrors.append('\tOnly one lathe display option can be checked')
		tabError = True
	if tabError:
		configErrors.insert(nextHeader, 'Display Tab:')
		nextHeader = len(configErrors)
		tabError = False
	# end of Display Tab

	# check the Axis Tab for errors
	if len(parent.coordinatesLB.text()) == 0:
		tabError = True
		configErrors.append('\tAt least one Joint must be configured starting with Joint 0')
	else: #check the joints
		# make this a loop getattr(parent, f'_{i}')
		coordinates = parent.coordinatesLB.text()

		for i in range(6):
			if getattr(parent, f'axisCB_{i}').currentText() != 'Select':
				coordinates = coordinates[:1]
				currentAxis = getattr(parent, f"axisCB_{i}").currentText()
				if currentAxis in coordinates: # multiple joints on one axis
					if i != coordinates.index(currentAxis):
						if getattr(parent, f'homeSequence_{coordinates.index(currentAxis)}').text()[0] == '-':
							firstJoint = True
						else:
							firstJoint = False
						if getattr(parent, f'homeSequence_{i}').text()[0] == '-':
							secondJoint = True
						else:
							secondJoint = False
						if not firstJoint and not secondJoint:
							configErrors.append(f'\tThe Home Sequence for a Gantry must be negative for at least one Joint')
							configErrors.append(f'\tEither Joint {coordinates.index(currentAxis)} or Joint {i} must be negative')
				if not getattr(parent, f'scale_{i}').text():
					tabError = True
					configErrors.append(f'\tThe Scale must be specified for Joint {i}')
				if not getattr(parent, f'minLimit_{i}').text():
					tabError = True
					configErrors.append(f'\tThe Mininum Limit for Joint {i} must be specified')
				if not getattr(parent, f'maxLimit_{i}').text():
					tabError = True
					configErrors.append(f'\tThe Maximum Limit for Joint {i} must be specified')
				if not getattr(parent, f'maxVelocity_{i}').text():
					tabError = True
					configErrors.append(f'\tThe Maximum Velocity for Joint {i} must be specified')
				if not getattr(parent, f'maxAccel_{i}').text():
					tabError = True
					configErrors.append(f'\tThe Maximum Acceleration for Joint {i} must be specified')
				if not getattr(parent, f'p_{i}').text():
					tabError = True
					configErrors.append(f'\tThe P for Joint {i} must be specified')
				if not getattr(parent, f'i_{i}').text():
					tabError = True
					configErrors.append(f'\tThe I for Joint {i} must be specified')
				if not getattr(parent, f'd_{i}').text():
					tabError = True
					configErrors.append(f'\tThe D for Joint {i} must be specified')
				if not getattr(parent, f'ff0_{i}').text():
					tabError = True
					configErrors.append(f'\tThe FF0 for Joint {i} must be specified')
				if not getattr(parent, f'ff1_{i}').text():
					tabError = True
					configErrors.append(f'\tThe FF1 for Joint {i} must be specified')
				if not getattr(parent, f'ff2_{i}').text():
					tabError = True
					configErrors.append(f'\tThe FF2 for Joint {i} must be specified')
				# stepper only checks
				if parent.cardCB.currentText() == '7i76':
					if not getattr(parent, f'stepTime_{i}').text():
						tabError = True
						configErrors.append(f'\tThe Step Time for Joint {i} must be specified')
					if not getattr(parent, f'stepSpace_{i}').text():
						tabError = True
						configErrors.append(f'\tThe Step Space for Joint {i} must be specified')
					if not getattr(parent, f'dirSetup_{i}').text():
						tabError = True
						configErrors.append(f'\tThe Direction Setup for Joint {i} must be specified')
					if not getattr(parent, f'dirHold_{i}').text():
						tabError = True
						configErrors.append(f'\tThe Direction Hold for Joint {i} must be specified')
				# servo only checks
				if parent.cardCB.currentText() == '7i77':
					if not getattr(parent, f'analogMinLimit_{i}').text():
						tabError = True
						configErrors.append(f'\tThe Analog Min Limit for Joint {i} must be specified')
					if not getattr(parent, f'analogMaxLimit_{i}').text():
						tabError = True
						configErrors.append(f'\tThe Analog Max Limit for Joint {i} must be specified')
					if not getattr(parent, f'analogScaleMax_{i}').text():
						tabError = True
						configErrors.append(f'\tThe Analog Scale Max for Joint {i} must be specified')
					if not getattr(parent, f'encoderScale_{i}').text():
						tabError = True
						configErrors.append(f'\tThe Encoder Scale for Joint {i} must be specified')

				# add sanity check for home entries
				if getattr(parent, f'home_{i}').text():
					if not isNumber(getattr(parent, f'home_{i}').text()):
						tabError = True
						configErrors.append(f'\tThe Home Location for Joint {i} must be a number')
				if getattr(parent, f'homeOffset_{i}').text():
					if not isNumber(getattr(parent, f'homeOffset_{i}').text()):
						tabError = True
						configErrors.append(f'\tThe Home Offset for Joint {i} must be a number')
				if getattr(parent, f'homeSearchVel_{i}').text():
					if not isNumber(getattr(parent, f'homeSearchVel_{i}').text()):
						tabError = True
						configErrors.append(f'\tThe Home Search Velocity for Joint {i} must be a number')
				if getattr(parent, f'homeLatchVel_{i}').text():
					if not isNumber(getattr(parent, f'homeLatchVel_{i}').text()):
						tabError = True
						configErrors.append(f'\tThe Home Latch Velocity for Joint {i} must be a number')
				if getattr(parent, f'homeSequence_{i}').text():
					if not isNumber(getattr(parent, f'homeSequence_{i}').text()):
						tabError = True
						hs = getattr(parent, f'homeSequence_{i}').text()
						configErrors.append(f'\tThe Home Sequence for Joint {i} must be a number not {hs}')


	if tabError:
		configErrors.insert(nextHeader, 'Axis Tab:')
		nextHeader = len(configErrors)
		tabError = False
	# end of Axis Tab

	# check the I/O Tab for errors
	for i in range(32):
		if getattr(parent, f'inputPB_{i}').text() == 'Home All':
			seq = []
			seqStart = ['-1', '-0', '0', '1']
			for i in range(5):
				if getattr(parent, f'axisCB_{i}').currentText() != 'Select':
					# need to also check for a valid home sequence
					if not isNumber(getattr(parent, f'homeSequence_{i}').text()):
						tabError = True
						e = getattr(parent, f'homeSequence_{i}').text()
						configErrors.append(f'\tThe Home All Input requires the Home Sequence for Joint {i} be a number not {e}')
					else:
						seq.append(getattr(parent, f'homeSequence_{i}').text())
			seqRemoveDups = list(dict.fromkeys(seq))
			seqSorted = sorted(seqRemoveDups)
			if seqSorted[0] not in seqStart:
				tabError = True
				configErrors.append(f'\tThe Home All Input requires the Home Sequence to start with 0 or 1')
			numList = [int(i) for i in seqSorted]
			checkList = list(range(min(numList), max(numList)+1))
			if not numList == checkList:
				tabError = True
				configErrors.append(f'\tThe Home All Input requires the Home Sequence to not skip a number {numList}')


	if tabError:
		configErrors.insert(nextHeader, 'I/O Tab:')
		nextHeader = len(configErrors)
		tabError = False

	# end of I/O Tab


	parent.machinePTE.clear()
	if configErrors:
		checkit.result = '\n'.join(configErrors)
		parent.machinePTE.setPlainText(checkit.result)
		return False
	else:
		parent.machinePTE.setPlainText('Configuration checked OK')
		return True
	
def isNumber(x):
	try:
		float(x)
		return True
	except ValueError:
		return False
