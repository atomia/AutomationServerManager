#!/bin/sh

if [ -x "/usr/bin/dpkg" ]; then
	# atomia manager package
	./exec_fpm.sh -n atomia-manager -s python -t deb ./setup.py
	python setup.py bdist_wininst
	
	# jsonpath package
	./exec_fpm.sh -n python-jsonpath -s python -t deb jsonpath
	mv dist/*.exe .
elif [ -x "/bin/rpm" ]; then
	./exec_fpm.sh -n atomia-manager -s python -t rpm ./setup.py
	
	./exec_fpm.sh -n python-jsonpath -s python -t rpm jsonpath
else
	echo "unknown platform, exiting"
	exit 1
fi
