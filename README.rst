listec2
=======

List and filter running AWS EC2 instances. Supports multiple profiles and saving them for easy querying of multiple accounts.

Installation
------------

To install from source, run in the root of the repo::

  pip install -e .


Usage Help
----------

Usage::

  usage: listec2 [-h] [-p PROFILE] [-x] [--update-config] [filter_string]
  
  List running AWS EC2 servers
  
  positional arguments:
    filter_string         Filter for specific string in server names
  
  optional arguments:
    -h, --help            show this help message and exit
    -p PROFILE, --profile PROFILE
                          awscli configured profile
    -x, --no-early-exit   Stop querying different profiles once servers found
    --update-config       Force prompt for updating config (forces explicitly
                          set profile to be ignored)


Use Cases
---------

The listec2 allows storing which profiles to use and will loop through the profiles searching for matching servers until some are found in an account.
By default the script will exit and show output as soon as servers are matched to avoid extended wait times.

To store the list of profiles, run the listec2 command with the `--update-config` option and the command will prompt for input of the new list of profiles.

To use with a single profile or avoid getting a prompt for profiles use the `--profile|-p` option to specify the profile to use.
