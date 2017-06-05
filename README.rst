listec2
=======

List and filter running AWS EC2 instances. Supports multiple profiles and saving them for easy querying of multiple accounts.

To install from source, run in the root of the repo::

  pip install -e .

Usage::

  usage: listec2 [-h] [-p PROFILE] [-x] [--update-config] [search_regex]
  
  List running AWS EC2 servers
  
  positional arguments:
    search_regex          Regex for filtering servers
  
  optional arguments:
    -h, --help            show this help message and exit
    -p PROFILE, --profile PROFILE
                          awscli configured profile
    -x, --no-early-exit   Stop querying different profiles once servers found
    --update-config       Force prompt for updating config (forces explicitly
                          set profile to be ignored)
  
