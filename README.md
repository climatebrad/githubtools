# flatiron-github-fork
Automate the process of forking and cloning Flatiron Data Science repos to your personal directory.


## Usage:
~~~~
  forker.py [(-v|--verbose) -n <max> --test  --fork --clone --dir=<dir> --upstream] KEYWORD
  forker.py [(-t ACCESS_TOKEN|-f ACCESS_TOKEN_FILE)] KEYWORD
  forker.py (-h|--help)
~~~~

Search for Github repositories matching KEYWORD using Github oAuth specified by ACCESS_TOKEN
or in ACCESS_TOKEN_FILE; optionally fork to the user's Github directory, clone locally, and
add upstream remote.

### Arguments:
KEYWORD
: keyword to search Github repositories for

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
