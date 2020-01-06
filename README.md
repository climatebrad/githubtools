# githubtools
Toolkit for manipulating local and Github repositories. Including the process of searching, forking and cloning repos to your personal directory.

Built for Flatiron Data Science class after Learn.co removed their automatic forking functionality.

## Usage:

~~~~
from githubtools import Githubtool

ght = Githubtool(clone_dir='..')

keyword = "dc-ds-100719"
repos = ght.search_github_repos(keyword) 

forked_repos = ght.fork_repos(repos)
cloned_repos = ght.clone_repos(forked_repos) # clones into clone_dir
upstream_remotes = ght.add_upstream_repos(cloned_repos)
~~~~


### Initialization Options:
~~~~
Githubtool(
    is_verbose=False,
    is_test=False,
    locals_file='git_list',
    clone_dir='..',
    access_token_file='.oAuth',
    access_token=None
)
~~~~

## Requires:
*	pygit2
*	docopt
*	PyGithub
*	giturlparse

~~~~
	~> pip install docopt==0.6.2
	~> pip install PyGithub
	~> brew install libgit2
	~> pip install pygit2
	~> pip install giturlparse.py
~~~~


# forker.py

Power tool to search for Github repositories matching KEYWORD using Github oAuth specified by ACCESS_TOKEN
or in ACCESS_TOKEN_FILE; optionally fork to the user's Github directory, clone locally, and
add upstream remote.

## Usage:
~~~~
  forker.py [(-v|--verbose) -n <max> --test  --fork --clone --dir=<dir> --upstream] 
            [(-t ACCESS_TOKEN|-f ACCESS_TOKEN_FILE) --user=<username>] KEYWORD ...
  forker.py (-h|--help)
~~~~

### Arguments:
KEYWORD ...
: keywords to search Github repositories for

### Options:
~~~~
  -h --help             show this screen.
  -v --verbose          verbose mode
  -n <max>              specify <max> limit of matching repositories
  --fork                fork matching repositories
  --clone               clone matching forked repositories, if they exist
  --upstream            add remote upstream to cloned repos, if they exist
  --test                test mode (no write)
  --dir=<dir>           specify <dir> to clone repositories [default: ./]
  -t ACCESS_TOKEN       specify ACCESS_TOKEN directly, takes precedence over ACCESS_TOKEN_FILE
  -f ACCESS_TOKEN_FILE  specify file in working directory with ACCESS_TOKEN [default: .oAuth]
  --user=<username>     specify github user to search under
~~~~

# forkone.py

Search for Github repository REPO "owner/repo" using Github oAuth specified by ACCESS_TOKEN
or in ACCESS_TOKEN_FILE; optionally fork to the user's Github directory, clone locally, and
add upstream remote.

## Usage:
~~~~
  forkone.py [(-v|--verbose) --test  --fork --clone --dir=<dir> --upstream] REPO
  forkone.py [(-t ACCESS_TOKEN|-f ACCESS_TOKEN_FILE)] REPO
  forkone.py (-h|--help)
~~~~


### Arguments:
REPO
:  repository name to search Github repositories for in form "owner/repo"

### Options:
~~~~
  -h --help             show this screen.
  -v --verbose          verbose mode
  --fork                fork matching repository
  --clone               clone matching forked repository, if it exists
  --upstream            add remote upstream to cloned repo, if it exists
  --test                test mode (no write)
  --dir=<dir>           specify <dir> to clone repository into [default: ./]
  -t ACCESS_TOKEN       specify ACCESS_TOKEN directly, takes precedence over ACCESS_TOKEN_FILE
  -f ACCESS_TOKEN_FILE  specify file in working directory with ACCESS_TOKEN [default: .oAuth]
~~~~
