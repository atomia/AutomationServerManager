all: clean platform_package pip

.PHONY: platform_package pip clean semiclean install _install

platform_package:
	./platform_package.sh
	make semiclean

pip:
	python setup.py bdist_egg
	mv dist/*.egg .
	make semiclean

clean:
	git clean -fdx

semiclean:
	$(eval TMP_ART := $(shell mktemp -d))
	$(shell mv *.egg *.exe *.deb *.rpm $(TMP_ART) 2>&1 | grep -v "cannot stat")
	git clean -fdx
	mv $(TMP_ART)/* .
	rm -rf $(TMP_ART)

install: clean _install clean

_install:
	python setup.py install
