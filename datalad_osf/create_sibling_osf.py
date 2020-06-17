from datalad.interface.base import Interface
from datalad.interface.base import build_doc
from datalad.support.annexrepo import AnnexRepo
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
)
from datalad.interface.results import get_status_dict
from datalad_osf.utils import create_project


@build_doc
class CreateSiblingOSF(Interface):
    """Create a dataset representation at OSF
    """

    _params_ = dict(
        dataset=Parameter(
            args=("-d", "--dataset"),
            doc=""""Dataset to create a sibling for. If no further
        constraining path is given, metadata is extracted from all files
        of the dataset.""",
            constraints=EnsureDataset() | EnsureNone()
        ),
        title=Parameter(
            args=("title",),
            doc="""  """,
            constraints=EnsureStr()
        ),
        sibling=Parameter(
            args=("sibling",),
            doc="""""",
            constraints=EnsureStr()
        ),
        path=Parameter(
            args=("--path",),
            doc="""""",
            constraints=EnsureStr() | EnsureNone()
        ),
    )

    @staticmethod
    @datasetmethod(name='create_sibling_osf')
    @eval_results
    def __call__(title, sibling, path=None, dataset=None):
        ds = require_dataset(dataset,
                             purpose="create OSF remote",
                             check_installed=True)
        # we need an annex
        if not isinstance(ds.repo, AnnexRepo):
            yield get_status_dict(action="create-sibling-osf",
                                  type="dataset",
                                  status="impossible",
                                  message="dataset has no annex")
            return

        # NOTES:
        # - we prob. should check osf-special-remote availability upfront to
        #   fail early
        # - create project on OSF first
        # - initremote second
        # - publish-depends option?
        # - (try to) detect github/gitlab/bitbucket to suggest linking it on
        #   OSF and configure publish dependency
        # - add --recursive option
        #
        # - adapt to conclusions in issue #30
        #   -> create those subcomponents

        proj_id = create_project(title=title)
        init_opts = ["encryption=none",
                     "type=external",
                     "externaltype=osf",
                     "autoenable=true",
                     "project={}".format(proj_id)]
        if path:
            init_opts += ["objpath={}".format(path)]

        ds.repo.init_remote(sibling, options=init_opts)
