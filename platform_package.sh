#!/bin/sh

if [ -x "/usr/bin/dpkg" ]; then
	./exec_fpm.sh -n atomia-manager -s python -t deb ./setup.py
	python setup.py bdist_wininst
	mv dist/*.exe .
elif [ -x "/bin/rpm" ]; then
	./exec_fpm.sh -n atomia-manager -s python -t rpm ./setup.py
else
	echo "unknown platform, exiting"
	exit 1
fi
