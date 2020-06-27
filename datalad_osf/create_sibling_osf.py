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
from datalad.utils import ensure_list


@build_doc
class CreateSiblingOSF(Interface):
    """Create a dataset representation at OSF.

    This will create a project on OSF and initialize
    an osf special remote to point to it. There are two modes
    this can operate in: 'annex' and 'export'.
    The former uses the OSF project as a key-value store, that
    can be used by git-annex to copy data to and retrieve
    data from (potentially by any clone of the original dataset).
    The latter allows to use 'git annex export' to publish a
    snapshot of a particular version of the dataset. Such an OSF
    project will - in opposition to the 'annex' - be
    human-readable.

    For authentification with OSF, you can define environment variables: Either
    'OSF_TOKEN', or both 'OSF_USERNAME' and 'OSF_PASSWORD'. If neither of these
    is defined, the tool will fall back to the datalad credential manager and
    inquire for credentials interactively.

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
            args=("--title",),
            doc="""title of the to-be created OSF project that is displayed
            on the OSF website. Defaults to '<name> [DataLad::<id>]',
            where <name> is the basename of the root directory of the local
            dataset and <id> is the DataLad dataset ID.""",
            constraints=EnsureStr() | EnsureNone(),
        ),
        name=Parameter(
            args=("-s", "--name",),
            doc="""Name of the to-be initialized osf-special-remote""",
            constraints=EnsureStr()
        ),
        mode=Parameter(
            args=("--mode",),
            doc=""" """,
            constraints=EnsureChoice("annex", "export")
        ),
        tags=Parameter(
            args=('--tag',),
            dest='tags',
            metavar='TAG',
            doc="""specific one or more tags for the to-be-create OSF project.
            A tag 'DataLad dataset' and the dataset ID (if there is any)
            will be automatically added as additional tags.
            [CMD: This option can be given more than once CMD].""",
            action='append',
        ),
    )

    @staticmethod
    @datasetmethod(name='create_sibling_osf')
    @eval_results
    def __call__(title=None, name="osf", dataset=None, mode="annex",
                 tags=None):
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

        if title is None:
            # build a default title that is somewhat human-readable
            # (include root directory name), but also useful for
            # machine discovery (includes unique dataset ID)
            title = '{name}{id}'.format(
                # TODO query for metadata for a name, eventually
                name=ds.pathobj.name,
                id=' [DataLad::{}]'.format(ds.id) if ds.id else '',
            )

        tags = ensure_list(tags)
        if 'DataLad dataset' not in tags:
            tags.append('DataLad dataset')
        if ds.id and ds.id not in tags:
            tags.append(ds.id)

        cred = get_credentials(allow_interactive=True)
        osf = OSF(**cred)
        proj_id, proj_url = create_project(
            osf_session=osf.session,
            title=title,
            tags=tags if tags else None,
        )
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
