#!/usr/bin/env python

import os
import sys
import errno

from fuse import FUSE, FuseOSError, Operations

class GRand(Operations):
    def __init__(self, root):
        self.root = root

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================


def main(mountpoint, root):
    FUSE(GRand(root), mountpoint, nothreads=True, foreground=True)

if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1])