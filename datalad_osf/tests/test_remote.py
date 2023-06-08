# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See LICENSE file distributed along with the datalad_osf package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##

from datalad_next.tests.utils import skip_if_on_windows

common_init_opts = ["encryption=none", "type=external", "externaltype=osf",
                    "autoenable=true"]


# testremote itself fails in the prep-phase, before talking to the special
# remote. It might just be that the SHA256 key paths get too long
# https://github.com/datalad/datalad-osf/issues/71
@skip_if_on_windows
def test_gitannex(osf_node, minimal_dataset):
    from datalad.cmd import GitWitlessRunner
    ds = minimal_dataset

    # add remote parameters here
    init_remote_opts = ["node={}".format(osf_node)]

    # add special remote
    init_opts = common_init_opts + init_remote_opts
    ds.repo.init_remote('osfproject', options=init_opts)

    # run git-annex-testremote
    # note, that we don't want to capture output. If something goes wrong we
    # want to see it in test build's output log.
    # TODO use AnnexRepo._call_annex(..., protocol=None) with 0.14+
    GitWitlessRunner(
        cwd=ds.path,
        env=GitWitlessRunner.get_git_environ_adjusted()).run(
            ['git', 'annex', 'testremote', 'osfproject', "--fast"]
    )
