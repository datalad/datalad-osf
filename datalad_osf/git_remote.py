#!/usr/bin/env python
## emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See LICENSE file distributed along with the datalad package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""
"""

import json
import os
from tempfile import TemporaryFile
from pathlib import Path
from shutil import (
    rmtree,
    make_archive,
)
import zipfile
import subprocess
import sys
from urllib.parse import urlparse
from unittest.mock import patch
import posixpath

from osfclient import OSF


class OSFGitRemote(object):
    """git-remote-helper implementation to maintain a repo archive in OSF projects."""
    def __init__(self,
                 gitdir,
                 remote,
                 url,
                 instream=sys.stdin,
                 outstream=sys.stdout,
                 errstream=sys.stderr):
        """
        Parameters
        ----------
        gitdir : str
          Path to the GITDIR of the repository to operate on (provided
          by Git).
        remote : str
          Remote label to use (provided by Git).
        url : str
          osf://-type URL of the remote (provided by Git).
        instream :
          Stream to read communication from Git from.
        outstream :
          Stream to communicate outcomes to Git.
        errstream :
          Stream for logging.
        """
        self.parsed_url = urlparse(url)
        if self.parsed_url.path and self.parsed_url.path != '/':
            # project urls have no path
            raise RuntimeError("Only URLs of type osf://<PROJECT ID> are "
                               "supported. Got: %s" % url)
        self.remote = remote
        # internal logic relies on workdir to be an absolute path
        self.workdir = Path(gitdir, 'osf', remote).resolve()
        self.repodir = self.workdir / 'repo'
        self.marks_git = self.workdir / "git.marks"
        self.marks_osf = self.workdir / "osf.marks"
        self.refspec = "refs/heads/*:refs/osf/{}/*".format(remote)
        self.instream = instream
        self.outstream = outstream
        self.errstream = errstream

        self.osf = self._get_osf_api()
        self._osfproject = None
        self._osfstorage = None
        self._remote_archive = None

        # TODO delay
        self.workdir.mkdir(parents=True, exist_ok=True)
        self.marks_git.touch()
        self.marks_osf.touch()

    def _get_osf_api(self):
        """"""
        try:
            # make use of DataLad's credential manager for a more convenient
            # out-of-the-box behavior
            from datalad_osf.utils import get_credentials
            # we should be able to allow interactive
            creds = get_credentials(allow_interactive=True)
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
        return OSF(**creds)

    @property
    def osfproject(self):
        if self._osfproject is None:
            # next one performs initial auth, and raise of that goes wrong
            # because of insufficient auth
            self._osfproject = self.osf.project(
                self.parsed_url.netloc.strip('/'))
        return self._osfproject

    @property
    def osfstorage(self):
        if self._osfstorage is None:
            # TODO select storage other than 'osfstorage'?
            # could be done by using the 'path' part of the
            # osf:// URL
            self._osfstorage = self.osfproject.storage()
        return self._osfstorage

    def log(self, *args):
        print(*args, file=self.errstream)

    def send(self, msg):
        print(msg, end='', file=self.outstream, flush=True)

    def get_remote_refs(self):
        """Report remote refs

        There are kept in a dedicated "refs" file at the remote.

        Returns
        -------
        str
        """
        refs_handle = [
            f for f in self.osfstorage.files
            if f.path == '/.git/refs']
        if not len(refs_handle):
            # ls didn't find a repo at the remote end, but could talk to
            # the remote itself -> nothing to there
            return ''
        refs_handle = refs_handle[0]
        with TemporaryFile() as fp:
            refs_handle.write_to(fp)
            fp.seek(0)
            refs = fp.read().decode('ascii')
        return refs

    def get_remote_archive(self):
        """Return an OSFclient file handle for the remote zip archive

        or None if there isn't one at the remote.
        """
        if self._remote_archive:
            return self._remote_archive
        # otherwise search for it
        repo_handle = {
            f.path: f
            for f in self.osfstorage.files
            if f.path.startswith('/.git/repo')
        }
        # pick new-style LZMA-zip, fall back on old 7z, and
        # lastly report None, if there isn't anything
        repo_handle = repo_handle.get(
            '/.git/repo.zip', repo_handle.get(
                '/.git/repo.7z', None))
        self._remote_archive = repo_handle
        return repo_handle

    def get_remote_state(self):
        """Return a dict with hashes for the remote repo archive or None
        """
        archive_handle = self.get_remote_archive()
        return archive_handle.hashes if archive_handle else None

    def mirror_repo_if_needed(self):
        """Ensure a local Git repo mirror of the one archived at the remote.
        """
        # TODO acquire and release lock
        url = self.parsed_url
        # stamp file with last syncronization IDs
        synced = self.workdir / 'synced'
        repo_hashes = None
        if synced.exists():
            repo_hashes = self.get_remote_state()
            if repo_hashes is None:
                # we had it sync'ed before, but now it is gone from the
                # remote -- we have all that is left locally
                synced.unlink()
                # sync stamp removed, but leave any local mirror untouched
                # it may be the only copy left
                return
            # compare states, try to be robust and take any hash match
            # unclear when which hash is available, but any should be good
            last_hashes = json.load(synced.open())
            if any(repo_hashes.get(k, None) == v
                    for k, v in last_hashes.items()):
                # local sync matches remote situation
                return
        if repo_hashes is None:
            # in case we never sync'ed, obtain the ID info prior download
            # so we have it, whenever the download succeeded
            repo_hashes = self.get_remote_state()
        if repo_hashes is None:
            # there is nothing at the remote end
            return
        sync_dir = self.workdir / 'sync'
        sync_dir.mkdir(parents=True, exist_ok=True)
        self.log('Downloading repository archive')
        repo_archive = sync_dir / posixpath.basename(
            self.get_remote_archive().path)
        with (repo_archive).open('wb') as fp:
            self.get_remote_archive().write_to(fp)
        self.log('Extracting repository archive')
        if self.repodir.exists():
            # if we extract, we cannot tollerate left-overs
            rmtree(str(self.repodir), ignore_errors=True)
        if repo_archive.suffix == '.zip':
            with zipfile.ZipFile(str(repo_archive)) as zip:
                zip.extractall(
                    str(self.workdir),
                    # a bit of a safety-net, exclude all unexpected content
                    members=[m for m in zip.namelist() if m.startswith('repo')]
                )
        else:
            # fallback for previous times
            subprocess.run([
                '7z', 'x', str(repo_archive)],
                cwd=str(self.workdir),
                stdout=subprocess.PIPE,
                check=True,
            )
        rmtree(str(sync_dir), ignore_errors=True)
        # update sync stamp only after everything else was successful
        synced.write_text(json.dumps(repo_hashes))

    def import_refs_from_mirror(self, refs):
        """Uses fast-export to pull refs from the local repository mirror

        The mirror must exist, when this functional is called.
        """
        if not self.repodir.exists():
            # this should not happen.If we get here, it means that Git
            # was promised some refs to be available, but there the mirror
            # to pull them from did not materialize. Crash at this point,
            # any recovery form such a situation should have happened
            # before
            raise RuntimeError(
                'osf repository mirror not found')
        env = os.environ.copy()
        env['GIT_DIR'] = str(self.repodir)
        subprocess.run([
            'git', 'fast-export',
            '--import-marks={}'.format(str(self.marks_osf)),
            '--export-marks={}'.format(str(self.marks_osf)),
            '--refspec', self.refspec] + refs,
            env=env,
            check=True,
        )

    def format_refs_in_mirror(self):
        """Format a report on refs in the mirror like LIST wants it

        If the mirror is empty, the report will be empty.
        """
        refs = ''
        if not self.repodir.exists():
            return refs
        env = os.environ.copy()
        env['GIT_DIR'] = str(self.repodir)
        refs += subprocess.run([
            'git', 'for-each-ref', "--format=%(objectname) %(refname)"],
            env=env,
            check=True,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        ).stdout
        HEAD_ref = subprocess.run([
            'git', 'symbolic-ref', 'HEAD'],
            env=env,
            check=True,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        ).stdout
        refs += '@{} HEAD\n'.format(HEAD_ref.strip())
        return refs

    def export_to_osf(self):
        """Export a fast-export stream to osf.

        The stream is fast-import'ed into a local repository mirror first.
        If not mirror repository exists, an empty one is created. The mirror
        is then zip'ed and uploaded.
        """
        # TODO acquire and release lock
        url = self.parsed_url
        env = os.environ.copy()
        env['GIT_DIR'] = str(self.repodir)
        if not self.repodir.exists():
            # ensure we have a repo
            self.repodir.mkdir()
            subprocess.run([
                'git', 'init', '--bare', '--quiet'],
                env=env,
                check=True,
            )
        # which refs did we have in the mirror before the import?
        before = subprocess.run([
            'git', 'for-each-ref', "--format= %(refname) %(objectname) "],
            env=env,
            check=True,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        ).stdout
        # perform actual import
        subprocess.run([
            'git', 'fast-import', '--quiet',
            '--import-marks={}'.format(str(self.marks_osf)),
            '--export-marks={}'.format(str(self.marks_osf))],
            env=env,
            check=True,
        )
        # which refs do we have now?
        after = subprocess.run([
            'git', 'for-each-ref', "--format= %(refname) %(objectname) "],
            env=env,
            check=True,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        ).stdout
        # figure out if anything happened
        upload_failed_marker = (self.workdir / 'upload_failed')
        if upload_failed_marker.exists():
            # we have some unsync'ed data from a previous attempt
            updated_refs = json.load(upload_failed_marker.open())
            need_sync = True
            upload_failed_marker.unlink()
        else:
            updated_refs = []
            need_sync = False
        for line in after.splitlines():
            if line in before:
                # no change in ref
                continue
            else:
                updated_refs.append(line.strip().split()[0])
                need_sync = True

        # TODO acknowledge a failed upload
        if not need_sync:
            return
        subprocess.run([
            'git', 'gc'],
            env=env,
            # who knows why this would fail, but it would not be then end
            # of the world
            check=False,
        )
        # prepare upload pack
        sync_dir = self.workdir / 'sync'
        if not sync_dir.exists():
            sync_dir.mkdir()
        # use our zipfile wrapper to get an LZMA compressed archive
        # via the shutil convenience layer
        with patch('zipfile.ZipFile', LZMAZipFile):
            make_archive(
                str(sync_dir / 'repo'),
                'zip',
                root_dir=str(self.workdir),
                base_dir='repo',
            )
        # dump refs for a later LIST of the remote
        (sync_dir / 'refs').write_text(
            self.format_refs_in_mirror())

        self.log('Upload repository archive')
        try:
            for fpath, tpath in ((sync_dir / 'refs', '/.git/refs'),
                          (sync_dir / 'repo.zip', '/.git/repo.zip')):
                with fpath.open('rb') as fp:
                    self.osfstorage.create_file(
                        tpath, fp, force=True, update=True)
        except Exception as e:
            # TODO we could retry...
            # make a record which refs failed to update/upload
            upload_failed_marker.write_text(
                json.dumps(updated_refs))
            # to not report refs as successfully updated
            raise e
            return

        # we no longer need the repo archive, we keep the actual
        # repo mirror
        rmtree(str(sync_dir), ignore_errors=True)

        # upload was successful, so we can report that
        for ref in updated_refs:
            print('ok {}'.format(ref))

        # lastly update the sync stamp to avoid redownload of what was
        # just uploaded
        synced = self.workdir / 'synced'
        repo_hashes = self.get_remote_state()
        if repo_hashes is None:
            self.log('Failed to update sync stamp after successful upload')
        else:
            synced.write_text(json.dumps(repo_hashes))

    def communicate(self):
        """Implement the necessary pieces of the git-remote-helper protocol

        Uses the input, output and error streams configured for the
        class instance.
        """
        for line in self.instream:
            if line == '\n':
                # orderly exit command
                return
            elif line == 'capabilities\n':
                self.send(
                    'import\n'
                    'export\n'
                    'refspec {refspec}\n'
                    '*import-marks {marks}\n'
                    '*export-marks {marks}\n'
                    'signed-tags\n'
                    '\n'.format(
                        refspec=self.refspec,
                        marks=str(self.marks_git))
                )
            elif line == 'list\n':
                self.send('{}\n'.format(self.get_remote_refs()))
            elif line.startswith('import '):
                # data is being imported from osf
                self.mirror_repo_if_needed()
                refs = [line[7:].strip()]
                while True:
                    line = self.instream.readline()
                    if not line.startswith('import '):
                        break
                    refs.append(line[7:].strip())
                self.send(
                    'feature import-marks={marks}\n'
                    'feature export-marks={marks}\n'
                    'feature done\n'.format(
                        marks=str(self.marks_git))
                )
                self.import_refs_from_mirror(refs)
                self.send('done\n')
            elif line == 'export\n':
                # data is being exported to osf
                self.mirror_repo_if_needed()
                self.export_to_osf()
                self.send(
                    '\n'
                )
            else:
                self.log('UNKNOWN COMMAND', line)
                # unrecoverable error
                return

# tiny wrapper to monkey-patch zipfile in order to have
# shutil.make_archive produce an LZMA-compressed ZIP
class LZMAZipFile(zipfile.ZipFile):
    def __init__(self, *args, **kwargs):
        kwargs.pop('compression', None)
        return super().__init__(
            *args, compression=zipfile.ZIP_LZMA, **kwargs)


def main():
    try:
        if len(sys.argv) < 3:
            raise ValueError("Usage: git-remote-osf REMOTE-NAME URL")

        remote, url = sys.argv[1:3]
        # no fallback, must be present
        gitdir = os.environ['GIT_DIR']

        osf = OSFGitRemote(gitdir, remote, url)
        osf.communicate()
    except Exception as e:
        # Receiving an exception here is "fatal" by definition.
        # Mimicking git's error reporting style.
        print("fatal: " + str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
