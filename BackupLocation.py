#!/usr/bin/env python3

import logging, shutil, json
from pathlib import Path
from Globals import *

class BackupLocation:

	backup_dir = str(BACKUP_DIR)
	BACKUP_LOCATION = 'BACKUP_LOCATION'

	"""
	Represents a backup location entry. It is a list of orig_path and back_path pairs. Has functions to
	convert it to and from json for easy reading of config file. Also has method to backup, restore and revert the
	location. Folders are moved under git repo and a symlink is added to it from the original location. Files
	are hard linked under git repo
	"""

	def __init__(self, orig_path: Path, back_path: Path):
		self.orig_path = orig_path
		self.back_path = back_path
		self.log = logging.getLogger(f'backup.location.{self.orig_path.name}')

	def backup(self):
		"""
		Backs up the orig_path location
		"""
		if not self.orig_path.exists():
			self.log.error(f'Path {self.orig_path} doesnot exist')
			return

		if self.orig_path.is_dir():
			self.log.debug(f'Backup path is dir')
			if self.back_path.exists():
				self.log.debug(f'Destination exists')
				if not self.orig_path.is_symlink() or self.orig_path.readlink() != self.back_path:
					self.log.error(f'{self.back_path} exists. But {self.orig_path} is not a symlink or \
						symlink does not point to {self.back_path}')
					eprint(f'{self.back_path} exists and it not {self.orig_path} symlink')
					
				else:
					self.log.info(f'{self.orig_path} already synced to {self.back_path}')
					print('Already synced')
			else:
				self.log.info(f'Backing up {self.orig_path}. Moving it to {self.back_path} and replacing it with a symbolic link')
				shutil.move(self.orig_path, self.back_path)
				self.orig_path.symlink_to(self.back_path)
				print(f'Backed up {self.orig_path}')
		else:
			self.log.debug(f'Backup path is file')
			if self.back_path.exists():
				self.log.debug(f'Destination exists')
				if not self.orig_path.samefile(self.back_path):
					self.log.error(f'{self.back_path} exists. But {self.orig_path} is not same as {self.back_path}')
					eprint(f'{self.back_path} exists and it not {self.orig_path} symlink')
				else:
					self.log.info(f'{self.orig_path} already synced to {self.back_path}')
					print('Already synced')
			else:
				self.log.info(f'Creating hard link {self.back_path} to {self.orig_path}')
				self.orig_path.link_to(self.back_path)
				print(f'Backed up {self.orig_path}')

	def restore(self):
		"""
		Restores orig_path from back_path
		"""
		if not self.back_path.exists():
			self.log.error(f'Path {self.back_path} doesnot exist')
			return

		if self.back_path.is_dir():
			self.log.debug(f'Restore path is dir')
			if self.orig_path.exists():
				self.log.debug(f'Destination exists')
				if not self.orig_path.is_symlink() or self.orig_path.readlink() != self.back_path:
					self.log.error(f'{self.orig_path} exists and is not symlinked to {self.back_path}')
					eprint(f'{self.orig_path} exists and it not linked of {self.back_path}')
				else:
					self.log.info(f'{self.orig_path} is present and is synced to {self.back_path}')
					print('Already restored')
			else:
				self.log.info(f'Restoring {self.orig_path}. Symlinking to {self.back_path}')
				self.orig_path.symlink_to(self.back_path)
				print(f'Restored {self.orig_path}')
		else:
			self.log.debug(f'Restore path is file')
			if self.orig_path.exists():
				self.log.debug(f'Destination exists')
				if not self.back_path.samefile(self.orig_path):
					self.log.error(f'{self.orig_path} exists and is not same as {self.back_path}')
					eprint(f'{self.orig_path} exists and it not {self.back_path} symlink')
				else:
					self.log.info(f'{self.orig_path} already restored from {self.back_path}')
					print('Already restored')
			else:
				self.log.info(f'Restoring {self.orig_path} from {self.back_path}')
				self.back_path.link_to(self.orig_path)
				print(f'Restored {self.orig_path}')

	def revert(self):
		"""
		Revert changes
		"""
		if not self.back_path.exists():
			self.log.error(f'Path {self.back_path} doesnot exist')
			return

		if self.back_path.is_dir():
			self.log.debug(f'Revert path is dir')
			if self.orig_path.exists():
				self.log.debug(f'Destination exists')
				if not self.orig_path.is_symlink() or self.orig_path.readlink() != self.back_path:
					self.log.error(f'{self.orig_path} exists and is not symlinked to {self.back_path}')
					eprint(f'{self.orig_path} exists and it not {self.back_path} symlink')
				else:
					self.log.info(f'{self.orig_path} link will be removed and will be replaced with {self.back_path}')
					self.orig_path.unlink()
					shutil.move(self.back_path, self.orig_path)
					print(f'Reverted {self.orig_path}')
			else:
				self.log.warn(f'{self.orig_path} is not present')
				self.log.info(f'{self.back_path} will be moved to {self.orig_path}')
				shutil.move(self.back_path, self.orig_path)
				print(f'Reverted {self.orig_path}')
		else:
			self.log.debug(f'Revert path is file')
			if self.orig_path.exists():
				self.log.debug(f'Destination exists')
				if not self.back_path.samefile(self.orig_path):
					self.log.error(f'{self.orig_path} exists and is not same as {self.back_path}')
					eprint(f'{self.orig_path} exists and it not {self.back_path} symlink')
				else:
					self.log.info(f'Removing {self.back_path}')
					self.back_path.unlink()
					print(f'Reverted {self.orig_path}')
			else:
				self.log.warn(f'{self.orig_path} is not present')
				self.log.info(f'Moving {self.back_path} to {self.orig_path}')
				shutil.move(self.back_path, self.orig_path)
				print(f'Reverted {self.orig_path}')

	def __repr__(self):
		return json.dumps(self.to_json())
	
	@classmethod
	def from_json(cls, obj):
		if 'src' in obj and 'backup' in obj:
			return cls(Path(obj['src']), Path(obj['backup'].replace(BackupLocation.BACKUP_LOCATION, BackupLocation.backup_dir)))
		else:
			return None

	def to_json(self):
		return {'src': str(self.orig_path), 'backup': str(self.back_path.resolve()).replace(BackupLocation.backup_dir, BackupLocation.BACKUP_LOCATION)}
