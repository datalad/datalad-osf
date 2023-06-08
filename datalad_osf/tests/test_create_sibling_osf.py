# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See LICENSE file distributed along with the datalad_osf package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##

from datalad_next.tests.utils import assert_result_count
from datalad_osf.utils import delete_node
from osfclient import OSF


#def test_invalid_calls(minimal_dataset):
#
#    # - impossible w/o dataset
#    # - impossible w/o annex
#    # - mandatory arguments
#    raise SkipTest("TODO")


def test_create_osf_simple(osf_credentials_or_skip, minimal_dataset):

    ds = minimal_dataset

    file1 = ds.pathobj / "file1.txt"

    create_results = ds.create_sibling_osf(name="osf")

    assert_result_count(create_results, 2, status='ok')
    assert_result_count(
        create_results, 1,
        status='ok', type='dataset', name="osf-storage", path=ds.path)
    assert_result_count(
        create_results, 1,
        status='ok', type='sibling', name="osf", path=ds.path)

    # if we got here, we created something at OSF;
    # make sure, we clean up afterwards
    try:
        # special remote is configured:
        remote_log = ds.repo.call_git(['cat-file', 'blob',
                                       'git-annex:remote.log'])
        assert "node={}".format(create_results[0]['id']) in remote_log

        # copy files over
        ds.repo.copy_to('.', "osf-storage")
        whereis = ds.repo.whereis(str(file1))
        here = ds.config.get("annex.uuid")
        # files should be 'here' and on remote end:
        assert len(whereis) == 2
        assert here in whereis

        # drop content here
        ds.drop('.')
        whereis = ds.repo.whereis(str(file1))
        # now on remote end only
        assert len(whereis) == 1
        assert here not in whereis

        # and get content again from remote:
        ds.get('.')
        whereis = ds.repo.whereis(str(file1))
        assert len(whereis) == 2
        assert here in whereis
    finally:
        # clean remote end:
        osf = OSF(**osf_credentials_or_skip)
        delete_node(osf.session, create_results[0]['id'])


def test_create_osf_export(osf_credentials_or_skip, minimal_dataset):

    ds = minimal_dataset

    create_results = ds.create_sibling_osf(
        title="CI dl-create",
        # do not create a git-remote
        mode="exportonly")

    assert_result_count(
        create_results, 1,
        status='ok', type='dataset', name='osf-storage', path=ds.path)

    # if we got here, we created something at OSF;
    # make sure, we clean up afterwards
    try:

        # for now just run an export and make sure it doesn't fail
        ds.repo.call_git(['annex', 'export', 'HEAD', '--to', 'osf-storage'])

    finally:
        # clean remote end:
        osf = OSF(**osf_credentials_or_skip)
        delete_node(osf.session, create_results[0]['id'])


# def test_create_osf_existing(osf_credentials_or_skip):
#     raise SkipTest("TODO")
