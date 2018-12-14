import unittest
import tempfile
import os
from archive_manager import ArchiveManager, ArchiveManagerException
from module import get_config
from fallocate import fallocate
import shutil
import subprocess
import time

class ArchiveManagerTestCase(unittest.TestCase):
    """Tests for cloud archive manager"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(dir="/var/tmp")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def is_immutable(self, fname):
        p = subprocess.Popen(['lsattr', fname], bufsize=1, stdout=subprocess.PIPE)
        data, _ = p.communicate()
        return 'i' in data

    def generic_archive(self, backup_extension=".tar.gz"):
        """create a generic archive"""
        self.create_test_files(backup_extension)
        filename = self.create_test_config()
        cfg = get_config(filename)
        cfg['backup_root'] = self.test_dir
        cfg['backup_extension'] = backup_extension
        verbose = None
        archive = ArchiveManager(cfg, verbose)
        return archive

    def test_custom_backup_extention(self):
        backup_extension = ".tgz"
        archive = self.generic_archive(backup_extension)
        self.assertEqual(archive.backup_extension, backup_extension)
        for d in archive.backup_dirs:
            files = archive.get_files(d)
            self.assertEqual(len(files), 100)
            last_file = "99-test%s" % backup_extension
            first_file = "0-test%s" % backup_extension
            self.assertEqual(files[-1], last_file)
            self.assertEqual(files[0], first_file)   

    def test_newest_oldest(self):
        """Ensure the first file is the oldest and the last file is the newest"""
        archive = self.generic_archive()

        for dir in archive.backup_dirs: 
            files = archive.get_files(dir)
            oldest_file = files[-1]
            filepath = os.path.join(archive.backup_root, dir, oldest_file)
            oldest_file_mtime = os.stat(filepath).st_mtime

            newest_file = files[0]
            filepath = os.path.join(archive.backup_root, dir, newest_file)
            newest_file_mtime = os.stat(filepath).st_mtime

            self.assertGreater(newest_file_mtime, oldest_file_mtime)

    def test_delete_read_only_file(self):
        """Make one of the files immutable and test if delete will fail"""
        self.create_test_files()
        filename = self.create_test_config()
        cfg = get_config(filename)
        cfg['backup_root'] = self.test_dir
        # 3mb, create_test_files should create 5mb of files
        cfg['max_dir_size'] = 3145728 
        verbose = None
        archive = ArchiveManager(cfg, verbose)
        # Just use one directory this time
        dir = archive.backup_dirs[0]

        # Set this file read only
        filepath = os.path.join(archive.backup_root, dir, "99-test.tar.gz")
        # TODO: May be better to simply delete the file than to run sudo chattr...
        os.system("sudo chattr +i " + filepath)
        assert self.is_immutable(filepath) is True

        try:
            archive.delete_until_size_or_min(dir)
        except:
            pass

        # Now make it mutable again
        os.system("sudo chattr -i " + filepath)
        assert self.is_immutable(filepath) is False

        try:
            archive.delete_until_size_or_min(dir)
        except:
            self.fail("Failed to delete file unexpectedly")

        files = archive.get_files(dir)
        # To get to 3mb of files we'll need to delete down to 77 files
        self.assertEqual(len(files), 77)
        self.assertEqual(files[-1], '76-test.tar.gz')
        self.assertEqual(files[0], '0-test.tar.gz')

    def test_bad_file_names(self):
        """Put non tar.gz files into the directory"""
        archive = self.generic_archive()

        # FIXME: a better way to create these kind of files?
        bad_filename = "shouldntexist"
        file_extension = []
        file_extension.append('.tar.gz')
        file_extension.append('.tgz')
        file_extension.append('.zip')
        file_extension.append('.txt')
        file_extension.append('.rar')
        file_extension.append('.rpm')

        # If the custom backup extension is in the list, remove it
        try:
            file_extension.remove(archive.backup_extension)
        except:
           pass

        for dir in archive.backup_dirs:  
            # Create bad files
            for f in file_extension:
                bf = "%s%s" % (bad_filename, f)
                filepath = os.path.join(archive.backup_root, dir, bf)
                with open(filepath, "w+") as f:
                    size = 1024
                    with open(filepath, "w+b") as f:
                        fallocate(f, 0, size)
                    f.close() 
            
            files = archive.get_files(dir)
            self.assertEqual(len(files), 100)

            # Bad files should not be included in the files list
            for f in file_extension:
                bf = "%s%s" % (bad_filename, f) 
                self.assertNotIn(bf, files)

    def test_delete_oldest(self):
        archive = self.generic_archive()

        for dir in archive.backup_dirs:   
            files = archive.get_files(dir)
            try:
                archive.delete_oldest(dir, files)
            except:
                self.fail("delete oldest failed")
    
            self.assertEqual(len(files), 99)
            self.assertEqual(files[-1], "98-test.tar.gz")

            # Try listing the files again and deleting another file
            files = archive.get_files(dir)
            try:       
                archive.delete_oldest(dir, files)
            except:
                self.fail("delete oldest failed")
    
            self.assertEqual(len(files), 98)
            self.assertEqual(files[-1], "97-test.tar.gz")

    def test_get_files(self):
        archive = self.generic_archive()

        for dir in archive.backup_dirs:
            files = archive.get_files(dir)
            oldest_file = files[-1]
            newest_file = files[0]
            self.assertEqual(len(files), 100)
            self.assertEqual(oldest_file, "99-test.tar.gz")
            self.assertEqual(newest_file, "0-test.tar.gz")

    def test_get_size(self):
        archive = self.generic_archive()

        for dir in archive.backup_dirs:
            size = archive.get_size(dir)  
            self.assertEqual(size, 5171200)

    def test_keep_max_files(self):
        archive = self.generic_archive()

        for dir in archive.backup_dirs:
            try:
                archive.keep_max_files(dir)
            except:
                self.fail("should not fail")

            files = archive.get_files(dir)
            self.assertEqual(len(files), 36)

    def test_delete_until_max_dir_size(self):
        """Delete until we have a minimum amount of files, which takes precedence over size"""
        self.create_test_files()
        filename = self.create_test_config()
        cfg = get_config(filename)
        cfg['max_dir_size'] =  3145728
        cfg['backup_root'] = self.test_dir
        verbose = None
        archive = ArchiveManager(cfg, verbose)

        for dir in archive.backup_dirs:
            try:
                archive.delete_until_size_or_min(dir)
            except ArchiveManagerException, err:
                self.fail("ERROR: %s\n" % str(err))

            # I guess do this here, as the actual files is in the function
            # FIXME: this suggests this is not the right way to do it
            files = archive.get_files(dir)           
            self.assertEqual(len(files), 77)
            self.assertEqual(files[-1], '76-test.tar.gz')
            self.assertEqual(files[0], '0-test.tar.gz')

    def test_min_larger_than_max(self):
        self.create_test_files()
        filename = self.create_test_config()
        cfg = get_config(filename)
        cfg['max_dir_size'] =  3145728
        cfg['backup_root'] = self.test_dir        
        # Max should be larger than min, here we set it to be smaller
        cfg['max_num_backup_files'] = 80
        cfg['min_num_backup_files'] = 90

        # Should fail
        with self.assertRaises(ArchiveManagerException):
            verbose = None
            unused_archive = ArchiveManager(cfg, verbose)
        
        # Now set min/max properly
        cfg['max_num_backup_files'] = 90
        cfg['min_num_backup_files'] = 80

        try:
            verbose = None
            unused_archive = ArchiveManager(cfg, verbose)
        except ArchiveManagerException, err:
            self.fail("ERROR: %s\n" % str(err))

    def create_test_config(self):
        filename = os.path.join(self.test_dir, "config.ini")
        try:
            fh = open(filename, "w+")
            # NOTE: no backup_root setting, everything but
            config_string = ("---\n"
                            "max_num_backup_files: 36\n"
                            "min_num_backup_files: 24\n"
                            "max_dir_size: 5000000000\n"
                            "backup_root: '/backup'\n"
                            "backup_dirs:\n"
                            "  - 'backups-1'\n"
                            "  - 'backups-2'\n")
            fh.write(config_string)
            fh.close()
        except:
            # TODO: handle error
            pass
        return filename

    def create_test_files(self, backup_extension=".tar.gz"):
        filename = self.create_test_config()
        cfg = get_config(filename)
        cfg['backup_root'] = self.test_dir

        for dir in cfg['backup_dirs']:
            full_dir = os.path.join(cfg['backup_root'], dir)
            if not os.path.exists(full_dir):
                os.makedirs(full_dir)
            for i in range(100):
                filename = str(i) + "-test%s" % backup_extension
                filepath = os.path.join(full_dir, filename)

                # Note the use of fallocate here to create files quickly that have a
                # given size.
                with open(filepath, "w+") as f:
                    size = (i+1)*1024
                    with open(filepath, "w+b") as f:
                        fallocate(f, 0, size)
                    f.close()

                # Here we are setting the mtime so that cloud archive manager
                # has some newer and older files to use, as far as its concerned
                stat = os.stat(filepath)
                mtime = stat.st_mtime
                atime = stat.st_atime

                # Make each file one hour older...though this will make file 99
                # the oldest file which is a bit counter intuitive...
                new_mtime = mtime - i*3600
                os.utime(filepath,(atime, new_mtime))

    def test_read_bad_config(self):
        filename = self.create_test_config()
        cfg = get_config(filename)
        # Remove backup_root to test failing archive creation
        del cfg['backup_root']

        with self.assertRaises(ArchiveManagerException):
            verbose = None
            unused_archive = ArchiveManager(cfg, verbose)
 
    def test_read_good_config(self):
        self.create_test_files()
        filename = self.create_test_config()
        cfg = get_config(filename)
        cfg['backup_root'] = self.test_dir  

        verbose = None
        try:
            archive = ArchiveManager(cfg, verbose)
        except ArchiveManagerException, err:
            self.fail("ERROR: %s\n" % str(err))

        backup_dirs_test = []
        backup_dirs_test.append("backups-1")
        backup_dirs_test.append("backups-2")

        self.assertEqual(archive.backup_root, self.test_dir)
        self.assertEqual(archive.max_num_backup_files, 36)
        self.assertEqual(archive.min_num_backup_files, 24)
        self.assertEqual(archive.max_dir_size, 5000000000)
        self.assertEqual(archive.backup_dirs, backup_dirs_test)
        self.assertEqual(archive.backup_dirs[0], 'backups-1')
        self.assertEqual(archive.backup_dirs[1], 'backups-2')

if __name__ == '__main__':
    unittest.main()