from os import environ
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
from datalad_osf.osfclient.osfclient import OSF
from datalad_osf.utils import create_project


def _get_credentials():
    """helper to read credentials

    for now go w/ env vars. can be refactored
    to read from datalad configs, credential store, etc.
    """
    token = environ.get("OSF_TOKEN")
    username = environ.get("OSF_USERNAME")
    password = environ.get("OSF_PASSWORD")
    return dict(token=token, username=username, password=password)


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
    )

    @staticmethod
    @datasetmethod(name='create_sibling_osf')
    @eval_results
    def __call__(title, sibling, dataset=None):
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
        # - publish-depends option?
        # - (try to) detect github/gitlab/bitbucket to suggest linking it on
        #   OSF and configure publish dependency
        #   -> prob. overkill; just make it clear in the doc
        # - add --recursive option
        #       - recursive won't work easily. Need to think that through.
        #       - would need a naming scheme for subdatasets
        #       - flat on OSF or a tree?
        #       - how do we detect something is there already, so we can skip
        #         rather than duplicate (with a new name)?
        #         osf-type-special-remote sufficient to decide it's not needed?
        # - adapt to conclusions in issue #30
        #   -> create those subcomponents
        # - results need to report URL for created projects suitable for datalad
        #   output formatting!
        #   -> result_renderer
        #   -> needs to ne returned by create_project

        # - option: Make public!

        cred = _get_credentials()
        osf = OSF(**cred)
        proj_id, proj_url = create_project(osf_session=osf.session, title=title)
        yield get_status_dict(action="create-project-osf",
                              type="dataset",
                              url=proj_url,
                              id=proj_id,
                              status="ok"
                              )

        init_opts = ["encryption=none",
                     "type=external",
                     "externaltype=osf",
                     "autoenable=true",
                     "project={}".format(proj_id)]

        ds.repo.init_remote(sibling, options=init_opts)
        # TODO: add special remote name to result?
        #       need to check w/ datalad-siblings conventions
        yield get_status_dict(action="add-sibling-osf",
                              type="dataset",
                              status="ok"
                              )
