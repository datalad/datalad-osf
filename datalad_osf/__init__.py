# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See LICENSE file distributed along with the datalad_osf package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##

"""DataLad extension for data exchange on the Open Science Framework"""

__docformat__ = 'restructuredtext'



# defines a datalad command suite
# this symbol must be identified as a setuptools entrypoint
# to be found by datalad
command_suite = (
    # description of the command suite, displayed in cmdline help
    "DataLad extension for OSF support",
    [
        ('datalad_osf.credentials', 'OSFCredentials',
            'osf-credentials', 'osf_credentials'),
        # specification of a command, any number of commands can be defined
        (
            # importable module that contains the command implementation
            'datalad_osf.create_sibling_osf',
            # name of the command class implementation in above module
            'CreateSiblingOSF',
            # optional name of the command in the cmdline API
            'create-sibling-osf',
            # optional name of the command in the Python API
            'create_sibling_osf'
        ),
    ]
)


from datalad import setup_package
from datalad import teardown_package

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
