#!/usr/bin/env python3

import os
import posixpath # OSF uses posix paths!
from urllib.parse import urlparse

from datalad_osf.osfclient.osfclient import OSF
from datalad_osf.osfclient.osfclient.exceptions import UnauthorizedException

from annexremote import Master
from annexremote import SpecialRemote
from annexremote import RemoteError


class OSFRemote(SpecialRemote):
    """git-annex special remote for the open science framework

    Any OSF project or component can be used as a remote, but the
    recommended setup is to create a subcomponent of your project
    for archiving your data. Mark it with the Data category so you
    can find it quickly and take note of its URL. Each component
    (or project) has a URL like https://osf.io/6zbyf/ which is
    needed to connect to it.

    .. todo::

       Write doc section on how to do that, and what URL should be used to
       configure the special remote.

    Initialize the special remote::

       git annex initremote osf type=external externaltype=osf \\
            encryption=none project=https://osf.io/<your-component-id>/

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

        self.project = None

        # lazily evaluated cache of File objects
        self._files = None

    def initremote(self):
        ""
        if self.annex.getconfig('project') is None:
            raise ValueError('project url must be specified')
            # TODO: type-check the value; it must be https://osf.io/

    def prepare(self):
        """"""
        project_id = posixpath.basename(
            urlparse(self.annex.getconfig('project')).path.strip(posixpath.sep))

        osf = OSF(
            username=os.environ['OSF_USERNAME'],
            password=os.environ['OSF_PASSWORD'],
        ) # TODO: error checking etc
        # next one performs initial auth
        self.project = osf.project(project_id) # errors ??

        # which storage to use, defaults to 'osfstorage'
        # TODO a project could have more than one? Make parameter to select?
        self.storage = self.project.storage()

    def transfer_store(self, key, filename):
        ""
        try:
            with open(filename, 'rb') as fp:
                self.storage.create_file(key, fp, force=True, update=True)
        except Exception as e:
            raise RemoteError(e)
        # we need to register the idea that this key is now present, but
        # we also want to avoid (re)requesting file info
        if self._files is not None:
            # assign None to indicate that we know this key, but
            # have no info from OSF about it
            self._files[key] = None

    def transfer_retrieve(self, key, filename):
        """Get a key from OSF and store it to `filename`"""
        # we have to discover the file handle
        # TODO is there a way to address a file directly?
        try:
            fobj = self.files[key]
            if fobj is None:
                # we have no info about this particular key -> trigger request
                self._files = None
                fobj = self.files[key]
            with open(filename, 'wb') as fp:
                fobj.write_to(fp)
        except Exception as e:
            # e.g. if the file couldn't be retrieved
            if isinstance(e, UnauthorizedException):
                # UnauthorizedException doesn't give a meaningful str()
                raise RemoteError('Unauthorized access')
            else:
                raise RemoteError(e)

    def checkpresent(self, key):
        "Report whether the OSF project has a particular key"
        try:
            if key not in self.files:
                # we don't know this key at all
                return False
            fobj = self.files.get(key, None)
            if fobj is None:
                # we knew the key, but never checked with OSF if it really
                # has it -> trigger request
                self._files = None
            return key in self.files
        except Exception as e:
            # e.g. if the presence of the key couldn't be determined, eg. in
            # case of connection error
            raise RemoteError(e)

    def remove(self, key):
        """Remove a key from the remote"""
        f = self.files.get(key, None)
        if f is None:
            # removing a not existing key isn't considered an error
            return
        try:
            if f is None:
                self._files = None
                f = self.files[key]
            f.remove()
        except Exception as e:
            raise RemoteError(e)
        # anticipate change in remote and discard obj
        del self.files[key]

    def _osf_makedirs(self, folder, path, exist_ok=False):
        """
        Create folder 'path' inside OSF folder object 'folder'.

        'folder' may also be a osfclient.models.storage.Storage,
          representing the root of a virtual OSF drive.

        Returns the final created folder object.
        """
        for name in path.strip(posixpath.sep).split(posixpath.sep):
            folder = folder.create_folder(name, exist_ok=exist_ok)

        return folder

    @property
    def files(self):
        if self._files is None:
            # get all file info at once
            # per-request latency is substantial, presumably it is overall
            # faster to get all at once
            self._files = {
                f.name: f
                for f in self.storage.files
            }
        return self._files


def main():
    master = Master()
    remote = OSFRemote(master)
    master.LinkRemote(remote)
    master.Listen()


if __name__ == "__main__":
    main()
