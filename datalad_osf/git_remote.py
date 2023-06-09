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

import sys
from urllib.parse import urlparse

from datalad_next.gitremotes.datalad_annex import (
    RepoAnnexGitRemote,
    main as datalad_annex_gitremote_main,
)


class OSFGitRemote(RepoAnnexGitRemote):
    """Very thin wrapper around ``RepoAnnexGitRemote``

    All this class does is to parse ``osf://...`` URLs and assemble the
    corresponding ``datalad-annex::`` URLs.

    Use of this class can be bypassed safely, with no loss of functionality.
    """
    def __init__(self,
                 gitdir,
                 remote,
                 url,
                 instream=sys.stdin,
                 outstream=sys.stdout,
                 errstream=sys.stderr):
        """
        All parameters are passed on to ``RepoAnnexGitRemote``.
        """
        self.parsed_url = urlparse(url)
        if self.parsed_url.path and self.parsed_url.path != '/':
            # project urls have no path
            raise RuntimeError("Only URLs of type osf://<PROJECT ID> are "
                               "supported. Got: %s" % url)

        osf_nodeid = self.parsed_url.netloc.strip('/')

        # we construct a datalad-annex:: URL and init the base class with it.
        # this will not expose all features of datalad-annex::, but users
        # requiring that could just switch to that directly. This is just a
        # backward compatibility/transition shim
        url = f'datalad-annex::?type=external&externaltype=osf&encryption=none&node={osf_nodeid}'

        super().__init__(
            gitdir=gitdir,
            remote=remote,
            url=url,
            instream=instream,
            outstream=outstream,
            errstream=errstream,
        )


def main():
    """git-remote helper executable entrypoint"""
    datalad_annex_gitremote_main(OSFGitRemote)


if __name__ == '__main__':
    main()
