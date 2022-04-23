# mesact
Mesa Configuration Tool

The Mesa Configuration Tool is designed to create LinuxCNC configuration for the
following boards 5i25, 6i25, 7i76e, 7i80db, 7i80hd, 7i92, 7i93, 7i95, 7i96, 7i97
and 7i98.

The Mesa Configuration Tool will create a complete configuration from scratch.
This way you can modify values in the ini file and when you run the Mesa
Configuration Tool again those changes are not lost.

The Mesa Configuration Tool reads in the ini configuration file for changes.

You can create a configuration then run it with the Axis GUI and use
Machine > Calibration to tune each axis. Save the values to the ini file and
next time you run the Mesa Configuration Tool it will read the values from the
ini file.

The Mesa Configuration Tool requires Python 3.6 or newer to work.

See the [documentation](https://gnipsel.com/mesa/mesact/index.html) for installation and
usage instructions.

Note: The Mesa requires LinuxCNC 2.8 Uspace or newer to work.
[LinuxCNC 2.8](https://gnipsel.com/linuxcnc/uspace/debian10-emc.html)

This has also been tested on Linux Mint 20.2

Using Weblate.org to translate the text.
