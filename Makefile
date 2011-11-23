all: clean rpm deb pip exe semiclean

rpm:
	fpm -s python -t rpm ./setup.py

deb:
	fpm -s python -t deb ./setup.py

pip:
	python setup.py bdist_egg
	mv dist/*.egg .
	git clean -fdx

exe:
	python setup.py bdist_wininst
	mv dist/*.egg .
	git clean -fdx

clean:
	git clean -fdx

semiclean:
	$(eval TMP_ART := $(shell mktemp -d))
	mv *.egg *.exe *.deb *.rpm $(TMP_ART)
	git clean -fdx
	mv $(TMP_ART)/* .
	rm -rf $(TMP_ART)

install: clean _install clean

_install:
	python setup.py install
