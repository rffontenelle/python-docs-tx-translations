#!/bin/bash
# Remove PO files with 0% translation. Takes a root directory as argument.
# e.g.:
#   remove_untranslated.sh cpython/Doc/locales

set -ex

if [ -n "$1" ]; then
  cd "$1"
fi 

pofiles=$(find * -name '*.po' | sort)
to_remove=()
for po in $pofiles; do
  output=$(LC_ALL=C /usr/bin/msgfmt -cvo /dev/null $po 2>&1 | sed '/:/d;s|,.*||')
  if [[ "$output" == "0 translated messages" ]]; then
    to_remove+=($po)
  fi
done
git rm ${to_remove[@]}
