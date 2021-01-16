#!/usr/bin/env python3
# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See LICENSE file distributed along with the datalad_osf package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##


import os
import json
from os.path import (
    dirname,
    basename,
)
import posixpath # OSF uses posix paths!
from urllib.parse import urlparse

from osfclient import OSF
from osfclient.exceptions import UnauthorizedException

from annexremote import (
    Master,
    ExportRemote,
    RemoteError,
)


class OSFSpecialRemote(ExportRemote):
    """git-annex special remote for the open science framework

    Any OSF node can be used as a remote, but the
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
            encryption=none node=https://osf.io/<your-component-id>/

    To upload files you need to supply credentials.

    .. todo::

       Outline how this can be done

       OSF_USERNAME, OSF_PASSWORD - credentials, OR
       OSF_TOKEN   # TODO: untested, possibly currently broken in osfclient.

    Because this is a special remote, the uploaded data do not retain the
    git folder structure.

    The following parameters can be given to `git-annex initremote`, or
    `git annex enableremote` to (re-)configure a special remote.

    `node`
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
        self.configs['node'] = 'The OSF URL for the remote'

        self.node = None

        # lazily evaluated cache of File objects
        self._files = None

    def initremote(self):
        ""
        if self.annex.getconfig('node') is None:
            raise ValueError('node URL or ID must be specified')
            # TODO: type-check the value; it must be https://osf.io/

    def prepare(self):
        """"""
        node_id = self.annex.getconfig('node')
        if not node_id:
            # fall back on outdated 'project' parameter, which could be
            # just the node ID or a full URL to a project
            node_id = posixpath.basename(
                urlparse(self.annex.getconfig('project')
                         ).path.strip(posixpath.sep))

        if not node_id:
            raise RemoteError('Could not determine OSF node ID')

        try:
            # make use of DataLad's credential manager for a more convenient
            # out-of-the-box behavior
            from datalad_osf.utils import get_credentials
            # we must stay non-interactive, because this is running inside
            # git-annex's special remote protocal
            creds = get_credentials(allow_interactive=False)
        except ImportError as e:
            # whenever anything goes wrong here, stay clam and fall back
            # on envvars.
            # we want this special remote to be fully functional without
            # datalad
            creds = dict(
                username=os.environ.get('OSF_USERNAME', None),
                password=os.environ.get('OSF_PASSWORD', None),
                token=os.environ.get('OSF_TOKEN', None),
            )
        # next one just sets up the stage, no requests performed yet, hence
        # no error checking needed
        # supply both auth credentials, so osfclient can fall back on user/pass
        # if needed
        osf = OSF(**creds)
        # next one performs initial auth
        try:
            self.node = osf.project(node_id)
        except Exception as e:
            # we need to raise RemoteError() such that PREPARE-FAILURE
            # is reported, sadly that doesn't give users any clue
            # TODO support datalad logging here
            raise RemoteError(
                'Failed to obtain OSF node handle: {}'.format(e)
            )
        # which storage to use, defaults to 'osfstorage'
        # TODO a node could have more than one? Make parameter to select?
        self.storage = self.node.storage()

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

    def transferexport_store(self, key, local_file, remote_file):
        "Store the file located at `local_file` to `remote_file` on the remote"
        return self.transfer_store(remote_file, local_file)

    def transfer_retrieve(self, key, filename):
        """Get a key from OSF and store it to `filename`"""
        # we have to discover the file handle
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

    def transferexport_retrieve(self, key, local_file, remote_file):
        """Get the file located at `remote_file` from the remote

        and store it to `local_file`
        """
        return self.transfer_retrieve(remote_file, local_file)

    def checkpresent(self, key):
        "Report whether the OSF node has a particular key"
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

    def checkpresentexport(self, key, remote_file):
        """Return  if the file `remote_file` is present in the remote"""
        return self.checkpresent(remote_file)

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

    def removeexport(self, key, remote_file):
        """Remove the file in `remote_file` from the remote"""
        return self.remove(remote_file)

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
                # strip leading prefix to be directly indexable with ani
                # annex key
                f.path.lstrip(posixpath.sep): f
                for f in self.storage.files
            }
        return self._files

    def removeexportdirectory(self, remote_directory):
        """Remove the directory `remote_directory` from the remote"""
        try:
            folder = [f for f in self.storage.folders
                      if '{sep}{path}{sep}'.format(
                          sep=posixpath.sep,
                          path=remote_directory)]
            if not folder:
                # note that removing a not existing directory isn't
                # considered an error
                return
            elif len(folder) > 1:
                raise RuntimeError("More than matching folder found")
            folder = folder[0]
            # osfclient has no way to do this with the public API
            # going through the backdoor...
            folder._delete(folder._delete_url)
            # TODO delete all matching records from self._files
        except Exception as e:
            raise RemoteError(e)

    def renameexport(self, key, filename, new_filename):
        """Move the remote file in `name` to `new_name`"""
        try:
            fobj = self.files[filename]
            if fobj is None:
                # we have no info about this particular key -> trigger request
                self._files = None
                fobj = self.files[filename]
            response = self.storage.session.post(
                fobj._move_url,
                data=json.dumps(
                    dict(action='move',
                         path='/{}'.format(dirname(new_filename)),
                         rename=basename(new_filename))
                ),
            )
            if response.status_code != 201:
                raise RuntimeError('{}: {}'.format(response, response.text))
            del self._files[filename]
            self._files[new_filename] = None
        except Exception as e:
            raise RemoteError(repr(e))


def main():
    master = Master()
    remote = OSFSpecialRemote(master)
    master.LinkRemote(remote)
    master.Listen()


if __name__ == "__main__":
    main()
