#!/usr/bin/env python
#-*- coding: utf-8 -*-
               # encode/decode w/ utf-8: full-range of unicode chars, w/o addressing endian issues
import errno   # makes available errno system calls
import stat    # constants/functions for interpreting results of os.stat()
import os      # needed for os interfaces
import sys     # provides access to variables used/maintained by interpreter (inc. argv)
import time    # gives time functions
import fuse    # include fuse calls from python-fuse

fuse.fuse_python_api = (0, 2)   # application programming interface (0, 2)

class MyFuse(fuse.Fuse):
    randomFilename = "grandom"      # variable to hold the filename for random number access
    cpmFilename = "gcpm"            # variable to hold the filename for CPM access

    # Initializes the filesystem
    def __init__(self, *args, **kw):    # OOP constructor
        for all_args in sys.argv:       # print for debugging
            print " *** " + all_args    # print all arguments in sequence

        # require standardized call with root directory and mount_point
        if (len(sys.argv) < 3) or (sys.argv[-2][0] == '-') or (sys.argv[-1][0] == '-'):
            print "Error, proper input:"
            print "      MyFuse [-options] root_dir mount_point"
            print "or interpreting script:"
            print "      python MyFuse.py [-options] root_dir mount_point"
            sys.exit(0)

        # check to see if the root dir and mount point are valid
        must_exit = False
        if os.path.isdir(sys.argv[-2]) is False:
            print "Error: '" + sys.argv[-2] + "' is not a directory."
            must_exit = True
        if os.path.isdir(sys.argv[-1]) is False:
            print "Error: '" + sys.argv[-1] + "' is not a directory."
            must_exit = True
        if sys.argv[-2] == sys.argv[-1]:
            print "Error: root_dir and mount_point cannot be the same."
            must_exit = True
        if must_exit is True:
            sys.exit(0)

        self.root_dir = sys.argv[-2]
        print ":--- " + self.root_dir + " ---:" # prints second to last argument/root_dir"
        self.open_files = {}                    # initialize open_files to empty
        fuse.Fuse.__init__(self, *args, **kw)   # creates fuse Object

        # Initialize dummy stat structure for the two special files.
        dummy_touch = "/dummytouch"
        with open(sys.argv[-1] + dummy_touch, 'a'):
            current_mode = stat.S_IMODE(os.lstat(sys.argv[-1] + dummy_touch).st_mode)
            os.chmod(sys.argv[-1] + dummy_touch, current_mode & \
              ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
            self.file_stat = os.lstat(sys.argv[-1] + dummy_touch)
        os.remove(sys.argv[-1] + dummy_touch)

  # ==================== Filesystem Methods ====================

    # Change permissions for object to new permissions
    def chmod(self, path, mode):             # defines chmod to alter permissions
        print "*** CHMOD: ", path            # print information used for debugging
        if path == "/" + self.randomFilename or path == "/" + self.cpmFilename:
            to_return = -errno.EPERM
        else:
            os.chmod(self.root_dir + path, mode)  # syscall updating permissions mode
            to_return = 0
        return to_return

    # Obtains file attributes - method fills in the elements of the "stat" structure.
    def getattr(self, path):            # defines getattr to fetch attribute from file
        print "GETATTR-path: ", path    # print information used for debugging
        if path == "/" + self.randomFilename or path == "/" + self.cpmFilename:
            to_return = self.file_stat
        else:
            to_return = os.lstat(self.root_dir + path)
        return to_return                # return object with syscall updating status attributes

    # Lists directory entries (dirent) back to a caller
    def readdir(self, path, offset):                # defines readdir which lists files/folders
        print "\n\n*** READDIR: ", path             # print information used for debugging
        print "=====  " + self.root_dir + "  =====" # print information used for debugging
        for folders in '.', '..':
            yield fuse.Direntry(folders)
        for files in os.listdir(self.root_dir + path):      # list all file basenames in path
            yield fuse.Direntry(os.path.basename(files))    # yield fuse.Direntry(os.path.basename(x))
        for files in self.randomFilename, self.cpmFilename:
            yield fuse.Direntry(files)
        return

    # Removes empty directory of specified name
    def rmdir(self, path):         # defines rmdir to remove directories
        print "*** RMDIR: ", path  # print information used for debugging
        os.rmdir(self.path)        # syscall to remove directory path
        return 0

    # Creates a new directory of specified name
    def mkdir(self, path, mode):   # defines mkdir to create new directories
        print "*** MKDIR: ", path  # print information used for debugging
        os.mkdir(path)             # syscall to make directory path
        return 0

    # Remove file/link/node. Unlinking of hard links removes data from last hardlink removed
    def unlink(self, path):                 # defines unlink to rmdir to remove directories
        print "*** UNLINK: ", path          # print information used for debugging
        if path == "/" + self.randomFilename or path == "/" + self.cpmFilename:
            to_return = -errno.EPERM        # return an "operation not permitted" error
        elif path in self.open_files:       # error if path is open
            print "File must be closed to unlink, release open files: "
            for files in self.open_files:   # list open files
                print files
            to_return = -errno.EACCES       # return an "access denied"" error
        else:
            os.unlink(self.root_dir + path) # syscall to unlink
            to_return = 0
        return to_return

    # Rename a file/directory from a location to a new name or location
    def rename(self, oldpath, newpath):     # defines renaming/moving method for files
        print "*** RENAME: ", oldpath       # print oldpath information used for debugging
        print "***     TO: ", newpath       # print newpath information used for debugging
        if oldpath == "/" + self.randomFilename or oldpath == "/" + self.cpmFilename or \
          newpath == "/" + self.randomFilename or newpath == "/" + self.cpmFilename:
            to_return = -errno.EPERM        # return an "operation not permitted" error
        else:
            os.rename(self.root_dir + oldpath, self.root_dir + newpath)   # syscall to rename file
            to_return = 0
        return to_return

    # ==================== File Methods ====================

    # creates path not previously in existence
    def create(self, path, flags, mode):                # defines method to create file
        print "*** CREATE: ", path                      # print for debugging
        if path == "/" + self.randomFilename or path == "/" + self.cpmFilename:
            to_return = -errno.EPERM                    # return an "operation not permitted" error
        else:
            fhandle = open(self.root_dir + path, "w")   # opens new file to write to
            self.open_files[path] = fhandle             # open new file
            to_return = 0
        return to_return

    # Opens a file to read or write
    def open(self, path, flags):    # defines method to open a file
        print "*** OPEN: ", path    # print information used for debugging
        print "---               ---"

        access_flags = os.O_RDONLY | os.O_WRONLY | os.O_RDWR    # set access flags
        access_flags = flags & access_flags

        if path == "/" + self.randomFilename or path == "/" + self.cpmFilename:
            to_return = 0
        elif access_flags == os.O_RDONLY:                   # if file is "read only"
            file_handle = open(self.root_dir + path, "rb")  # open file in "read only/binary" mode
            self.open_files[path] = file_handle             # open file moved to open_files list
            to_return = 0
        elif access_flags & os.O_WRONLY == os.O_WRONLY or \
          access_flags & os.O_RDWR == os.O_RDWR:            # if file is "write only" or "read & write"
            file_handle = open(self.root_dir + path, "wb")  # file opened in "write only/binary" mode
            self.open_files[path] = file_handle             # open file moved to open_files list
            to_return = 0
        else:
            to_return = -errno.EACCES  # if file doesn't fit prior criteria, error: permission denied
        return to_return

    # Reads file data to buffer, beginning at offset in a file.
    def read(self, path, size, offset):         # defines method to read file
        print "*** READ: ", path
        print "**  size: ", size
        print "* offset: ", offset              # print information used for debugging

        if path == "/" + self.randomFilename or path == "/" + self.cpmFilename:
            # this is where the magic happens
            to_return = 0
        else:
            file_handle = self.open_files[path] # initialize variable with opened file
            file_handle.seek(offset)            # seek/find location in file to read data from
            to_return = file_handle.read(size)  # reads for a given length
        return to_return

    # Writes file data from buffer beginning at file start offset
    def write(self, path, buf, offset, file_handle=None):  # defines method to write to a file
        print "*** WRITE: ", path
        print "** offset: ", offset             # print information used for debugging

        if path == "/" + self.randomFilename or path == "/" + self.cpmFilename:
            to_return = -errno.EPERM            # return an "operation not permitted" error
        else:
            file_handle = self.open_files[path] # set output file to value
            file_handle.seek(offset)            # find/seek location (aka offset) from file start
            file_handle.write(buf)              # write to file from buffer
            to_return = len(buf)                # return buffer length
        return to_return

    # Called on each close so that the filesystem has a chance to report delayed errors.
    def flush(self, path, file_handle=None):    # defines flush method for Fuse
        print "*** FLUSH: ", path               # print information used for debugging

        if path == "/" + self.randomFilename or path == "/" + self.cpmFilename:
            to_return = 0                       # ignore the flush and do nothing
        elif path in self.open_files:           # if path is open, flush the buffer
            file_handle = self.open_files[path]
            file_handle.flush()
            to_return = 0
        return to_return

    # Closes files and frees-up allocated space
    def release(self, path, file_handle=None):  # releases files and re-allocates used space
        print "*** RELEASE: ", path             # print information used for debugging

        if path == "/" + self.randomFilename or path == "/" + self.cpmFilename:
            to_return = 0                       # ignore the release and do nothing
        elif path in self.open_files:           # if there are open files listed
            file_handle = self.open_files[path] # open file assigned to filehandler and closed
            file_handle.close()
            del self.open_files[path]           # delete/reallocate space from open file
            to_return = 0
        return to_return

if __name__ == '__main__':
    FS = MyFuse()
    FS.parse(errex=1)
    FS.main()
