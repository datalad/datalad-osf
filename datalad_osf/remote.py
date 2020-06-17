#!/usr/bin/env python3

import os
import posixpath # OSF uses posix paths!
from urllib.parse import urlparse

from osfclient import OSF

from annexremote import Master
from annexremote import SpecialRemote
from annexremote import RemoteError

annex = None
def osf_makedirs(folder, path, exist_ok=False):
    """
    Create folder 'path' inside OSF folder object 'folder'.

    'folder' may also be a osfclient.models.storage.Storage,
      representing the root of a virtual OSF drive.

    Returns the final created folder object.
    """

    annex.info('making')
    annex.info(path)
    annex.info(name)
    for name in path.strip(posixpath.sep).split(posixpath.sep):
        folder = folder.create_folder(name, exist_ok=exist_ok)

    return folder


class OSFRemote(SpecialRemote):
    """git-annex special remote for the open science framework

    The recommended way to use this is to create an OSF project or subcomponent.

    .. todo::

       Write doc section on how to do that, and what URL should be used to
       configure the special remote.

    Initialize the special remote::

       git annex initremote osf type=external externaltype=osf \\
            encryption=none repo='https://osf.io/<your-component-id>/'

    However, you may reuse an existing project without overwhelming it with
    garbled filenames by setting a path where git-annex will store its data::

       git annex initremote osf type=external externaltype=osf \\
            encryption=none repo='https://osf.io/<your-component-id>/' \\
            path='git-annex/'

    To upload files you need to supply credentials.

    .. todo::

       Outline how this can be done

       OSF_USERNAME, OSF_PASSWORD - credentials, OR
       OSF_TOKEN   # TODO: untested, possibly currently broken in osfclient.

    Because this is a special remote, the uploaded data do not retain the
    git folder structure.

    The following parameters can be given to `git-annex initremote`, or
    `git annex enableremote` to (re-)configure a special remote.

    `project`
       the OSF URL of the file store

    `path`
       a subpath with (default: /)

    .. seealso::

        https://git-annex.branchable.com/special_remotes
          Documentation on git-annex special remotes

        https://osf.io
          Open Science Framework, a science-focused filesharing and archiving
          site.
    """
    def __init__(self, *args):
        super().__init__(*args)
        self.configs['project'] = 'The OSF URL for the remote'
        self.configs['path'] = 'A subpath within the OSF project to store git-annex blobs in (optional)'

        self.project = None


    def initremote(self):
        ""
        if self.annex.getconfig('project') is None:
            raise ValueError('project url must be specified')
            # TODO: type-check the value; it must be https://osf.io/
        if self.annex.getconfig('path') is None: # design-question: do we really need this?
            self.annex.setconfig('path', '/')

    def prepare(self):

        project_id = posixpath.basename(urlparse(self.annex.getconfig('project')).path)

        osf = OSF(username=os.environ['OSF_USERNAME'], password=os.environ['OSF_PASSWORD']) # TODO: error checking etc
        #osf.login() # errors???
        self.project = osf.project(project_id) # errors ??

        # cache (annex.getconfig() is an expensive operation)
        self.path = self.annex.getconfig('path')

    def transfer_store(self, key, filename):
        ""
        try:
            # osfclient (or maybe OSF?) is a little weird:
            # you cannot create_folder("a/b/c/"), even if "a/b" already exists;
            # you need to instead do create_folder("a").create_folder("b").create_folder("c")
            # but you can create_file("a/b/c/d.bin"), and in fact you *cannot* create_folder("c").create_file("d.bin")
            # TODO: patch osfclient to be more intuitive.

            osf_makedirs(self.project.storage(), self.path, exist_ok=True)
            # TODO: is this slow? does it do a roundtrip for each path?

            with open(filename, 'rb') as fp:
                self.project.storage().create_file(posixpath.join(self.path, key), fp, update=True)
        except Exception as e:
            raise RemoteError(e)

    def transfer_retrieve(self, key, filename):
        ""
        # get the file identified by `key` and store it to `filename`
        # raise RemoteError if the file couldn't be retrieved

    def checkpresent(self, key):
        ""
        # return True if the key is present in the remote
        # return False if the key is not present
        # raise RemoteError if the presence of the key couldn't be determined, eg. in case of connection error
        
    def remove(self, key):
        ""
        # remove the key from the remote
        # raise RemoteError if it couldn't be removed
        # note that removing a not existing key isn't considered an error



def main():
    master = Master()
    remote = OSFRemote(master)
    master.LinkRemote(remote)
    master.Listen()

if __name__ == "__main__":
    main()
