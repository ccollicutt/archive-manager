#!/usr/bin/env python

import logging
import sys
import os
from stat import S_ISREG, ST_MODE, ST_MTIME

BACKUP_EXTENSION = ".tar.gz"

log = logging.getLogger()
log.setLevel(logging.INFO)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('INFO: %(message)s'))
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)

class ArchiveManagerException(Exception):
    pass

class ArchiveManager(object):
    
    def __init__(self, cfg, verbose):

        # Required variables
        try:
            self.backup_root = cfg['backup_root']
            self.backup_dirs = cfg['backup_dirs']
            self.max_num_backup_files = cfg['max_num_backup_files']
            self.min_num_backup_files = cfg['min_num_backup_files']
            self.max_dir_size = cfg['max_dir_size']
            self.verbose = verbose
        except:
            raise ArchiveManagerException('could not load required config variables')

        # Optional variables
        try:
            self.backup_extension = cfg['backup_extension']
        except:
            self.backup_extension = BACKUP_EXTENSION

        if self.min_num_backup_files > self.max_num_backup_files:
            raise ArchiveManagerException('min backup files larger than max')
        
        if not os.path.isdir(self.backup_root):
            msg = "backup_root %s is not a directory" % self.backup_root
            raise ArchiveManagerException(msg)
        
        for d in self.backup_dirs:
            path = os.path.join(self.backup_root, d)
            if not os.path.isdir(path):
                msg = "backup_dir %s is not a directory" % d
                raise ArchiveManagerException(msg)

    def delete_oldest(self, directory, dirfiles):
        """Delete the oldest file"""
        dir_path = os.path.join(self.backup_root, directory)
        file_to_delete = dirfiles.pop()
        full_path = os.path.join(dir_path, file_to_delete)

        if  full_path.startswith(dir_path) and full_path.endswith(BACKUP_EXTENSION) and len(dir_path) > 1:
            if self.verbose:
                msg = "Deleting file %s" % full_path
                logging.info(msg)
                
            try:
                os.remove(full_path)
            except:
                msg = "Failed to delete file %s" % full_path
                raise ArchiveManagerException(msg)       
        else:
            raise ArchiveManagerException("file has incorrect path or extension")

    def get_size(self, directory):
        """Return the total size of set of files in a directory in bytes"""
        dir_path = os.path.join(self.backup_root, directory)
        total_size = 0
        for dirpath, unused_dirnames, filenames in os.walk(dir_path):
            for fname in filenames:
                file_path = os.path.join(dirpath, fname)
                total_size += os.path.getsize(file_path)
        return total_size

    def get_files(self, directory):
        """get all the files in a directory that match a particular extension"""
        dirpath = os.path.join(self.backup_root, directory)

        if not os.path.isdir(dirpath):
            raise ArchiveManagerException("path %s is not a directory", dirpath)

        # Get all entries in the directory w/ stats
        entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
        entries = ((os.stat(path), path) for path in entries)

        # Leave only regular files, insert creation date
        entries = ((stat[ST_MTIME], path) for stat, path in entries if S_ISREG(stat[ST_MODE]))
        # NOTE: On Windows `ST_CTIME` is a creation date but on Unix it could be something else
        # NOTE: Use `ST_MTIME` to sort by a modification date

        all_files = []
        for unused_cdate, path in sorted(entries):
            # Only add it if it ends with BACKUP_EXTENSION
            if path.endswith(self.backup_extension):
                all_files.append(os.path.basename(path))

        # Make oldest files first on the array
        all_files.reverse()

        return all_files

    def delete_until_size_or_min(self, directory):
        """Delete files until the size is less than the max size or minimum files achieved"""
        dir_path = os.path.join(self.backup_root, directory)
        dir_size = self.get_size(dir_path)
        files = self.get_files(dir_path)
        while dir_size > self.max_dir_size and len(files) > self.min_num_backup_files:
            try:
                self.delete_oldest(dir_path, files)
            except ArchiveManagerException as e:
                raise e
            dir_size = self.get_size(dir_path)
        
        if dir_size > self.max_dir_size:
            logging.info("min number of files achieved, but dir size is larger than max size")

    def keep_max_files(self, directory):
        """Delete files until we have the max number of files"""
        dir_path = os.path.join(self.backup_root, directory)
        files = self.get_files(dir_path)   

        while len(files) > self.max_num_backup_files:
            try:
                self.delete_oldest(dir_path, files)
            except ArchiveManagerException as e:
                raise e