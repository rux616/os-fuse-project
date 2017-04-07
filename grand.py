#!/usr/bin/env python
#-*- coding: utf-8 -*-
                    # encode/decode w/ utf-8: full-range of unicode chars, w/o addressing endian issues
import errno        # makes available errno system calls
import fuse         
import stat         # Constants/functions for interpreting results of os.stat()
import os           # needed for os interfaces
import pickle       # serializes/deserializes object to/from a character string
import sys          # provides access to variables used/maintained by interpreter (inc. argv)
import time

   # import glob        # included in Prof. W. code, not needed
   # import hashlib     # included in Prof. W. code, not needed

fuse.fuse_python_api = (0, 2)   # application programming interface (0, 2)

class MyFuse(fuse.Fuse):
    
    # Initializes the filesystem
    def __init__(self, *args, **kw):    # OOP constructor
        for x in sys.argv:              # print for debugging
            print " *** " + x           # print all arguments in sequence
        print ":--- " + sys.argv[-2] + " ---:"   # New line prints second to last argument

        self.root = '/'
        self.open_files = {}            # initialize open_files
                                        # pickle.load deserializes hardlinks for object
        # self.hard_links = pickle.load(open(sys.argv[-2] + "/.MyFuse_hard_links", "rb"))  
        fuse.Fuse.__init__(self, *args, **kw)       # creates fuse Object
            
    # ================================== Helper Method =================================

    # Simple helper method to provide full file path if given only a partial path
    def _full_path(self, partial):              # ensures partial path is altered to full path structure
        if partial.startswith("/"):             # remove / if present
            partial = partial[1:]
        path = os.path.join(self.root, partial) # path.join connects object root + '/' + partial
        return path

    # ============================== Filesystem Methods ===============================

    # Change permissions for object to new permissions
    def chmod(self, path, mode):                    # defines chmod to alter permissions
       # full_path = self._full_path(path)
        print "*** CHMOD: ", self._full_path(path)  # print information used for debugging
        os.chmod(sys.argv[-2] + path, mode)         # syscall updating permissions mode
        return 0
    
    # Obtains file attributes - method fills in the elements of the "stat" structure.
    def getattr(self, path):                    # defines getattr to fetch attribute from file
        print "getattr-path: ", self._full_path(path)    # print information used for debugging
        return os.lstat(sys.argv[-2] + path)    # return object with syscall updating status attributes
    
    # Lists directory entries (dirent) back to a caller   *********** THIS SECTION STILL NEEDS WORK ***** NOT WORKING PROPERLY
    def readdir(self, path, offset):            # defines readdir which lists files/folders
        print "*** READDIR: ", self._full_path(path)    # print information used for debugging
        
        yield fuse.Direntry('.')                        
        yield fuse.Direntry('..')                      
        print "=====  " + sys.argv[-2] + "  ====="      # print information used for debugging
        
        for x in os.listdir(sys.argv[-2] + path):       # list all file basenames in path
            yield fuse.Direntry(os.path.basename(x))    # yield fuse.Direntry(os.path.basename(x))
            
        yield fuse.Direntry('FuseRoot')                 # 
        return      
         #   for e in os.listdir("." + path):
         #   yield fuse.Direntry(e)
    
    # Removes empty directory of specified name
    def rmdir(self, path):                          # defines rmdir to remove directories
        print "*** RMDIR: ", self._full_path(path)  # print information used for debugging
        os.rmdir(self._full_path(path))      # syscall to remove directory path
        return 0
    
    # Creates a new directory of specified name
    def mkdir(self, path, mode):                    # defines mkdir to create new directories
        print "*** MKDIR: ", self._full_path(path)  # print information used for debugging
        os.mkdir(self._full_path(path))      # syscall to make directory path
        return 0

    # Remove file/link/node. Unlinking of hard links removes data from last hardlink was removed
    def unlink(self, path):                         # defines unlink to rmdir to remove directories
        print "*** UNLINK: ", self._full_path(path) # print information used for debugging
        if path in self.open_files:                 # error if path is open
            return -errno.ENOSYS
        
        os.unlink(sys.argv[-2] + path)              # syscall to unlink
        return 0
        
       # return os.unlink(self._full_path(path))
    
    # Rename a file/directory from a location to a new name or location (file can be given a new directory)
    def rename(self, oldpath, newpath):                 # defines renaming/moving method for files
        print "*** RENAME: ", self._full_path(oldpath)  # print oldpath information used for debugging  
        print "***     TO: ", self._full_path(newpath)  # print newpath information used for debugging
        os.rename(sys.argv[-2] + oldpath, sys.argv[-2] + newpath)   # syscall to rename file
        return 0
                 
    # ===================================== File Methods ==========================================

    # Opens a file to read or write
    def open(self, path, flags):                    # defines method to open a file
        print " *** OPEN: ", self._full_path(path)  # print information used for debugging
        
        access_flags = os.O_RDONLY | os.O_WRONLY | os.O_RDWR    # set access flags
        access_flags = flags & access_flags
        
        if access_flags == os.O_RDONLY:             # if file is "read only"
            fi = open(sys.argv[-2] + path, "rb")    # file opened in "read only/binary" mode
            self.open_files[path] = fi              # open file moved to open_files list
            return 0
        else:                                       # if file is "write only" or "read & write"
            fi = open(sys.argv[-2] + path, "wb")    # file opened in "write only/binary" mode
            self.open_files[path] = fi              # open file moved to open_files list
            return 0
        
        return -errno.EACCESS       # if file doesn't fit prior criteria, error: permission denied
        #      return os.open(full_path, flags)

    # Reads file data to buffer, beginning at offset in a file.
    def read(self, path, length, offset):           # defines method to read file
        print "*** READ : ", self._full_path(path), length, offset   # print information used for debugging
        
        fi = self.open_files[path]          # initialize variable with opened file
        fi.seek(offset)                     # seek/find location in file to read data from
        
        return fi.read(length)              # returns reading from a given length
       # os.lseek(fh, offset, os.SEEK_SET)
       # return os.read(fh, length)

    # Writes file data from buffer beginning at file start offset           
    def write(self, path, buf, offset, fh):     # defines method to write to a file
        print "*** WRITE: ", self._full_path(path), offset      # print information used for debugging
        
        fo = self.open_files[path]      # set output file to value
        fo.seek(offset)                 # find/seek location (aka offset) from file start
        fo.write(buf)                   # write to file from buffer
        return len(buf)                 # return buffer length

    # Called on each close so that the filesystem has a chance to report delayed errors.             
    def flush(self, path, fh):                          # defines flush method for Fuse
        print "*** FLUSH: ", self._full_path(path)      # print information used for debugging
        if path in self.open_files:                     # if path is open, close it and flush
            fh = self.open_files[path]
            fh.flush() 
        return 0
        #return os.fsync(fh)

    # Closes files and frees-up allocated space            
    def release(self, path, fh = None):     # releases files and re-allocates used space
        print "*** RELEASE: ", self._full_path(path)    # print information used for debugging
        
        if path in self.open_files:     # if there are open files listed
            fh = self.open_files[path]  # open file assigned to filehandler and closed
            fh.close()                               
            del self.open_files[path]   # delete/reallocate space from open file
        return 0

if __name__ == '__main__':
    fs = MyFuse()
    fs.parse(errex = 1)
    fs.main()
    
