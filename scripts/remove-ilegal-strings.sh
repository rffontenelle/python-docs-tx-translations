#!/bin/bash
# Patch POT files to solve incompatibilities with Transifex
# - \\N is treated as new line in Transifex, so it is an ilegal source string

set -euo pipefail
IFS=$'\n\t'

# Check if a valid POT directory was passed in command-line interface.
# If no argument is passed, use current working directory .
if [ $# -lt 1 ]; then
    if [[ "$(basename $PWD)" != "pot" ]]; then
        echo "Error: Not in 'pot' directory and no path to pot directory passed."
        exit 1
    fi
else
    if [ $# -gt 1 ]; then
        echo "Ignoring extra arguments, sticking with '$1' ..."
    fi
    if [[ ! -d $1 || "$(basename $1)" != "pot" ]]; then
        echo "'$1' is not a valid directory. Expected a directory named 'pot'."
    fi
    cd $1
fi

# Create temporary files and set up exit trap
tmp=$(mktemp --suffix='.po')
tmp2=$(mktemp --suffix='.po')
trap 'rm -f $tmp $tmp2' EXIT


# Remove '\\N', an ilegal string in Transifex, otherwise uplading POT fails
remove_slash_n() {
    pot=$1
    msggrep -Ke '^\\N$' $pot > $tmp
    msgcomm --no-wrap --less-than=2 $pot $tmp > $tmp2
    mv $tmp2 $pot
    echo "Removing '\\N' from: $pot"
    powrap $pot
}


# Run patches in POT files known to need them
remove_slash_n library/codecs.pot
remove_slash_n library/re.pot
remove_slash_n reference/lexical_analysis.pot
