#!/usr/bin/env python
"""Usage:
  fixorigin.py [(-v|--verbose) --test (-t ACCESS_TOKEN|-f ACCESS_TOKEN_FILE)] DIR
  fixorigin.py (-h|--help)

Search for Github repositories in DIR using Github oAuth specified by ACCESS_TOKEN
or in ACCESS_TOKEN_FILE; for every git found under DIR make sure remote origin set to clone_url.

Arguments:
  DIR            root directory to search for gits

Options:
  -h --help             show this screen.
  -v --verbose          verbose mode
  --test                test mode
  -t ACCESS_TOKEN       specify ACCESS_TOKEN directly, takes precedence over ACCESS_TOKEN_FILE
  -f ACCESS_TOKEN_FILE  specify file in working directory with ACCESS_TOKEN [default: .oAuth]
"""
from docopt import docopt

if __name__ == '__main__':
	config = docopt(__doc__)
	rootDir = config['DIR']
	TEST = config['--test']
	VERBOSE = config['--verbose']
	if TEST or VERBOSE:
		print(config)

import os
import pygit2
from github import Github
from githubtools import *

ACCESS_TOKEN = set_access_token(config)
g=Github(ACCESS_TOKEN)

def fix_remote_origin(repo):
	try:
		repo.remotes['origin']: # check if remote origin exists
	except:
		if TEST or VERBOSE:
			print(f"{repo.path} does not have an origin remote.")
	else:
		if TEST or VERBOSE:
			print(f"Fetching {repo.remotes['origin'].url}...")
		origin_repo = get_github_repo_from_url(g,repo.remotes['origin'].url,config) # repo = g.get_repo(remote origin)
		if repo.remotes['origin'].url != origin_repo.clone_url:
			if TEST or VERBOSE:
				print(f"Fixing origin to {origin_repo.clone_url}...")
			if not TEST:
				repo.remotes.set_url('origin',origin_repo.clone_url)
		if TEST or VERBOSE:
			print(f"Done.")


for root, dirs, files in os.walk(rootDir): # traverse root
	if TEST: print(f"Traversing {root}...")
	if pygit2.discover_repository(root): # if dirName is git
	    repo = pygit2.Repository(pygit2.discover_repository(root))
		fix_remote_origin(repo)
		dirs[:] = [] # exclude subdirs of git
