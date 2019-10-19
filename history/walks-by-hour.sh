#!/bin/bash

readonly FILE=$1
readonly COUNTS=$(cat "$FILE" \
    | sed -e 's/\([0-9][0-9]\):[0-9][0-9]:[0-9][0-9]\.[0-9]\+/\1:00:00/' \
    | cut -f 1 \
    | sort \
    | uniq -c \
    | sed -e 's/^\s\+\([0-9]\+\)\s\+\(.\+\)/\2	\1/' \
    | sort)

ZEROES=""
for day in $(seq -w 8 14); do
    for hour in $(seq -w 0 23); do
        if ! grep "2019-07-$day $hour" <<<"$COUNTS" > /dev/null; then
            ZEROES+="\n2019-07-$day $hour:00:00	0"
        fi
    done
done

echo -n "Time	Walks"
{ echo "$COUNTS"; echo -e "$ZEROES"; } \
    | grep -v '2019-07-0[1-7]' \
    | sort \
    | sed -e 's/2019-07-08/08 Mon/' \
          -e 's/2019-07-09/09 Tue/' \
          -e 's/2019-07-10/10 Wed/' \
          -e 's/2019-07-11/11 Thu/' \
          -e 's/2019-07-12/12 Fri/' \
          -e 's/2019-07-13/13 Sat/' \
          -e 's/2019-07-14/14 Sun/'
