#!/usr/bin/env python
#-*- coding: utf-8 -*-
               # encode/decode w/ utf-8: full-range of unicode chars, w/o addressing endian issues
import errno   # makes available errno system calls
import fuse    # include fuse calls from python-fuse
import stat    # constants/functions for interpreting results of os.stat()
import os      # needed for os interfaces
import sys     # provides access to variables used/maintained by interpreter (inc. argv)
import time    # gives time functions

fuse.fuse_python_api = (0, 2)   # application programming interface (0, 2)

class MyFuse(fuse.Fuse):
    randomFilename = "grandom"      # variable to hold the filename for random number access
    cpmFilename = "gcpm"            # variable to hold the filename for CPM access

    # Initializes the filesystem
    def __init__(self, *args, **kw):    # OOP constructor
        for x in sys.argv:              # print for debugging
            print " *** " + x           # print all arguments in sequence

        # require standardized call with root directory and mountpoint
        if (len(sys.argv) < 3) or (sys.argv[-2][0] == '-') or (sys.argv[-1][0] == '-'):
            print "Error, proper input:"
            print "      MyFuse [-options] rootDir mountPoint"
            print "or interpreting script:"
            print "      python MyFuse.py [-options] rootDir mountPoint"
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
            print "Error: rootDir and mountPoint cannot be the same."
            must_exit = True
        if must_exit is True:
            sys.exit(0)

        self.rootDir = sys.argv[-2]
        print ":--- " + self.rootDir + " ---:"  # prints second to last argument/rootDir"
        self.open_files = {}                    # initialize open_files to empty
        fuse.Fuse.__init__(self, *args, **kw)   # creates fuse Object

  # ==================== Filesystem Methods ====================

    # Change permissions for object to new permissions
    def chmod(self, path, mode):             # defines chmod to alter permissions
        print "*** CHMOD: ", path            # print information used for debugging
        os.chmod(self.rootDir + path, mode)  # syscall updating permissions mode
        return 0
    
    # Obtains file attributes - method fills in the elements of the "stat" structure.
    def getattr(self, path):                  # defines getattr to fetch attribute from file
        print "GETATTR-path: ", path          # print information used for debugging
        if path == "/" + self.randomFilename:      # handle the random file
            to_return = os.lstat("/dev/random")
            # to_return
        elif path == "/" + self.cpmFilename:       # handle the cpm file
            to_return = os.lstat("/dev/random")
            # to_return
        else:
            to_return = os.lstat(self.rootDir + path)
        return to_return                      # return object with syscall updating status attributes

    # Lists directory entries (dirent) back to a caller
    def readdir(self, path, offset):   # defines readdir which lists files/folders
        print "\n\n*** READDIR: ", path    # print information used for debugging
        print "=====  " + self.rootDir + "  ====="  # print information used for debugging
        for e in '.', '..':
            yield fuse.Direntry(e)
        for x in os.listdir(self.rootDir + path):     # list all file basenames in path
            yield fuse.Direntry(os.path.basename(x))  # yield fuse.Direntry(os.path.basename(x))
        for e in self.randomFilename, self.cpmFilename:
            yield fuse.Direntry(e)
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
    def unlink(self, path):          # defines unlink to rmdir to remove directories
        print "*** UNLINK: ", path   # print information used for debugging
        if path in self.open_files:  # error if path is open
            print "File must be closed to unlink, release open files: "
            for x in self.open_files:   # list open files
                print x
            return -errno.ENOSYS        # error function not implemented
        os.unlink(self.rootDir + path)  # syscall to unlink
        return 0

    # Rename a file/directory from a location to a new name or location (file can be given a new directory)
    def rename(self, oldpath, newpath):   # defines renaming/moving method for files
        print "*** RENAME: ", oldpath     # print oldpath information used for debugging
        print "***     TO: ", newpath     # print newpath information used for debugging
        os.rename(self.rootDir + oldpath, self.rootDir + newpath)   # syscall to rename file
        return 0

    # ==================== File Methods ====================

    # creates path not previously in existence
    def create(self, path, flags, mode):            # defines method to create file
        print "*** CREATE: ", path                  # print for debugging
        fhandle = open(self.rootDir + path, "w")    # opens new file to write to
        self.open_files[path] = fhandle             # open new file
        return 0

    # Opens a file to read or write
    def open(self, path, flags):   # defines method to open a file
        print "*** OPEN: ", path  # print information used for debugging
        print "---               ---"

        access_flags = os.O_RDONLY | os.O_WRONLY | os.O_RDWR    # set access flags
        access_flags = flags & access_flags

        if access_flags == os.O_RDONLY:           # if file is "read only"
            fi = open(self.rootDir + path, "rb")  # file opened in "read only/binary" mode
            self.open_files[path] = fi            # open file moved to open_files list
            return 0
        else:                                     # if file is "write only" or "read & write"
            fi = open(self.rootDir + path, "wb")  # file opened in "write only/binary" mode
            self.open_files[path] = fi            # open file moved to open_files list
            return 0
        return -errno.EACCESS  # if file doesn't fit prior criteria, error: permission denied

    # Reads file data to buffer, beginning at offset in a file.
    def read(self, path, size, offset):  # defines method to read file
        print "*** READ: ", path
        print "**  size: ", size
        print "* offset: ", offset      # print information used for debugging

        fhread = self.open_files[path]  # initialize variable with opened file
        fhread.seek(offset)             # seek/find location in file to read data from
        return fhread.read(size)      # returns reading from a given length

    # Writes file data from buffer beginning at file start offset
    def write(self, path, buf, offset, fh = None):  # defines method to write to a file
        print "*** WRITE: ", path
        print "** offset: ", offset       # print information used for debugging

        fhwrite = self.open_files[path]   # set output file to value
        fhwrite.seek(offset)              # find/seek location (aka offset) from file start
        fhwrite.write(buf)                # write to file from buffer
        return len(buf)                   # return buffer length

    # Called on each close so that the filesystem has a chance to report delayed errors.
    def flush(self, path, fh = None):         # defines flush method for Fuse
        print "*** FLUSH: ", path      # print information used for debugging
        if path in self.open_files:    # if path is open, flush the buffer
            fh = self.open_files[path]
            fh.flush()
        return 0

    # Closes files and frees-up allocated space
    def release(self, path, fh = None):  # releases files and re-allocates used space
        print "*** RELEASE: ", path      # print information used for debugging
        if path in self.open_files:      # if there are open files listed
            fh = self.open_files[path]   # open file assigned to filehandler and closed
            fh.close()
            del self.open_files[path]    # delete/reallocate space from open file
        return 0

if __name__ == '__main__':
    fs = MyFuse()
    fs.parse(errex=1)
    fs.main()
