import pytest


@pytest.fixture(autouse=False, scope="function")
def minimal_dataset(existing_dataset):
    ds = existing_dataset
    (ds.pathobj / 'file1.txt').write_text('content')
    (ds.pathobj / 'subdir').mkdir()
    (ds.pathobj / 'subdir' / 'file2.txt').write_text('different content')
    ds.save()

    yield ds


@pytest.fixture(autouse=False, scope="session")
def osf_credentials():
    """Yields credential dict from get_credentials() suitable of OSF client"""
    from datalad_osf.utils import get_credentials
    cred = get_credentials(allow_interactive=False)
    yield cred


@pytest.fixture(autouse=False, scope="function")
def osf_credentials_or_skip(osf_credentials):
    if not any(osf_credentials.values()):
        pytest.skip(reason='no OSF credentials')

    yield osf_credentials


@pytest.fixture(autouse=False, scope="function")
def osf_node(osf_credentials_or_skip):
    from datalad_osf.utils import (
        create_node,
        delete_node,
    )
    from osfclient import OSF
    osf = OSF(**osf_credentials_or_skip)

    title = 'Temporary DataLad CI project'
    category = "data"

    node_id, proj_url = create_node(
        osf.session, title, category=category,
    )
    yield node_id

    delete_node(osf.session, node_id)
