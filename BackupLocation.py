#!/usr/bin/env python3

import logging, shutil
from pathlib import Path

class BackupLocation:
	"""
	Represents a backup location entry. It is a list of orig_path and back_path pairs. Has functions to
	convert it to and from json for easy reading of config file. Also has method to backup and restore the
	location. Folders are moved under git repo and a symlink is added to it from the original location. Files
	are hard linked under git repo
	"""

	def __init__(self, orig_path: Path, back_path: Path):
		self.orig_path = orig_path
		self.back_path = back_path
		self.log = logging.getLogger(f'backup.location.{self.orig_path.name}')

	def backup(self):
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
				else:
					self.log.info(f'{self.orig_path} already synced to {self.back_path}')
			else:
				self.log.info(f'Backing up {self.orig_path}. Moving it to {self.back_path} and replacing it with a symbolic link')
				shutil.move(self.orig_path, self.back_path)
				self.orig_path.symlink_to(self.back_path)
		else:
			self.log.debug(f'Backup path is file')
			if self.back_path.exists():
				self.log.debug(f'Destination exists')
				if not self.orig_path.samefile(self.back_path):
					self.log.error(f'{self.back_path} exists. But {self.orig_path} is not same as {self.back_path}')
				else:
					self.log.info(f'{self.orig_path} already synced to {self.back_path}')
			else:
				self.log.info(f'Creating hard link {self.back_path} to {self.orig_path}')
				self.orig_path.link_to(self.back_path)

	def restore(self):
		if not self.back_path.exists():
			self.log.error(f'Path {self.back_path} doesnot exist')
			return

		if self.back_path.is_dir():
			self.log.debug(f'Restore path is dir')
			if self.orig_path.exists():
				self.log.debug(f'Destination exists')
				if not self.orig_path.is_symlink() or self.orig_path.readlink() != self.back_path:
					self.log.error(f'{self.orig_path} exists and is not symlinked to {self.back_path}')
				else:
					self.log.info(f'{self.orig_path} is present and is synced to {self.back_path}')
			else:
				self.log.info(f'Restoring {self.orig_path}. Symlinking to {self.back_path}')
				self.orig_path.symlink_to(self.dest_path)
		else:
			self.log.debug(f'Restore path is file')
			if self.orig_path.exists():
				self.log.debug(f'Destination exists')
				if not self.back_path.samefile(self.orig_path):
					self.log.error(f'{self.orig_path} exists and is not same as {self.back_path}')
				else:
					self.log.info(f'{self.orig_path} already restored from {self.back_path}')
			else:
				self.log.info(f'Restoring {self.orig_path} from {self.back_path}')
				self.orig_path.link_to(self.back_path)

	#def __repr__(self):
        #    return json.dumps({'orig_path': self.orig_path.resolve(), 'back_path': se.back_path.resolve()})

	@classmethod
	def from_json(cls, obj):
		if 'src' in obj and 'backup' in obj:
			return cls(Path(obj['src']), Path(obj['backup']))
		else:
			return None

	def to_json(self):
		return {'src': str(self.orig_path), 'backup': str(self.back_path.resolve())}


