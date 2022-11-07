#!/usr/bin/env python3
# Fetches the project's language list and output to be used by tx-pull.
# Example of output: de,pt_BR,zh_CN

from transifex.api import transifex_api
import getpass
import re
import os

api_token = ""
transifexrc = os.path.expanduser("~") + '/.transifexrc'

# Try to read the API token from .transifexrc configuration file
if os.path.isfile(transifexrc):
    with open(transifexrc,"r") as config:
        pattern='^token\s+=\s+'
        for line in config:
            if re.match(pattern + '\d/\w+',line):
                api_token = re.sub(pattern,'',line.rstrip('\n'))
                break

# Prompt the user for the API token as a second attempt
if not api_token:
    api_token = getpass.getpass(prompt='Transifex APIv3 token: ')

# Query Transifex for the project's data
transifex_api.setup(auth=api_token)
organization = transifex_api.Organization.get(slug="python-doc")
project = organization.fetch('projects').get(slug="python-newest")

# Populate a list with the languages with transltion in the project
lang_list = []
for language in project.fetch('languages'):
    lang = re.sub('(.*<Language: l:|>.*)','',str(language))
    lang_list.append(lang)

# Transform into a string, adjusting to be used by tx-pull
lang_to_pull = re.sub('("|\'| |\[|\])','',str(lang_list))

print(lang_to_pull)
