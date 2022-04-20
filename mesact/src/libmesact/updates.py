import os, requests
import urllib.request

from packaging import version

from PyQt5.QtWidgets import QApplication, QFileDialog

REPO = 'mesact'

def checkUpdates(parent):
	response = requests.get(f"https://api.github.com/repos/jethornton/{REPO}/releases/latest")
	repoVersion = response.json()["name"]
	if version.parse(repoVersion) > version.parse(parent.version):
		parent.machinePTE.appendPlainText(f'A newer version {repoVersion} is available for download')
	elif version.parse(repoVersion) == version.parse(parent.version):
		parent.machinePTE.appendPlainText(f'The Repo version {repoVersion} is the same as this version')

def downloadDeb(parent):
	directory = str(QFileDialog.getExistingDirectory(parent, "Select Directory"))
	parent.statusbar.showMessage('Checking Repo')
	response = requests.get(f"https://api.github.com/repos/jethornton/{REPO}/releases/latest")
	repoVersion = response.json()["name"]
	parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} Download Starting')
	destination = os.path.join(directory, f'{REPO}_' + repoVersion + '_amd64.deb')
	deburl = os.path.join(f'https://github.com/jethornton/{REPO}/raw/master/{REPO}_' + repoVersion + '_amd64.deb')
	download(parent, deburl, destination)
	parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} Download Complete')

def downloadtZip(parent):
	directory = str(QFileDialog.getExistingDirectory(parent, "Select Directory"))
	parent.statusbar.showMessage('Checking Repo')
	response = requests.get("https://api.github.com/repos/jethornton/{REPO}/releases/latest")
	repoVersion = response.json()["name"]
	parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} Download Starting')
	destination = os.path.join(directory, f'{REPO}_' + repoVersion + '.zip')
	zipurl = 'https://github.com/jethornton/{REPO}/archive/master.zip'
	download(parent, zipurl, destination)
	parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} Download Complete')


def download(parent, down_url, save_loc):
	def Handle_Progress(blocknum, blocksize, totalsize):
		## calculate the progress
		readed_data = blocknum * blocksize
		if totalsize > 0:
			download_percentage = readed_data * 100 / totalsize
			parent.progressBar.setValue(int(download_percentage))
			QApplication.processEvents()
	urllib.request.urlretrieve(down_url, save_loc, Handle_Progress)
	parent.progressBar.setValue(100)
	parent.timer.start(10000)

def clearProgressBar(parent):
	parent.progressBar.setValue(0)
	parent.statusbar.clearMessage()
	parent.machinePTE.clear()
	parent.machinePTE.appendPlainText('Close the Configuration Tool and reinstall')

