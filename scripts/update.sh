#!/bin/sh
# Push source strings to Transifex

TX_PROJECT=${1:-python-newest}

[ -n "$CI" ] && set -x
set -e

ROOTDIR=$(realpath "$(dirname $0)/..")

cd "${ROOTDIR}"

if ! test -f cpython/Doc/conf.py; then
  echo "Unable to find proper CPython Doc directory."
  exit 1
fi

# Create POT Files
cd cpython/Doc
sphinx-build -E -b gettext -D gettext_compact=0 -d build/.doctrees . locales/pot

# Generate Transifex configuration file (.tx/config)
cd locales
sphinx-intl create-txconfig
sphinx-intl update-txconfig-resources -p pot -d . --transifex-organization-name python-doc --transifex-project-name "$TX_PROJECT"

if [ "$CI" = true ]; then
    echo 'tx push --source --skip'
fi
