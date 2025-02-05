#!/usr/bin/env python

import json
import os
import re
from argparse import ArgumentParser
from pathlib import Path

from transifex.api import transifex_api

# Version number of a new versioned project to create
new_project_version = '3.11'

transifex_api.setup(auth=os.getenv('TX_TOKEN'))

ORG_SLUG = "python-doc"
PROJ_SLUG = "python-newest"
ORGANIZATION = transifex_api.Organization.get(slug=ORG_SLUG)
PROJECT = ORGANIZATION.fetch('projects').get(slug=PROJ_SLUG)
RESOURCES = transifex_api.Resource.filter(project=PROJECT).all()


def __allow_translations_status(status):
    for resource in RESOURCES:
        print(f'{resource.name} ...')
        resource.attributes['accept_translations'] = status
        resource.save('accept_translations')


def lock_resources():
    __allow_translations_status(status=False)


def unlock_resources():
    __allow_translations_status(status=True)


def fetch_translations():
    """Fetch translations from Transifex, remove source lines."""
    pull_return_code = os.system(f'tx pull -all --force --skip')
    if pull_return_code != 0:
        exit(pull_return_code)


def create_project():
    """
    Creates a new Transifex project with versioned name based on python-newest
    vers_proj_* = version project being created
    vers_res_* = resource of version project being created
    p.* = python-newest project
    r.* = resource of python-newest project  
    
    """
    p = PROJECT
    organization = ORGANIZATION
    vers_proj_slug = 'python-' + new_project_version.replace('.', '')
    vers_proj_name = f'Python {new_project_version}'
    print(f'Creating project: {vers_proj_name}')
    versioned_project = transifex_api.Project.create(
        description=vers_proj_name,
        homepage_url=p.attributes.get('homepage_url'),
        instructions_url=p.attributes.get('instructions_url'),
        license=p.attributes.get('license'),
        long_description=p.attributes.get('long_description'),
        machine_translation_fillup=p.attributes.get('machine_translation_fillup'),
        name=vers_proj_name,
        private=p.attributes.get('private'),
        repository_url=p.attributes.get('repository_url'),
        slug=vers_proj_slug,
        tags=p.attributes.get('tags'),
        team=p.fetch('team'),
        organization=organization,
        source_language=p.fetch('source_language'),
        translation_memory_fillup=p.attributes.get('translation_memory_fillup'),
    )
    
    print(f'Creating {vers_proj_name}\'s resources:')
    for r in RESOURCES:
        print(f'r.name ...')
        transifex_api.Resource.create(
            project=versioned_project,
            i18n_format=r.i18n_format,
            slug=r.slug,
            name=r.name,
            priority=r.priority,
            accept_translations=True
        )


if __name__ == "__main__":
    RUNNABLE_SCRIPTS = ('lock_resources', 'unlock_resources', 'fetch_translations', 'create_project')

    parser = ArgumentParser()
    parser.add_argument('cmd', nargs=1, choices=RUNNABLE_SCRIPTS)
    options = parser.parse_args()

    eval(options.cmd[0])()
