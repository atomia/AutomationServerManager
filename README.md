To build the project and produce egg + exe + deb + rpm, you need to have:

* setuptools (apt-get install python-setuptools or equivalent)
* fpm (gem install fpm or equivalent)

Then you just execute:
```
make
```

You can install any of the produced packages manually as per your preference.

To install using setuptools + easy_install, instead do:
```
make install
```

Dependencies:

* The argparse Python Module. To check if this module is installed, try to execute python -c "import argparse; print argparse.__version_". If argparse is installed, this will print the version number. You need version 1.1 or later.

Post-installation:

* Rename atomia.conf.dist file to atomia.conf and put it in the /etc (for Linux) or leave it where it is (for Linux/Windows)
* Update the atomia.conf file with valid username, password and api_url

This product includes binaries covered by the GPLv3, downloaded from the following location:
http://cygwin.com/
