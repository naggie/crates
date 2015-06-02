# basic CAS. An extension could use multiple disks + redis and manage
# redundancy to make best effort use of all disk space.


# TODO deal with: (in base class, NotImplementedError)
# TODO scrub method could deal with one ref at a time to enable a web progress
# TODO atomic writes (not that important)
# bar (exhaust generator and iteratr over list)


# In the future, this could be a module in it's own directory with the
# following implementations:
# * Amazon S3 encrypted CAS (local cache)
# * CAS with local replication to tolerate hardware failure
# * ... etc


import os
import re
import hashlib
from shutil import copyfile,move
from os import listdir,chmod,makedirs,symlink,unlink,fdopen,mkdir
from os.path import isdir, join, exists, abspath, dirname
from django.conf import settings

from tempfile import mkstemp

class BasicCAS:
    def __init__(self):
        'Get ready to insert or select objects'
        if settings.CAS_DIRECTORY[0] != '/':
            raise ValueError('CAS_DIRECTORY must be an absolute path')

        if not exists(settings.CAS_DIRECTORY):
            makedirs(settings.CAS_DIRECTORY)

        # make the bins in advance, so that pyionotify can work
        # non-automatically
        for x in xrange(256):
            # first 2 characters of all possible refs
            bin_name = '{0:02x}'.format(x)
            directory = join(settings.CAS_DIRECTORY,bin_name)
            if not exists(directory):
                mkdir(directory)

    def insert_file(self,filepath):
        'Add a file to the CAS returning a ref'
        ref = self._hash(filepath)
        binpath = self._binpath(ref)

        if not exists(binpath):
            copyfile(filepath, binpath)
        elif self._hash(binpath) != ref:
            # opportunistic repair of data
            unlink(binpath)
            copyfile(filepath, binpath)

        chmod(binpath,0444)

        return ref

    def insert_blob(self,blob):
        sha = hashlib.sha256()
        sha.update(blob)
        ref =  sha.hexdigest()
        binpath = self._binpath(ref)

        if not exists(binpath):
            with open(binpath,'wb') as f:
                f.write(blob)

            chmod(binpath,0444)

        return ref

    def insert_generator(self,generator):
        '''
        Insert a file by streaming from a generator such as
        requests.get(url,stream=True).iter_content(chunk_size=8192)
        '''
        fd,tmpfilepath = mkstemp(dir=settings.CAS_DIRECTORY,prefix='gen_')
        sha = hashlib.sha256()
        # convert os level file descriptor so it can be closed automatically
        with fdopen(fd,'wb') as f:
            for chunk in generator:
                sha.update(chunk)
                f.write(chunk)
            f.flush() # internal buffers, not yet os buffers. os.fsync for that.

        ref =  sha.hexdigest()
        binpath = self._binpath(ref)

        # atomic, won't leave truncated file in CAS store.
        # TODO: implement atomic saving for other methods
        # TODO: on exception unlink tmp file
        move(tmpfilepath,binpath)
        return ref

    def select(self,ref):
        'Given a ref, return an absolute filepath. If not found, except IOError'
        binpath = self._binpath(ref)

        if not exists(binpath):
            raise IOError('%s not found in CAS' % ref)

        return binpath

    def delete(self,ref):
        'Remove an object from the CAS by ref'
        filepath = self._binpath(ref)

        if exists(filepath):
            unlink(filepath)

    #def link_in(self,filepath):
    #    'insert() a file then replace with a read-only symlink'
    #    ref = self.insert(filepath)
    #    unlink(filepath)
    #    self._symlink(binpath,filepath)
    #    return ref

    def link_out(self,ref,destination):
        '''create an absolute symlink in a path pointing to a ref. If the
        directory tree does not exist, it will be created'''
        binpath = self.select(ref)

        destination_dir = dirname(destination)

        if not isdir(destination_dir):
            makedirs( dirname(destination) )

        self._symlink(binpath,destination)


    def has(self,ref):
        'Convenience method, does this file exist locally by ref?'
        binpath = self._binpath(ref)
        return exists(binpath)


    def enumerate(self):
        'A generator that yields all refs'

        bins = [d for d in map(lambda d: join(settings.CAS_DIRECTORY,d),listdir(settings.CAS_DIRECTORY))]

        for d in bins:
            if not re.search(r'/[a-f0-9]{2}$',d): continue
            for f in listdir(d):
                filepath = join(d,f)
                ref = str(d[-2:])+str(f[:-4])
                yield ref

    def scrub(self):
        '''
        Return refs that no longer represent the linked file. This can
        happen due to disk corruption, or more likely mutation of the file
        thanks to an external program such as serato modifying the metadata.

        To deal with corruption, the files can be re-imported if they are
        simply mutated, otherwise (preferably) they can be harvested from
        connected peers just like a data recovery.
        '''

        dirty = list()

        for ref in self.enumerate():
            filepath = self._binpath(ref)

            if self._hash(filepath) != ref:
                dirty.append(ref)

        return dirty

    def stats(self):
        'Return stats of this CAS surrounding disk usage'
        from os import stat,statvfs # not on mac
        s = statvfs(settings.CAS_DIRECTORY)

        total = 0
        count = 0

        for ref in self.enumerate():
            binpath = self._binpath(ref)
            total += stat(binpath).st_size
            count +=1

        return dict(
            # disk
            free_bytes = s.f_bsize*s.f_bavail,
            used_bytes = s.f_bsize*s.f_blocks,
            # CAS
            total_bytes = total,
            object_count = count,
        )

    def _hash(self, filepath):
        'Run a hashing function on a given file to generate a ref. In this case SHA256'
        sha = hashlib.sha256()
        with open(filepath, 'rb') as f:
            while True:
                block = f.read(1024 * 1024 *10)  # 10MB
                if block == "": break
                sha.update(block)

        return sha.hexdigest()


    def _binpath(self, ref):
        'Given a ref, return a filepath'

        if not re.match(r'^[a-f0-9]{64}$', ref):
            raise ValueError('CAS reference invalid. Must be lowercase sha256 hex digest.')

        directory = join(settings.CAS_DIRECTORY, ref[:2])

        return join(directory, ref[2:] + '.bin')

    def _symlink(self,src, dest):
        'Make an absolute symlink'
        src = abspath(src)
        dest = abspath(dest)
        symlink(src, dest)

