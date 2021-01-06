#!/usr/bin/env python3

import subprocess, logging, os
from datetime import datetime
from enum import Enum
from Globals import PROJECT_DIR, WORKING_DIR

class GitStatus(Enum):
	UNTRACKED = 0
	UNSTAGED = 1
	UNCOMMITED = 2
	UNSYNCED = 3
	SYNCED = 4
	BEHIND = 5
	DIVERGED = 6

	def __repr__(self):
		if self == UNTRACKED:
			return 'Untracked'
		elif self == UNSTAGED:
			return 'Unstaged'
		elif self == UNCOMMITED:
			return 'Uncommited'
		elif self == UNSYNCED:
			return 'Unsynced'
		elif self == SYNCED:
			return 'Synced'
		elif self == BEHIND:
			return 'Behind'
		elif self == DIVERGED:
			return 'Diverged'

class Git:
	"""
	Helper class to interact with git
	"""

	def __init__(self):
		self.log = logging.getLogger('backup.git')

	def __run_git(self, args, stdout, stderr):
		# Change working directory to project folder, run the git command, and recert the working directory
		os.chdir(PROJECT_DIR)

		p = subprocess.run(['git', *args], stdout=stdout, stderr=stderr, check=True)

		os.chdir(WORKING_DIR)
		return p

	def status(self, stdout=None, stderr=None):
		self.log.debug('git status')
		return self.__run_git(['status'], stdout, stderr)

	def project_status(self):
		p = self.status(subprocess.PIPE, subprocess.PIPE)
		git_status = p.stdout.decode('utf-8')

		if 'Untracked files' in git_status:
			return GitStatus.UNTRACKED
		elif 'Changes not staged for commit' in git_status:
			return GitStatus.UNSTAGED
		elif 'Changes to be committed' in git_status:
			return GitStatus.UNCOMMITED
		else:
			local_commit = self.__run_git(['rev-parse', '@'], subprocess.PIPE, subprocess.PIPE).stdout.decode('utf-8')
			remote_commit = self.__run_git(['rev-parse', '@{u}'], subprocess.PIPE, subprocess.PIPE).stdout.decode('utf-8')
			base_commit = self.__run_git(['merge-base', '@', '@{u}'], subprocess.PIPE, subprocess.PIPE).stdout.decode('utf-8')
			
			if local_commit == remote_commit:
				return GitStatus.SYNCED
			elif local_commit == base_commit:
				return GitStatus.BEHIND
			elif remote_commit == base_commit:
				return GitStatus.UNSYNCED
			else:
				return GitStatus.DIVERGED

	def add(self, stdout=None, stderr=None):
		self.log.debug('git add')
		p = self.__run_git(['add', '-A'], stdout, stderr)
		print('Added to git')
		return p

	
	def commit(self, msg=None, stdout=None, stderr=None):
		self.log.debug('git commit')
		m = msg if msg else f'Autocommit at {datetime.now().replace(microsecond=0).isoformat()}'
		p = self.__run_git(['commit', '-m', m], stdout, stderr)
		print(f'Commited to git with msg "{m}"')
		return p
	
	def push(self, stdout=None, stderr=None):
		self.log.debug('git push')
		p = self.__run_git(['push', 'origin', 'master'], stdout, stderr)
		print('Pushed to git')
		return p
