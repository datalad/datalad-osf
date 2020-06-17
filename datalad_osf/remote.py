#!/usr/bin/env python3

import os
import posixpath # OSF uses posix paths!
from urllib.parse import urlparse

from osfclient import OSF
from osfclient.exceptions import UnauthorizedException

from annexremote import Master
from annexremote import SpecialRemote
from annexremote import RemoteError


class OSFRemote(SpecialRemote):
    """git-annex special remote for the open science framework

    The recommended way to use this is to create an OSF project or
    subcomponent.

    .. todo::

       Write doc section on how to do that, and what URL should be used to
       configure the special remote.

    Initialize the special remote::

        git annex initremote dolphinarchive type=external externaltype=osf \\
            encryption=none project=https://osf.io/<your-component-id>/

    Authenticate (optionally)::

    The special remote is usable in a read-only form when configured like this,
    which is perfectly good for most scientific applications.  But to upload a
    dataset in the first place you need to supply a credential. Generate a login
    token at https://osf.io/settings/tokens, giving it "osf.full_read" and
    "osf.full_write" scopes.  Reconfigure the remote like so:

        OSF_TOKEN='uo6g2MInjPRZ09P6Sl4qxX2TnwR3mFA1pMugZ9H1OMp6FtLefrbCxOTIvYn3gFmFOM2Fqx' \\
            git annex enableremote dolphinarchive

    You can also hand out read-only tokens to enable private read-only datasets. Create
    tokens with only "osf.full_read" and give them to your collaborators.

    It is a good idea to get in the habit of generating a new token for each computer you own,
    so that they can be revoked individually when you break or lose a computer, and without
    writing down your central password somewhere it could be stolen. In fact, git-annex
    intentionally keeps credentials to itself during synchronization.

    Usage::

    After initializing files can be transferred the usual way:

        git annex copy . --to='dolphinarchive'
        git annex copy . --from='dolphinarchive'

    Because this is a special remote, the uploaded data do not retain their
    folder structure.

    You may reuse an existing project without overwhelming it with garbled
    filenames by setting a path where git-annex will store its data instead:

        git annex initremote osf type=external externaltype=dolphinarchive \\
            encryption=none project=https://osf.io/<your-component-id>/ \\
            objpath=git-annex

    Configuration::

    The following parameters can be given to `git-annex initremote`, or
    `git annex enableremote` to (re-)configure a special remote.

    `project`
       the OSF URL of the file store

    `path`
       a subpath with (default: /)

     `OSF_TOKEN` (as an environment variable)
       a login token from https://osf.io/settings/tokens/

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
        self.configs['objpath'] = \
            'A path within the OSF project to store git-annex keys in ' \
            '(optional)'

        self.project = None

        # lazily evaluated cache of File objects
        self._files = None

        # flag whether we made sure that the object tree folder exists
        self._have_objpath = False

    def initremote(self):
        if self.annex.getconfig('project') is None:
            raise ValueError('project url must be specified')
            # TODO: type-check the value; it must be https://osf.io/

        if "OSF_TOKEN" in os.environ:
            self.annex.setcreds("osf", "token", os.environ["OSF_TOKEN"])

    def prepare(self):
        """"""
        project_id = posixpath.basename(
            urlparse(self.annex.getconfig('project')).path.strip(posixpath.sep))

        token = self.annex.getcreds("osf")
        if token.get('user', None) != 'token':
            raise ValueError()
        token = token['password'] or None # cast "" -> None because osfclient doesn't handle "" as 'no token'.

        try:
            osf = OSF(token=token)
            # next one performs initial auth
            self.project = osf.project(project_id)

            # which storage to use, defaults to 'osfstorage'
            # TODO a project could have more than one? Make parameter to select?
            # https://github.com/datalad/datalad-osf/issues/30#issuecomment-645339882
            self.storage = self.project.storage()

            # get a potential path configuration indicating which folder to put
            # the annex object tree at
            self.objpath = self.annex.getconfig('objpath')
            if not self.objpath:
                # use a sensible default, avoid putting keys into the root
                self.objpath = '/git-annex'
            if not self.objpath.startswith(posixpath.sep):
                # ensure a normalized format
                self.objpath = posixpath.sep + self.objpath
        except Exception as e:
            self.annex.info(repr(e))
            raise RemoteError(repr(e))

    def transfer_store(self, key, filename):
        ""
        try:
            # make sure we have the target folder, but only do it once
            # in the lifetime of the special remote process, because
            # it is relatively expensive
            if not self._have_objpath:
                # osfclient (or maybe OSF?) is a little weird:
                # you cannot create_folder("a/b/c/"), even if "a/b" already
                # exists; you need to instead do
                # create_folder("a").create_folder("b").create_folder("c")
                # but you can create_file("a/b/c/d.bin"), and in fact you
                # *cannot* create_folder("c").create_file("d.bin")
                # TODO: patch osfclient to be more intuitive.
                self._osf_makedirs(self.storage, self.objpath, exist_ok=True)
                # TODO: is this slow? does it do a roundtrip for each path?
                self._have_objpath = True

            with open(filename, 'rb') as fp:
                self.storage.create_file(
                    posixpath.join(self.objpath, key), fp,
                    force=True, update=True)
        except Exception as e:
            raise RemoteError(e)
        # we need to register the idea that this key is now present, but
        # we also want to avoid (re)requesting file info
        if self._files:
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
                # only consider files that are stored in the configured
                # object tree folder
                if f.path.startswith(self.objpath + posixpath.sep)
            }
        return self._files


def main():
    master = Master()
    remote = OSFRemote(master)
    master.LinkRemote(remote)
    master.Listen()


if __name__ == "__main__":
    main()
