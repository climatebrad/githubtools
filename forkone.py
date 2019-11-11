#!/usr/bin/env python
"""Usage:
  forkone.py [(-v|--verbose) --test  --fork --clone --old --upstream]
             [--locals=<list>  --dir=<dir>]
             [(-t ACCESS_TOKEN|-f ACCESS_TOKEN_FILE)] REPO
  forkone.py (-h|--help)

Search for Github repository REPO "owner/repo" using Github oAuth specified by ACCESS_TOKEN
or in ACCESS_TOKEN_FILE; optionally fork to the user's Github directory, clone locally, and
add upstream remote.

Arguments:
  REPO             repository name to search Github repositories for in form "owner/repo"

Options:
  -h --help             show this screen.
  -v --verbose          verbose mode
  --test                test mode (no write)
  --fork                fork matching repository
  --clone               clone matching forked repository, if it exists
  --upstream            add remote upstream to cloned repo, if it exists
  --old                 do clone and/or upstream even if repository already forked
  --locals=<list>       specify file name where names of local repos are listed [default: git_list]
  --dir=<dir>           specify <dir> to clone repository into [default: .]
  -t ACCESS_TOKEN       specify ACCESS_TOKEN directly, takes precedence over ACCESS_TOKEN_FILE
  -f ACCESS_TOKEN_FILE  specify file in working directory with ACCESS_TOKEN [default: .oAuth]
"""
from docopt import docopt

if __name__ == '__main__':
	arguments = docopt(__doc__)
	REPO = arguments['REPO']
	TEST = arguments['--test']
	VERBOSE = arguments['--verbose']
	if TEST or VERBOSE:
		print(arguments)

import sys
import time
# get a list of the github repositories we need to fork
# https://python.gotrained.com/search-github-api/
# https://pygithub.readthedocs.io/en/latest/introduction.html
# https://developer.github.com/v3/search/#search-repositories

# library to the Github API
from github import Github

from githubtools import *


# Here's our top-level code:

ACCESS_TOKEN = set_access_token(arguments)
g=Github(ACCESS_TOKEN)

repo = g.get_repo(REPO)

if arguments['--fork']:
	forked_repo = fork_repos(arguments, g, repo)

# we need to give Github time to complete the fork. It would be good to have this be a
# while that can check if the fork is completed and then wait longer
if arguments['--verbose']:
	print("Waiting 3 seconds to give Github time to complete the fork.")
time.sleep(3)

if arguments['--clone']:
	cloned_repo = clone_repos(arguments, forked_repo)

if arguments['--upstream']:
	upstream_remote = add_upstream_repos(arguments, g, cloned_repo)
