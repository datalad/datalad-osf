# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See LICENSE file distributed along with the datalad_osf package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##

from mock import patch

from datalad.api import clone

from datalad.tests.utils import (
    assert_in,
    eq_,
    with_tempfile,
)


def no_credentials(*args, **kwargs):
    return dict(token=None, username=None, password=None)


@with_tempfile
# make sure that even with locally configured credentials
# none actually reach the special remote
@patch('datalad_osf.utils.get_credentials', no_credentials)
def test_readonly_access(path):
    # obtain a prepared minimal dataset with pre-configured
    # OSF remotes and prestaged data
    ds = clone('https://github.com/datalad/testrepo--minimalds-osf.git', path)
    # check that both OSF remotes were enabled
    assert_in('osfannex', ds.repo.get_remotes())
    assert_in('osftree', ds.repo.get_remotes())
    test_file = ds.repo.pathobj / 'inannex' / 'animated.gif'
    test_file_status = ds.repo.annexstatus([test_file])[test_file]
    eq_(test_file_status['has_content'], False)
    # git-annex reports annexed file to be available on osf remote
    eq_(ds.repo.get_special_remotes()[
        '82d91e46-58da-4625-96c0-56aadef98d49']['name'],
        'osfannex')
    assert_in(
        '82d91e46-58da-4625-96c0-56aadef98d49',
        ds.repo.whereis('inannex'))
    # obtain content, from osfannex specifically to avoid 'wget'
    ds.repo.call_git(['annex', 'copy', str(test_file), '-f', 'osfannex'])
    eq_(ds.repo.annexstatus([test_file])[test_file]['has_content'], True)
