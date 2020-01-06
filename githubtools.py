#!/usr/bin/env python
"""Usage:
  githubtools.py [(-v|--verbose) -n <max> --test  --old]
  githubtools.py [--locals=<list> --dir=<dir>]
  githubtools.py [(-t ACCESS_TOKEN|-f ACCESS_TOKEN_FILE)]
  githubtools.py (-h|--help)

Toolkit for manipulating local and Github repositories. Most functions take a config dict argument.

Options:
  -h --help             show this screen.
  -v --verbose          verbose mode
  -n <max>              specify <max> limit of matching repositories
  --test                test mode (no write)
  --old                 add github repo to forked list even it was previously forked
  --locals=<list>       specify file name where names of local repos are listed [default: git_list]
  --dir=<dir>           specify <dir> to clone repositories [default: ..]
  -t ACCESS_TOKEN       specify ACCESS_TOKEN directly, takes precedence over ACCESS_TOKEN_FILE
  -f ACCESS_TOKEN_FILE  specify file in working directory with ACCESS_TOKEN [default: .oAuth]
"""
import sys
import os
from os import path

from docopt import docopt

# library to the Github API
from github import Github

# for local git commands
import pygit2

# just so we can go from a Github URL to a Github owner/repo request
import giturlparse


if __name__ == '__main__':
    CONFIG = docopt(__doc__)
    if CONFIG['--test'] or CONFIG['--verbose']:
        print(CONFIG)


# get a list of the github repositories we need to fork
# https://python.gotrained.com/search-github-api/
# https://pygithub.readthedocs.io/en/latest/introduction.html
# https://developer.github.com/v3/search/#search-repositories


# get token


class Githubtool:
    """Githubtool class"""
    def __init__(self,
                 is_verbose=False,
                 is_test=False,
                 locals_file='git_list',
                 clone_dir='..',
                 access_token_file='.oAuth',
                 access_token=None,
                 ):
        """ create a new githubtool """
        # configs
        self.config = {}
        self.config['-t'] = access_token
        self.config['--dir'] = clone_dir
        self.config['--locals'] = locals_file
        self.is_verbose = is_verbose
        self.is_test = is_test
        self.locals_file = locals_file
        self.clone_dir = clone_dir

        # initialize Github objects
        _access_token = self.set_access_token(access_token_file, access_token)
        self.g = Github(_access_token)

        self.local_repos_list = []
        self.repos = []
        self.forked_repos = []
        self.cloned_repos = []
        self.upstream_remotes = []




    @staticmethod
    def load_access_token(fname):
        """given a file name / path fname, return the string stored in it.
        does not check if it's actually an authentic auth token"""
        f = open(fname, "r")
        token = f.read()
        return token.rstrip()

    def set_access_token(self, access_token_file, access_token):
        """first looks to set auth token passed directly from config['-t']
        then looks for auth token stored in a file from config['-f']"""

        token = None

    # if -t flag set, takes precedence. Probably should validate.

        if access_token:
            token = access_token
        else:
            if path.exists(access_token_file):
                token = self.load_access_token(access_token_file)

        if not token:
            sys.exit([f"No {access_token_file} file found or -t=ACCESS_TOKEN specified."])
        return token

    @staticmethod
    def _is_iterable(obj):
        """private function to check whether obj is iterable"""
        try:
            iterator = iter(obj)
        except:
            return False
        else:
            return True

    def search_github_repos(self, keywords, user=None, max_match=None):
        """
        given keywords (either list or single string) and config hash, user can be specified as well"""

        if type(keywords) is not list: keywords = [keywords] # not the most pythonic but strings are iterable
        q = ' '.join(keywords) # the space gets converted to a +
        if user:
            q = f'{q} user:{user}'
        repos = self.g.search_repositories(query=q, sort='updated', order='desc')

        if self.is_test or self.is_verbose:
            print(f'Found {repos.totalCount} repo(s)')
        if max_match: # I should be validating this argument
            n = int(max_match)
            if n < repos.totalCount:
                repos = list(repos[0:n-1])
                if self.is_test or self.is_verbose:
                    print(f'Limiting to first {n} repos.')

        if self.is_verbose:
            for repo in repos:
                print(repo.clone_url)

        if self.is_test:
            test_repo = repos[0]
            print("FIRST FOUND: " + test_repo.clone_url)

        self.repos = repos
        return repos


    # Fork them



    def my_forked_repos(self):
        """Return list of forked repos for user associated with g"""
        me = self.g.get_user()
        my_repos = me.get_repos()
        self.forked_repos = [repo for repo in my_repos if repo.fork]
        return self.forked_repos

    def find_fork(self, repo):
        """For a given repo, check that github_user has a repo of the same name that is its fork.
    If fork exists, return the fork. Else return false.
    This is a moderately accurate check. The correct way is to load all the user's repos and check through the parents."""

        me = self.g.get_user()
        try:
            my_repo = self.g.get_repo(f"{me.login}/{repo.name}")
        except:
            return False
        else:
            if (my_repo.fork) and (my_repo.parent.full_name == repo.full_name):
                return my_repo
            else:
                return False

    # AuthenticatedUser.create_fork(repo)
    # Calls:    POST /repos/:owner/:repo/forks
    # Parameters:    repo – github.Repository.Repository
    # Return type:    github.Repository.Repository

    def fork_repos(self, repos, include_old=False):
        """For list of repos, fork into github_user's account"""
    # make sure repos is iterable
        if not self._is_iterable(repos): repos = [repos]
        me = self.g.get_user()
        forked_repos = []
        msg_prefix = 'TEST: ' if self.is_test else ''
        for repo in repos:
            if self.is_test or self.is_verbose:
                print(f"{msg_prefix}Forking {repo.clone_url}...")
            forked_repo = self.find_fork(repo)
            if forked_repo:
                if self.is_test or self.is_verbose:
                    print(f"{repo.clone_url} already forked.")
                if include_old:
                    forked_repos.append(forked_repo)
            else:
                if not self.is_test:
                    forked_repo = me.create_fork(repo)
                    forked_repos.append(forked_repo)
                if self.is_verbose:
                    print(f"Done.")
        self.forked_repos = forked_repos
        return forked_repos

    @staticmethod
    def dir_is_repo(gitdir):
        """Check if dir is a git repository."""
        return pygit2.discover_repository(gitdir)

    # clone them locally
    # https://stackoverflow.com/questions/49458329/create-clone-and-push-to-github-repo-using-pygithub-and-pygit2

    # repoClone = pygit2.clone_repository(repo.git_url, <dir>)

    # creates clones for given remote repos; returns clones that already exist

    # working_dir better not already be a git repository!!

    def _load_local_repos_list(self):
        """Load list of local repos (name only). Default location is git_list"""
        locals_file = open(self.locals_file, "w")
        for root, dirs, files in os.walk(self.clone_dir): # for every dir under starting directory
            if self.dir_is_repo(root):
                locals_file.write(root.split(path.sep)[-1] + "\n")
                dirs[:] = [] # don't descend into repo
        locals_file.close()
        self.local_repos_list = [repo.rstrip('\n') for repo in open(config['--locals'])]

    def local_repo_exists(self, repo_name):
        """Return true if repo_name is found in local repos list"""
        if not self.local_repos_list:
            self._load_local_repos_list()
        return repo_name in self.local_repos_list

    def clone_repos(self, repos):
        """For list of repos, clone into local directory set by config['--dir']"""
    # make sure repos is iterable
        if not self._is_iterable(repos): repos = [repos]
        cloned_repos = []
        working_dir = self.config['--dir']
        msg_prefix = 'TEST: ' if self.is_test else ''
        for repo in repos:
            clone_path = working_dir + "/" + repo.name
            if self.is_test or self.is_verbose:
                print(f"{msg_prefix}Cloning {repo.git_url} into {clone_path} ...")
            if self.dir_is_repo(working_dir):
                sys.exit(f"A repository already exists in {working_dir}")

    # check if the working dir includes the repo somewhere

            if self.local_repo_exists(repo.name):
                if self.is_test or self.is_verbose:
                    print(f"Repository {repo.name} already cloned somewhere in {working_dir}")
                continue
            if self.dir_is_repo(clone_path):
                if self.is_test or self.is_verbose:
                    print(f"Repository {repo.name} already exists in {working_dir}")
                cloned_repo = pygit2.Repository(pygit2.discover_repository(clone_path))
                # if the repo's origin remote doesn't exist or is set to the git_url, fix it to the clone_url
                if ("origin" not in cloned_repo.remotes) or (cloned_repo.remotes["origin"].url == repo.git_url):
                    cloned_repo.remotes.set_url("origin", repo.clone_url)
            elif not self.is_test:
                cloned_repo = pygit2.clone_repository(repo.git_url, clone_path)
                cloned_repo.remotes.set_url("origin", repo.clone_url) # have to fix the remote url

            if not self.is_test:
                cloned_repos.append(cloned_repo)
            if self.is_verbose:
                print(f"Done.")
        self.cloned_repos = cloned_repos
        return cloned_repos

    # adding upstream remote
    # maybe should be able to set name of upstream parent
    def get_github_repo_from_url(self, url):
        """given url of a github repo, return the repo"""
        p = giturlparse.parse(url)
        if self.is_test:
            print(f"Retrieving {p.owner}/{p.repo}")
        return self.g.get_repo(p.owner+"/"+p.repo)

    def add_upstream_repos(self, cloned_repos):
        """set upstream remotes for local copies of cloned_repos"""
    # make sure cloned_repos is iterable
        if not self._is_iterable(cloned_repos): cloned_repos = [cloned_repos]
        upstream_remotes = []
        msg_prefix = 'TEST: ' if self.is_test else ''
        for cloned_repo in cloned_repos:
            if self.is_test or self.is_verbose:
                print(f"Getting {cloned_repo.remotes['origin'].url}...")
            forked_repo = self.get_github_repo_from_url(cloned_repo.remotes["origin"].url)
            if not forked_repo.parent: # skip
                if self.is_test or self.is_verbose:
                    print(f"Repo {forked_repo.url} does not have an upstream parent.")
                    continue

            if self.is_test or self.is_verbose:
                print(f"{msg_prefix}Adding upstream remote {forked_repo.parent.git_url}...")
            if not self.is_test:
                try:
                    remote_upstream = cloned_repo.remotes['upstream']
                    if self.is_test or self.is_verbose:
                        print(f"Upstream remote {remote_upstream.url} already exists.")
                    upstream_remotes.append(remote_upstream)
                except:
                    upstream_remotes.append(cloned_repo.remotes.create("upstream", forked_repo.parent.git_url))
            if self.is_verbose:
                print(f"Done.")
        self.upstream_remotes = upstream_remotes
        return upstream_remotes
