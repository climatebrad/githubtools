#!/usr/bin/env python
"""Usage:
  githubtools.py [(-v|--verbose) -n <max> --test --dir=<dir>]
  githubtools.py [(-t ACCESS_TOKEN|-f ACCESS_TOKEN_FILE)]
  githubtools.py (-h|--help)

Toolkit for manipulating local and Github repositories. Most functions take a config dict argument.

Options:
  -h --help             show this screen.
  -v --verbose          verbose mode
  -n <max>              specify <max> limit of matching repositories
  --test                test mode (no write)
  --dir=<dir>           specify <dir> to clone repositories [default: ./]
  -t ACCESS_TOKEN       specify ACCESS_TOKEN directly, takes precedence over ACCESS_TOKEN_FILE
  -f ACCESS_TOKEN_FILE  specify file in working directory with ACCESS_TOKEN [default: .oAuth]
"""
from docopt import docopt

# class Githubtool:
# 	def __init__(self,config):
#		""" create a new githubtool """
#		access_token=set_access_token(arguments)
#		self.g = Github(access_token)

if __name__ == '__main__':
	config = docopt(__doc__)
	if config['--test'] or config['--verbose']:
		print(config)

import sys
# get a list of the github repositories we need to fork
# https://python.gotrained.com/search-github-api/
# https://pygithub.readthedocs.io/en/latest/introduction.html
# https://developer.github.com/v3/search/#search-repositories

# library to the Github API
from github import Github

# for local git commands
import pygit2

# just so we can go from a Github URL to a Github owner/repo request
import giturlparse

# get token

import os.path
from os import path

def load_access_token(fname):
	f = open(fname,"r")
	token = f.read()
	return token.rstrip()

def set_access_token(config):
	token = None
	token_file = config['-f']

	if path.exists(token_file):
		token = load_access_token(token_file)

	# if -t flag set, takes precedence. Probably should validate.

	if config['-t']:
		token = config['-t']

	if not token:
		sys.exit([f"No {config['-f']} file found or -t=ACCESS_TOKEN specified."])
	return token


def _is_iterable(obj):
	try:
		iterator = iter(obj)
	except:
		return False
	else:
		return True

# this doesn't work well with a list for some reason
# e.g. I can't get dc,100719 to work
# but the single keyword "dc-ds-100719" works
# so we're using it only to take one keyword

def search_github_repos(g,keywords,config):
	if type(keywords) is not list: keywords = [ keywords ] # not the most pythonic but strings are iterable
	q = '+'.join(keywords)
	repos = g.search_repositories(query=q,sort='updated',order='desc')

	if config['--test'] or config['--verbose']:
		print(f'Found {repos.totalCount} repo(s)')
	if config['-n']: # I should be validating this argument
		n = int(config['-n'])
		if n < repos.totalCount:
			repos = list(repos[0:n-1])
			if config['--test'] or config['--verbose']:
				print(f'Limiting to first {n} repos.')

	if config['--verbose']:
		for repo in repos:
			print(repo.clone_url)

	if config['--test']:
		test_repo = repos[0]
		print("FIRST FOUND: "+test_repo.clone_url)

	return repos


# Fork them


# AuthenticatedUser.create_fork(repo)
# Calls:	POST /repos/:owner/:repo/forks
# Parameters:	repo – github.Repository.Repository
# Return type:	github.Repository.Repository

def my_forked_repos(g,me):
	my_forked_repos = []
	my_repos = me.get_repos()
	for repo in my_repos:
		if repo.fork:
			my_forked_repos.append(repo)

def fork_exists(g,me,repo,config):
	# get my repositories
	# for the ones which are forks
	# get the owner/repo info
	return False

# creates forks for repos given

def fork_repos(g,repos,config):
# make sure repos is iterable
	if not _is_iterable(repos): repos = [repos]
	me = g.get_user()
	forked_repos = []
	msg_prefix = 'TEST: ' if config['--test'] else ''
	for repo in repos:
		if config['--test'] or config['--verbose']:
			print(f"{msg_prefix}Forking {repo.clone_url}...")
		if not config['--test']: # it would be good to check if fork exists before doing this
			forked_repo = me.create_fork(repo)
			forked_repos.append(forked_repo)
		if config['--verbose']:
			print(f"Done.")
	return forked_repos

# need to add a check that forked repo doesn't already exist (?)

# clone them locally
# https://stackoverflow.com/questions/49458329/create-clone-and-push-to-github-repo-using-pygithub-and-pygit2

# repoClone = pygit2.clone_repository(repo.git_url, <dir>)

# creates clones for given remote repos; returns clones that already exist

# working_dir better not already be a git repository!!
def clone_repos(repos,config):
# make sure repos is iterable
	if not _is_iterable(repos): repos = [repos]
	cloned_repos = []
	working_dir = config['--dir']
	msg_prefix = 'TEST: ' if config['--test'] else ''
	for repo in repos:
		if config['--test'] or config['--verbose']:
			print(f"{msg_prefix}Cloning {repo.git_url} into {working_dir}/{repo.name} ...")
		if pygit2.discover_repository(working_dir):
			sys.exit(f"A repository already exists in {working_dir}")
		if pygit2.discover_repository(working_dir+"/"+repo.name):
			if config['--test'] or config['--verbose']:
				print(f"Repository {repo.name} already exists in {working_dir}")
			# note: should check if the local repo that exists is actually a clone of the repo, not just same name
			cloned_repo = pygit2.Repository(pygit2.discover_repository(working_dir+"/"+repo.name))
			if cloned_repo.remotes["origin"].url != repo.clone_url: # repair - this fails if remote not set
				cloned_repo.remotes.set_url("origin",repo.clone_url)
		elif not config['--test']:
			cloned_repo = pygit2.clone_repository(repo.git_url,working_dir+"/"+repo.name)
			cloned_repo.remotes.set_url("origin",repo.clone_url) # have to fix the remote url
		if not config['--test']:
			cloned_repos.append(cloned_repo)
		if config['--verbose']:
			print(f"Done.")
	return cloned_repos

# adding upstream remote
# maybe should be able to set name of upstream parent
def get_github_repo_from_url(g,url,config):
	p = giturlparse.parse(url)
	if config['--test']:
		print(f"Retrieving {p.owner}/{p.repo}")
	return g.get_repo(p.owner+"/"+p.repo)


def add_upstream_repos(g,cloned_repos,config):
# make sure cloned_repos is iterable
	if not _is_iterable(cloned_repos): cloned_repos = [cloned_repos]
	upstream_remotes = []
	msg_prefix = 'TEST: ' if config['--test'] else ''
	for cloned_repo in cloned_repos:
		if config['--test'] or config['--verbose']:
			print(f"Getting {cloned_repo.remotes['origin'].url}...")
		forked_repo = get_github_repo_from_url(g,cloned_repo.remotes["origin"].url,config)
		if not forked_repo.parent: # skip
			if config['--test'] or config['--verbose']:
				print(f"Repo {forked_repo.url} does not have an upstream parent.")
				continue

		if config['--test'] or config['--verbose']:
			print(f"{msg_prefix}Adding upstream remote {forked_repo.parent.git_url}...")
		if not config['--test']:
			try:
				remote_upstream = cloned_repo.remotes['upstream']
				if config['--test'] or config['--verbose']:
					print(f"Upstream remote {remote_upstream.url} already exists.")
				upstream_remotes.append(remote_upstream)
			except:
				upstream_remotes.append(cloned_repo.remotes.create("upstream",forked_repo.parent.git_url))
		if config['--verbose']:
			print(f"Done.")
	return upstream_remotes
