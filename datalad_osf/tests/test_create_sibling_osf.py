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
from datalad.tests.utils import (
    assert_equal,
    assert_in,
    assert_not_in,
    assert_result_count,
    skip_if,
    SkipTest,
    with_tree
)
from datalad.utils import Path
from datalad_osf.utils import (
    delete_node,
    get_credentials,
)
from osfclient import OSF


minimal_repo = {'ds': {'file1.txt': 'content',
                       'subdir': {'file2.txt': 'different content'}
                       }
                }


@with_tree(tree=minimal_repo)
def test_invalid_calls(path):

    # - impossible w/o dataset
    # - impossible w/o annex
    # - mandatory arguments
    raise SkipTest("TODO")


@skip_if(cond=not any(get_credentials().values()), msg='no OSF credentials')
@with_tree(tree=minimal_repo)
def test_create_osf_simple(path):

    ds = Dataset(path).create(force=True)
    ds.save()

    file1 = Path('ds') / "file1.txt"

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
        assert_in("node={}".format(create_results[0]['id']), remote_log)

        # copy files over
        ds.repo.copy_to('.', "osf-storage")
        whereis = ds.repo.whereis(str(file1))
        here = ds.config.get("annex.uuid")
        # files should be 'here' and on remote end:
        assert_equal(len(whereis), 2)
        assert_in(here, whereis)

        # drop content here
        ds.drop('.')
        whereis = ds.repo.whereis(str(file1))
        # now on remote end only
        assert_equal(len(whereis), 1)
        assert_not_in(here, whereis)

        # and get content again from remote:
        ds.get('.')
        whereis = ds.repo.whereis(str(file1))
        assert_equal(len(whereis), 2)
        assert_in(here, whereis)
    finally:
        # clean remote end:
        cred = get_credentials(allow_interactive=False)
        osf = OSF(**cred)
        delete_node(osf.session, create_results[0]['id'])


@skip_if(cond=not any(get_credentials().values()), msg='no OSF credentials')
@with_tree(tree=minimal_repo)
def test_create_osf_export(path):

    ds = Dataset(path).create(force=True)
    ds.save()

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
        cred = get_credentials(allow_interactive=False)
        osf = OSF(**cred)
        delete_node(osf.session, create_results[0]['id'])


@skip_if(cond=not any(get_credentials().values()), msg='no OSF credentials')
def test_create_osf_existing():

    raise SkipTest("TODO")
