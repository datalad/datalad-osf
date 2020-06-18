"""DataLad demo extension"""

__docformat__ = 'restructuredtext'



# defines a datalad command suite
# this symbol must be identified as a setuptools entrypoint
# to be found by datalad
command_suite = (
    # description of the command suite, displayed in cmdline help
    "DataLad extension for OSF support",
    [
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
