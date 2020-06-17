from os.path import curdir

from datalad.interface.base import Interface
from datalad.interface.base import build_doc
from datalad.support.param import Parameter
from datalad.distribution.dataset import (
    datasetmethod,
    EnsureDataset,
    require_dataset
)
from datalad.interface.utils import eval_results
from datalad.support.constraints import (
    EnsureNone,
    EnsureStr,
    EnsureChoice,
    EnsureBool,
)
from datalad.interface.results import get_status_dict


@build_doc
class CreateSiblingOSF(Interface):
    """Short description of the command

    Long description of arbitrary volume.
    """

    _params_ = dict(
        dataset=Parameter(
            args=("-d", "--dataset"),
            doc=""""Dataset to extract metadata from. If no further
        constraining path is given, metadata is extracted from all files
        of the dataset.""",
            constraints=EnsureDataset() | EnsureNone()),
        title=Parameter(),
        path=Parameter(),
        sibling=Parameter(),
    )

    @staticmethod
    @datasetmethod(name='create_sibling_osf')
    @eval_results
    def __call__(dataset=None, title=None, path=None, sibling=None):
        ds = require_dataset(dataset,
                             purpose="create OSF remote",
                             check_installed=True)
