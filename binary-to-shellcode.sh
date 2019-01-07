#!/usr/bin/env bash

# Script that outputs contents of binary or object as shellcode.

if [[ ${#} -lt 1 ]]; then
    echo "> Usage: ${0} [Binary|Object]"
    echo '> Exiting.'
    exit 1
fi

BINARY="${1}"

if [[ ! -f ${BINARY} ]]; then
    echo "> Specified Binary|Object doesn't exist."
    echo '> Exiting.'
    exit 1
fi

for i in $(objdump -d ${BINARY} | grep '^ ' | cut -f2)
do
    echo -n "\x${i}"
done

echo

