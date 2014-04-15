#!/bin/sh

version_from_file=`cat version.txt`

cat "atomia-client/setup.py.input" | sed -e "s/%VERSION/$version_from_file/g" > "atomia-client/setup.py"

if [ -x "/usr/bin/dpkg" ]; then
	# atomia manager package
	./exec_fpm.sh -n atomia-manager -s python -t deb ./setup.py
	if ! python setup.py bdist_wininst; then
		exit 1
	fi
	
	# jsonpath package
	if ! ./exec_fpm.sh -n python-jsonpath -s python -t deb jsonpath; then
		exit 1
	fi

	if ! sh ./exec_fpm.sh -n python-atomia-client -s python -t deb atomia-client/setup.py; then
		exit 1
	fi
	mv dist/*.exe .
elif [ -x "/bin/rpm" ]; then
	if ! ./exec_fpm.sh -n atomia-manager -s python -t rpm ./setup.py; then
		exit 1
	fi
	
	if ! ./exec_fpm.sh -n python-jsonpath -s python -t rpm jsonpath; then
		exit 1
	fi

	if ! sh ./exec_fpm.sh -n python-atomia-client -s python -t rpm atomia-client; then
		exit 1
	fi
else
	echo "unknown platform, exiting"
	exit 1
fi
