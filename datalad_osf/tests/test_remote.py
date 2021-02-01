# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See LICENSE file distributed along with the datalad_osf package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##

from datalad.api import (
    Dataset,
)
from datalad.utils import Path
from datalad.tests.utils import (
    with_tempfile,
    skip_if_on_windows,
    skip_if,
)
from datalad_osf.tests.utils import (
    with_node,
)
from datalad_osf.utils import (
    get_credentials,
)

common_init_opts = ["encryption=none", "type=external", "externaltype=osf",
                    "autoenable=true"]


# testremote itself fails in the prep-phase, before talking to the special
# remote. It might just be that the SHA256 key paths get too long
# https://github.com/datalad/datalad-osf/issues/71
@skip_if_on_windows
@skip_if(cond=not any(get_credentials().values()), msg='no OSF credentials')
@with_node(title="CI osf-special-remote")
@with_tempfile
def test_gitannex(osf_id, dspath):
    from datalad.cmd import GitWitlessRunner
    dspath = Path(dspath)

    ds = Dataset(dspath).create()

    # add remote parameters here
    init_remote_opts = ["node={}".format(osf_id)]

    # add special remote
    init_opts = common_init_opts + init_remote_opts
    ds.repo.init_remote('osfproject', options=init_opts)

    # run git-annex-testremote
    # note, that we don't want to capture output. If something goes wrong we
    # want to see it in test build's output log.
    # TODO use AnnexRepo._call_annex(..., protocol=None) with 0.14+
    GitWitlessRunner(
        cwd=dspath,
        env=GitWitlessRunner.get_git_environ_adjusted()).run(
            ['git', 'annex', 'testremote', 'osfproject', "--fast"]
    )
