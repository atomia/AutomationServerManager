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
