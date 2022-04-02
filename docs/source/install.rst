==========
Installing
==========

Mesa Configuration Tool

.. Note:: Tested on Debian 10, and Linux Mint 20.2 but it should work on
	other Debian type OS's.

.. Note:: Requires Python 3.6 or newer to work.

I now have a Debian deb for installing the Mesa Configuration Tool!!!

Download the `deb <https://github.com/jethornton/mesact/raw/master/mesact_0.1.0_amd64.deb>`_

Or use wget from a terminal
::

	wget https://github.com/jethornton/mesact/raw/master/mesact_0.1.0_amd64.deb

If you get `bash: wget: command not found` you can install it from a terminal with
::

	sudo apt install wget

Check the readme.md file for the latest deb and md5sum.

Open the File Manager and right click on the file and open with Gdebi then install.

If you don't have Gdebi installed you can install it from a terminal
::

	sudo apt install gdebi

If you don't have LinuxCNC installed then the mesact Configuration tool
will show up in the Applications > Other menu otherwise it will be in
the CNC menu.

To flash firmware to the mesact you need to install 
`mesaflash <https://github.com/LinuxCNC/mesaflash>`_ from the LinuxCNC
repository.

To uninstall the mesact Configuration Tool right click on the .deb file
and open with Gdebi and select `Remove Package`.

To upgrade the mesact Configuration Tool delete the .deb file and download
a fresh copy then right click on the .deb file and open with Gdebi and
select `Reinstall Package`

