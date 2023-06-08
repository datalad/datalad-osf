from datalad.conftest import setup_package

from datalad_next.tests.fixtures import (
    # no test can leave global config modifications behind
    check_gitconfig_global,
    # no test can leave secrets behind
    check_plaintext_keyring,
    # function-scope config manager
    datalad_cfg,
    # function-scope, Dataset instance
    dataset,
    # function-scope, Dataset instance with underlying repository
    existing_dataset,
)

from datalad_osf.tests.fixtures import (
    # standard test dataset setup used throughout the datalad-osf tests
    minimal_dataset,
    osf_credentials,
    osf_credentials_or_skip,
    osf_node,
)
