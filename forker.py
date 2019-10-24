#!/usr/bin/env python
"""Usage:
  forker.py [(-v|--verbose) -n <max> --test  --fork --clone  --upstream  --old --dir=<dir>] KEYWORD
  forker.py [(-t ACCESS_TOKEN|-f ACCESS_TOKEN_FILE)] KEYWORD
  forker.py (-h|--help)

Search for Github repositories matching KEYWORD using Github oAuth specified by ACCESS_TOKEN
or in ACCESS_TOKEN_FILE; optionally fork to the user's Github directory, clone locally, and
add upstream remote.

Arguments:
  KEYWORD             keyword to search Github repositories for

Options:
  -h --help             show this screen.
  -v --verbose          verbose mode
  -n <max>              specify <max> limit of matching repositories
  --test                test mode (no write)
  --fork                fork matching repositories
  --clone               clone matching forked repositories, if they exist
  --upstream            add remote upstream to cloned repos, if they exist
  --old                 add already forked repositories to cloning list
  --dir=<dir>           specify parent <dir> in which to clone repositories [default: ./]
  -t ACCESS_TOKEN       specify ACCESS_TOKEN directly, takes precedence over ACCESS_TOKEN_FILE
  -f ACCESS_TOKEN_FILE  specify file in working directory with ACCESS_TOKEN [default: .oAuth]
"""
from docopt import docopt

if __name__ == '__main__':
	arguments = docopt(__doc__)
	KEYWORD = arguments['KEYWORD']
	TEST = arguments['--test']
	VERBOSE = arguments['--verbose']
	if TEST or VERBOSE:
		print(arguments)

from githubtools import *

# library to the Github API
from github import Github

import time
# Here's our top-level code:

ACCESS_TOKEN = set_access_token(arguments)
g=Github(ACCESS_TOKEN)

repos = search_github_repos(g,KEYWORD,arguments)

if arguments['--fork']:
	forked_repos = fork_repos(g,repos,arguments)

if arguments['--verbose']:
	print("Waiting 5 seconds to give Github time to complete the forks.")
time.sleep(5)

if arguments['--clone']:
	cloned_repos = clone_repos(forked_repos,arguments)

# add upstream connection

if arguments['--upstream']:
	upstream_remotes = add_upstream_repos(g,cloned_repos,arguments)
