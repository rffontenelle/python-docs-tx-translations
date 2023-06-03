#!/bin/bash
# Patch POT files to solve incompatibilities with Transifex
# - \\N is treated as new line in Transifex, so it is an ilegal source string

[ $# -lt 1 ] && { echo 'Expected one or more POT file as argument'; exit 1; }

set -xeuo pipefail
IFS=$'\n\t'

tmp=$(mktemp --suffix='.po')
tmp2=$(mktemp --suffix='.po')
trap "rm -f $tmp $tmp2" EXIT

for pot in $@; do
    msggrep -Ke '^\\N$' $pot > $tmp
    msgcomm --no-wrap --less-than=2 $pot $tmp > $tmp2
    mv $tmp2 $pot
done
