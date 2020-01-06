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

from githubtools import Githubtool

ght = Githubtool(VERBOSE,
                 TEST,
                 clone_dir=rootDir,
                 access_token_file=arguments['-f'],
                 access_token=arguments['-t'])

for repo in ght.local_repos:
    ght.set_origin(repo)
