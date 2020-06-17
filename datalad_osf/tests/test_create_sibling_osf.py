from datalad.tests.utils import (
    SkipTest,
    with_tree
)

minimal_repo = {'ds': {'file1.txt': 'content',
                       'subdir': {'file2.txt': 'different content'}
                       }
                }


@with_tree(tree=minimal_repo)
def test_invalid_calls(path):

    # - impossible w/o dataset
    # - impossible w/o annex
    # - mandatory arguments
    raise SkipTest("Needs test setup")


@with_tree(tree=minimal_repo)
def test_create_osf(path):

    # - create the OSF project(s)
    # - test result via osfclient or just test it being functional?
    # - test for correct config in git-annex:remote.log

    # - annex-move and annex-get again
    # - account for export when implemented
    raise SkipTest("Needs test setup")
