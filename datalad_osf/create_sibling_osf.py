# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See LICENSE file distributed along with the datalad_osf package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##

from datalad.interface.base import (
    Interface,
    build_doc,
)
from datalad.support.annexrepo import AnnexRepo
from datalad.support.param import Parameter
from datalad.distribution.dataset import (
    datasetmethod,
    EnsureDataset,
    require_dataset
)
from datalad.interface.utils import (
    ac,
    eval_results,
)
from datalad.support.constraints import (
    EnsureChoice,
    EnsureNone,
    EnsureStr,
)
from datalad.interface.results import get_status_dict
from datalad_osf.osfclient.osfclient import OSF
from datalad_osf.utils import (
    create_project,
    get_credentials,
)


@build_doc
class CreateSiblingOSF(Interface):
    """Create a dataset representation at OSF

    This will create a project on OSF and initialize
    an osf special remote to point to it. There are two modes
    this can operate in: 'annex' and 'export'.
    The former uses the OSF project as a key-value store, that
    can be used to by git-annex to copy data to and retrieve
    data from (potentially by any clone of the original dataset).
    The latter allows to use 'git annex export' to publish a
    snapshot of a particular version of the dataset. Such an OSF
    project will - in opposition to the 'annex' - be
    human-readable.
    """

    result_renderer = 'tailored'

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
            doc="""Title of the to-be created OSF project.""",
            constraints=EnsureStr()
        ),
        name=Parameter(
            args=("-s", "--name",),
            doc="""name of the to-be initialized osf-special-remote""",
            constraints=EnsureStr()
        ),
        mode=Parameter(
            args=("--mode",),
            doc=""" """,
            constraints=EnsureChoice("annex", "export")
        )
    )

    @staticmethod
    @datasetmethod(name='create_sibling_osf')
    @eval_results
    def __call__(title, name="osf", dataset=None, mode="annex"):
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

        cred = get_credentials(allow_interactive=True)
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

        if mode == "export":
            init_opts += ["exporttree=yes"]

        ds.repo.init_remote(name, options=init_opts)
        # TODO: add special remote name to result?
        #       need to check w/ datalad-siblings conventions
        yield get_status_dict(action="add-sibling-osf",
                              type="dataset",
                              status="ok"
                              )

    @staticmethod
    def custom_result_renderer(res, **kwargs):
        from datalad.ui import ui
        status_str = "{action}({status}): "
        if res['action'] == "create-project-osf":
            ui.message("{action}({status}): {url}".format(
                action=ac.color_word(res['action'], ac.BOLD),
                status=ac.color_status(res['status']),
                url=res['url'])
            )
        elif res['action'] == "add-sibling-osf":
            ui.message("{action}({status})".format(
                action=ac.color_word(res['action'], ac.BOLD),
                status=ac.color_status(res['status']))
            )
        else:
            from datalad.interface.utils import default_result_renderer
            default_result_renderer(res, **kwargs)
