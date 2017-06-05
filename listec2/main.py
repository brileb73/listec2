#!/usr/bin/env python
"""
Main file for source of listec2 script
"""
from __future__ import print_function
from argparse import ArgumentParser
import os
import sys
import time
import boto3
from tabulate import tabulate
from six.moves import configparser
from six.moves import input

SETTINGS_FILE = os.path.expanduser('~/.get_ips.ini')
START_TIME = time.time()


def stop_and_tabulate(list_to_tabulate):
    """
    Called at end of execution to output data to stdout.
    Displays execution time and calls sys.exit to allow the script to break early
    """
    sorted_list = sort_by_name(list_to_tabulate)
    print(tabulate(sorted_list, headers='keys', tablefmt='psql'))
    print("[Executed in %s seconds]" % (time.time() - START_TIME))
    sys.exit(0)


def sort_by_name(list_to_sort):
    """
    Sort list by Name attribute
    """
    return sorted(
        list_to_sort,
        cmp=lambda x, y: cmp(x.lower(), y.lower()),
        key=lambda k: k['Name']
    )


def get_args():
    """
    Parse command line arguments based on necessary input
    """
    argsparser = ArgumentParser(prog='listec2', description='List running AWS EC2 servers')
    argsparser.add_argument('-p', '--profile', help='awscli configured profile')
    argsparser.add_argument(
        '-x',
        '--no-early-exit',
        action='store_true',
        default=False,
        help='Stop querying different profiles once servers found'
    )
    argsparser.add_argument(
        '--update-config',
        action='store_true',
        help='Force prompt for updating config (forces explicitly set profile to be ignored)'
    )
    argsparser.add_argument(
        'filter_string',
        nargs='?',
        default='',
        help='Filter for specific string in server names'
    )
    return argsparser.parse_args()


def get_profiles(args):
    """
    Find which profile should be used with boto3
    """
    # Use profile from cli if provided
    if args.profile and not args.update_config:
        return [args.profile]

    # Run config to get or set the config file
    config = configparser.ConfigParser()

    if os.path.isfile(SETTINGS_FILE) and not args.update_config:
        # Get profiles from config
        config.read(SETTINGS_FILE)
    else:
        # Get default profiles from user
        try:
            profiles_input = input(
                'Please enter space separated list of profiles to use (ex: bsp tj bst): '
            )
        except KeyboardInterrupt:
            # Avoid ugly stacktrace on ctrl-c in input
            sys.exit(1)
        # Setup config
        config.add_section('profiles')
        config.set('profiles', 'default', profiles_input)
        # Write to config
        config_file = open(SETTINGS_FILE, 'w')
        config.write(config_file)
        config_file.close()

    return config.get('profiles', 'default').split()


def get_ec2_reservations(profile, running_filter):
    """
    Get all instance reservations for a profile
    """
    ec2_client = boto3.Session(profile_name=profile).client('ec2')
    filtered_instances = ec2_client.describe_instances(Filters=running_filter)
    return filtered_instances['Reservations']


def main():
    """
    Main function for doing boto3 calls and reading through data
    """
    # Initialize
    args = get_args()
    profiles = get_profiles(args)
    running_filter = [{'Name': 'instance-state-name', 'Values': ['running']}]

    # Sort through servers for a matching name
    matching_list = []
    for profile in profiles:
        filtered_instances = get_ec2_reservations(profile, running_filter)
        for reservation in filtered_instances:
            # Filter for instances with a 'Name' tag that matches filter_string
            instances = [
                instance for instance in reservation['Instances']
                if [
                    tag for tag in instance['Tags']
                    if tag['Key'] == 'Name' and args.filter_string in tag['Value']
                ]
            ]
            # Add matching instances to matching_list
            for instance in instances:
                matching_list.append({
                    'Name': [tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name'][0],
                    'InstanceId': instance['InstanceId'],
                    'PublicDnsName': instance['PublicDnsName'] if instance['PublicDnsName']
                                     else 'No Public DNS',
                    'PrivateIpAddress': instance['PrivateIpAddress'] if instance['PrivateIpAddress']
                                        else 'No Private IP'
                })

        # If flag for full run not added, exit one there instances are found
        if matching_list and not args.no_early_exit:
            stop_and_tabulate(matching_list)

    # Tabulate output once done
    stop_and_tabulate(matching_list)


if __name__ == '__main__':
    main()
