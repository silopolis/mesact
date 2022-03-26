import os
from datetime import datetime

def build(parent):
	filePath = os.path.join(parent.configPath, 'sserial.hal')
	if os.path.exists(filePath):
		os.remove(filePath)
	if parent.ssCardCB.currentData():
		parent.machinePTE.appendPlainText(f'Building {filePath}')
		contents = []
		contents = ['# This file was created with the 7i92 Wizard on ']
		contents.append(datetime.now().strftime('%b %d %Y %H:%M:%S') + '\n')
		contents.append('# If you make changes to this file DO NOT use the Configuration Tool\n\n')
		if parent.ssCardCB.currentIndex() > 0:
			contents.append(f'# Configuration file for the {parent.ssCardCB.currentText()} Smart Serial Card\n\n')

		input_dict = {
			'Joint 0 Home':'net joint-0-home joint.0.home-sw-in <= ',
			'Joint 1 Home':'net joint-1-home joint.1.home-sw-in <= ',
			'Joint 2 Home':'net joint-2-home joint.2.home-sw-in <= ',
			'Joint 3 Home':'net joint-3-home joint.3.home-sw-in <= ',
			'Joint 4 Home':'net joint-4-home joint.4.home-sw-in <= ',
			'Joint 5 Home':'net joint-5-home joint.5.home-sw-in <= ',
			'Joint 6 Home':'net joint-6-home joint.6.home-sw-in <= ',
			'Joint 7 Home':'net joint-7-home joint.7.home-sw-in <= ',
			'Joint 8 Home':'net joint-8-home joint.8.home-sw-in <= ',
			'Home All':'fix me',

			'Joint 0 Plus':'net pos-limit-joint-0 joint.0.pos-lim-sw-in <= ',
			'Joint 0 Minus':'net neg-limit-joint-0 joint.0.neg-lim-sw-in <= ',
			'Joint 0 Both':'net both-limit-joint-0 joint.0.pos-lim-sw-in\n'
				'net both-limit-joint-0 joint.0.neg-lim-sw-in <= ',
			'Joint 1 Plus':'net pos-limit-joint-1 joint.1.pos-lim-sw-in <= ',
			'Joint 1 Minus':'net neg-limit-joint-1 joint.1.neg-lim-sw-in <= ',
			'Joint 1 Both':'net both-limit-joint-1 joint.1.pos-lim-sw-in\n'
				'net both-limit-joint-1 joint.1.neg-lim-sw-in <= ',
			'Joint 2 Plus':'net pos-limit-joint-2 joint.2.pos-lim-sw-in <= ',
			'Joint 2 Minus':'net neg-limit-joint-2 joint.2.neg-lim-sw-in <= ',
			'Joint 2 Both':'net both-limit-joint-2 joint.2.pos-lim-sw-in\n'
				'net both-limit-joint-2 joint.2.neg-lim-sw-in <= ',
			'Joint 3 Plus':'net pos-limit-joint-3 joint.3.pos-lim-sw-in <= ',
			'Joint 3 Minus':'net neg-limit-joint-3 joint.3.neg-lim-sw-in <= ',
			'Joint 3 Both':'net both-limit-joint-3 joint.3.pos-lim-sw-in\n'
				'net both-limit-joint-3 joint..neg-lim-sw-in <= ',
			'Joint 4 Plus':'net pos-limit-joint-4 joint.4.pos-lim-sw-in <= ',
			'Joint 4 Minus':'net neg-limit-joint-4 joint.4.neg-lim-sw-in <= ',
			'Joint 4 Both':'net both-limit-joint-4 joint.4.pos-lim-sw-in\n'
				'net both-limit-joint-4 joint.4.neg-lim-sw-in <= ',
			'Joint 5 Plus':'net pos-limit-joint-5 joint.5.pos-lim-sw-in <= ',
			'Joint 5 Minus':'net neg-limit-joint-5 joint.5.neg-lim-sw-in <= ',
			'Joint 5 Both':'net both-limit-joint-5 joint.5.pos-lim-sw-in\n'
				'net both-limit-joint-5 joint.5.neg-lim-sw-in <= ',
			'Joint 6 Plus':'net pos-limit-joint-6 joint.6.pos-lim-sw-in <= ',
			'Joint 6 Minus':'net neg-limit-joint-6 joint.6.neg-lim-sw-in <= ',
			'Joint 6 Both':'net both-limit-joint-6 joint.6.pos-lim-sw-in\n'
				'net both-limit-joint-6 joint.6.neg-lim-sw-in <= ',
			'Joint 7 Plus':'net pos-limit-joint-7 joint.7.pos-lim-sw-in <= ',
			'Joint 7 Minus':'net neg-limit-joint-7 joint.7.neg-lim-sw-in <= ',
			'Joint 7 Both':'net both-limit-joint-7 joint.7.pos-lim-sw-in\n'
				'net both-limit-joint-7 joint.7.neg-lim-sw-in <= ',
			'Joint 8 Plus':'net pos-limit-joint-8 joint.8.pos-lim-sw-in <= ',
			'Joint 8 Minus':'net neg-limit-joint-8 joint.8.neg-lim-sw-in <= ',
			'Joint 8 Both':'net both-limit-joint-8 joint.8.pos-lim-sw-in\n'
				'net both-limit-joint-8 joint.8.neg-lim-sw-in <= ',

			'Jog X Plus':'net jog-x-plus halui.axis.x.plus <= ',
			'Jog X Minus':'net jog-x-minus halui.axis.x.minus <= ',
			'Jog Y Plus':'net jog-y-plus halui.axis.y.plus <= ',
			'Jog Y Minus':'net jog-y-minus halui.axis.y.minus <= ',
			'Jog Z Plus':'net jog-z-plus halui.axis.z.plus <= ',
			'Jog Z Minus':'net jog-z-minus halui.axis.z.minus <= ',
			'Jog A Plus':'net jog-a-plus halui.axis.a.plus <= ',
			'Jog A Minus':'net jog-a-minus halui.axis.a.minus <= ',
			'Jog B Plus':'net jog-b-plus halui.axis.b.plus <= ',
			'Jog B Minus':'net jog-b-minus halui.axis.b.minus <= ',
			'Jog C Plus':'net jog-c-plus halui.axis.c.plus <= ',
			'Jog C Minus':'net jog-c-minus halui.axis.c.minus <= ',
			'Jog U Plus':'net jog-u-plus halui.axis.u.plus <= ',
			'Jog U Minus':'net jog-u-minus halui.axis.u.minus <= ',
			'Jog V Plus':'net jog-v-plus halui.axis.v.plus <= ',
			'Jog V Minus':'net jog-v-minus halui.axis.v.minus <= ',
			'Jog W Plus':'net jog-w-plus halui.axis.w.plus <= ',
			'Jog W Minus':'net jog-w-minus halui.axis.w.minus <= ',


			'Probe Input':'net probe-input motion.probe-input <= ',
			'Digital 0':'net digital-0-input motion.digital-in-00 <= ',
			'Digital 1':'net digital-1-input motion.digital-in-01 <= ',
			'Digital 2':'net digital-2-input motion.digital-in-02 <= ',
			'Digital 3':'net digital-3-input motion.digital-in-03 <= ',

			'Flood':'net coolant-flood iocontrol.0.coolant-flood <= ',
			'Mist':'net coolant-mist iocontrol.0.coolant-mist <= ',
			'Lube Level':'net lube-level iocontrol.0.lube_level <= ',
			'Tool Changed':'net tool-changed iocontrol.0.tool-changed <= ',
			'Tool Prepared':'net tool-prepared iocontrol.0.tool-prepared <= '
			}

		# build inputs from qpushbutton menus
		for i in range(11):
			key = getattr(parent, 'inputPB_' + str(i)).text()
			invert = '_not' if getattr(parent, 'inputInvertCB_' + str(i)).isChecked() else ''
			if input_dict.get(key, False): # return False if key is not in dictionary
				contents.append(input_dict[key] + f'hm2_7i92.0.gpio.{i:03}.in{invert}\n')
			else: # handle special cases
				if key == 'Home All':
					contents.append('\n# Home All Joints\n')
					contents.append('net home-all ' + f'hm2_7i92.0.gpio.{i:03}.in{invert}\n')
					for i in range(5):
						if getattr(parent, 'axisCB_' + str(i)).currentData():
							contents.append('net home-all ' + f'joint.{i}.home-sw-in\n')
				elif key == 'External E Stop':
					contents.append('\n# External E-Stop\n')
					contents.append('loadrt estop_latch\n')
					contents.append('addf estop-latch.0 servo-thread\n')
					contents.append('net estop-loopout iocontrol.0.emc-enable-in <= estop-latch.0.ok-out\n')
					contents.append('net estop-loopin iocontrol.0.user-enable-out => estop-latch.0.ok-in\n')
					contents.append('net estop-reset iocontrol.0.user-request-enable => estop-latch.0.reset\n')
					contents.append(f'net remote-estop estop-latch.0.fault-in <= hm2_7i92.0.gpio.{i:03}.in{invert}\n\n')


		if parent.ssCardCB.currentText() == '7i64':
			for i in range(24):
				if getattr(parent, 'ss7i64in_' + str(i)).text() != 'Select':
					inPin = getattr(parent, 'ss7i64in_' + str(i)).text()
					contents.append(f'net ss7i64in_{i} hm2_7i92.0.7i64.0.0.input-{i:02} <= {inPin}\n')
			for i in range(24):
				if getattr(parent, 'ss7i64out_' + str(i)).text() != 'Select':
					outPin = getattr(parent, 'ss7i64out_' + str(i)).text()
					contents.append(f'net ss7i64out_{i} hm2_7i92.0.7i64.0.0.output-{i:02} => {outPin}\n')

		elif parent.ssCardCB.currentText() == '7i69':
			for i in range(24):
				if getattr(parent, 'ss7i69in_' + str(i)).text() != 'Select':
					inPin = getattr(parent, 'ss7i69in_' + str(i)).text()
					contents.append(f'net ss7i69in_{i} hm2_7i92.0.7i69.0.0.input-{i:02} <= {inPin}\n')
			for i in range(24):
				if getattr(parent, 'ss7i69out_' + str(i)).text() != 'Select':
					outPin = getattr(parent, 'ss7i69out_' + str(i)).text()
					contents.append(f'net ss7i69out_{i} hm2_7i92.0.7i69.0.0.output-{i:02} => {outPin}\n')

		elif parent.ssCardCB.currentText() == '7i70':
			for i in range(48):
				if getattr(parent, 'ss7i70in_' + str(i)).text() != 'Select':
					inPin = getattr(parent, 'ss7i70in_' + str(i)).text()
					contents.append(f'net ss7i70in_{i} hm2_7i92.0.7i70.0.0.input-{i:02} <= {inPin}\n')

		elif parent.ssCardCB.currentText() == '7i71':
			for i in range(48):
				if getattr(parent, 'ss7i71out_' + str(i)).text() != 'Select':
					inPin = getattr(parent, 'ss7i71out_' + str(i)).text()
					contents.append(f'net ss7i71out_{i} hm2_7i92.0.7i71.0.0.output-{i:02} <= {inPin}\n')

		elif parent.ssCardCB.currentText() == '7i72':
			for i in range(48):
				if getattr(parent, 'ss7i72out_' + str(i)).text() != 'Select':
					inPin = getattr(parent, 'ss7i72out_' + str(i)).text()
					contents.append(f'net ss7i72out_{i} hm2_7i92.0.7i72.0.0.output-{i:02} <= {inPin}\n')

		elif parent.ssCardCB.currentText() == '7i73':
			for i in range(16):
				if getattr(parent, 'ss7i73key_' + str(i)).text() != 'Select':
					keyPin = getattr(parent, 'ss7i73key_' + str(i)).text()
					contents.append(f'net ss7i73key_{i} hm2_7i92.0.7i73.0.0.input-{i:02} <= {keyPin}\n')
			for i in range(12):
				if getattr(parent, 'ss7i73lcd_' + str(i)).text() != 'Select':
					lcdPin = getattr(parent, 'ss7i73lcd_' + str(i)).text()
					contents.append(f'net ss7i73lcd_{i} hm2_7i92.0.7i73.0.0.output-{i:02} => {lcdPin}\n')
			for i in range(16):
				if getattr(parent, 'ss7i73in_' + str(i)).text() != 'Select':
					inPin = getattr(parent, 'ss7i73in_' + str(i)).text()
					contents.append(f'net ss7i73in_{i} hm2_7i92.0.7i73.0.0.input-{i:02} <= {inPin}\n')
			for i in range(2):
				if getattr(parent, 'ss7i73out_' + str(i)).text() != 'Select':
					outPin = getattr(parent, 'ss7i73out_' + str(i)).text()
					contents.append(f'net ss7i73out_{i} hm2_7i92.0.7i84.0.0.output-{i:02} => {outPin}\n')

		elif parent.ssCardCB.currentText() == '7i84':
			for i in range(32):
				if getattr(parent, 'ss7i84in_' + str(i)).text() != 'Select':
					inPin = getattr(parent, 'ss7i84in_' + str(i)).text()
					contents.append(f'net ss7i84in_{i} hm2_7i92.0.7i84.0.0.input-{i:02} <= {inPin}\n')
			for i in range(16):
				if getattr(parent, 'ss7i84out_' + str(i)).text() != 'Select':
					outPin = getattr(parent, 'ss7i84out_' + str(i)).text()
					contents.append(f'net ss7i84out_{i} hm2_7i92.0.7i84.0.0.output-{i:02} => {outPin}\n')

		elif parent.ssCardCB.currentText() == '7i87':
			for i in range(8):
				if getattr(parent, 'ss7i87in_' + str(i)).text() != 'Select':
					inPin = getattr(parent, 'ss7i87in_' + str(i)).text()
					contents.append(f'net ss7i87in_{i} hm2_7i92.0.7i87.0.0.input-{i:02} <= {inPin}\n')

		try:
			with open(filePath, 'w') as f:
				f.writelines(contents)
		except OSError:
			parent.machinePTE.appendPlainText(f'OS error\n {traceback.print_exc()}')
