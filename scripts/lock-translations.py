#!/usr/bin/env python3

import os
import re
import argparse
import configparser
import dateutil.parser
import dateutil.utils
import dateutil
from transifex.api import transifex_api


def get_local_resources(tx_config, project):
    """Read resources in .tx/config and returns a list of resource slug"""
    config = configparser.ConfigParser()
    config.read(tx_config)
    
    try:
      project in re.search('p:[\w-]+:', config.sections()[1]).group(0)
    except:
      print(f"Invalid Transifex configuration file for project '{project}'")
      exit(1)
    
    resources = []
    for section in config.sections():
        section = section.split(":r:", 1)
        
        # Eliminate the main configuration, and remote project identifier
        if section[0] == "main":
            continue
        else:
            resources.append(section[1])
    
    print("Successfully retrieved local resources!")
    
    return resources


def get_remote_resources(project):
    """Return a generator containing all the project's resources"""
    return transifex_api.Resource.filter(project=project).all()
    #TODO: Implement error handling


def get_unused_resources(remote_resources, local_resources):
    """Compare local an remote resources and returns a dict with the unused ones"""
    unused_resources = {}
    for resource in remote_resources:
        if resource.slug not in local_resources: 
            if not resource.accept_translations:
                last_update = dateutil.parser.parse(
                    resource.datetime_modified
                )
                current_time = dateutil.utils.today().replace(tzinfo=dateutil.tz.UTC)
                
                #TODO: double-check the above comparison before enabling deletion                
                delete_status = (current_time - last_update).days >= 3
                print(f"delete_status: {delete_status}")
                if delete_status:
                    #resource.delete()
                    print(f"would delete {resource.slug}")
                
                continue
            
            unused_resources[resource.slug] = resource
    
    return unused_resources


def lock_resources(unused_resources):
    """Lock resources considered as unused, so they can be considered for deletion"""
    #err = False
    for slug in unused_resources:
        resource = unused_resources[slug]
        print(f"Locking {resource.slug}... ")
        resource.attributes['accept_translations'] = False
        resource.save('accept_translations')
        
    # TODO: Implement error handling
        #if response.status_code != 200:
        #    print("Error locking resource:", response, resource)
        #    print(response.content)
        #    err = True
        #else:
        #    print("Successfully locked resource:", resource)
    
    #if err:
    #    print("Script exited with problems!")
    #    exit(1)


def main():
    arg_parser = argparse.ArgumentParser(
        description="locks the unused files on Transifex"
    )
    arg_parser.add_argument("tx_config_path", type=str, help="path to Transifex config")
    arg_parser.add_argument("project_slug", type=str, default='python-newest', help="Project in Transifex (default: python-newest)")
    args = vars(arg_parser.parse_args())

    tx_config_path = args["tx_config_path"]
    project_slug = args["project_slug"]

    print("Using TX Config Path:", tx_config_path)
    print("Using project:", project_slug)
    
    local_resources = get_local_resources(tx_config_path, project_slug)
    
    transifex_api.setup(auth=os.getenv('TX_TOKEN'))
    ORGANIZATION = transifex_api.Organization.get(slug="python-doc")
    PROJECT = ORGANIZATION.fetch('projects').get(slug=project_slug)
    remote_resources = get_remote_resources(PROJECT)

    unused_resources = get_unused_resources(remote_resources, local_resources)

    if len(unused_resources) == 0:
        print("All resources are locked or in use!")
    else:
        for resource in unused_resources:
            print("Unused resource:", resource)
        lock_resources(unused_resources)


if __name__ == "__main__":
    main()
