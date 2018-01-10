#!/bin/sh

gem=`whereis gem | head -n 1 | awk '{ print $2 }'`

if [ -z "$gem" ] || [ ! -x "$gem" ]; then
	echo "ruby gems not found, assuming fpm isn't installed"
	exit 1
fi

ruby=`head -n 1 "$gem" | sed 's/^#!//' | grep ruby`
if [ -z "$ruby" ]; then
	echo "$gem isn't ruby gems, assuming fpm isn't installed"
	exit 1
fi

fpm=`find /var/lib/gems/ /usr/local/share/gems/ /usr/lib*/ruby/gems/ -path "*/gems/fpm-*/bin/fpm" 2> /dev/null`
if [ -z "$fpm" ]; then
	echo "didn't find fpm, assuming it isn't installed"
	exit 1
fi

"$ruby" "$fpm" $@
