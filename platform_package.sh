#!/bin/sh

if [ -x "/usr/bin/dpkg" ]; then
	# atomia manager package
	./exec_fpm.sh -n atomia-manager -s python -t deb ./setup.py
	python setup.py bdist_wininst
	
	# jsonpath package
	./exec_fpm.sh -n python-jsonpath -s python -t deb jsonpath
	sh ./exec_fpm.sh -n python-atomia-client -s python -t deb atomia-client/setup.py
	mv dist/*.exe .
elif [ -x "/bin/rpm" ]; then
	./exec_fpm.sh -n atomia-manager -s python -t rpm ./setup.py
	
	./exec_fpm.sh -n python-jsonpath -s python -t rpm jsonpath
	sh ./exec_fpm.sh -n python-atomia-client -s python -t rpm atomia-client
else
	echo "unknown platform, exiting"
	exit 1
fi
