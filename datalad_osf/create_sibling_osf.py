from os import environ
from datalad.interface.base import Interface
from datalad.interface.base import build_doc
from datalad.interface.utils import ac
from datalad.support.annexrepo import AnnexRepo
from datalad.support.param import Parameter
from datalad.distribution.dataset import (
    datasetmethod,
    EnsureDataset,
    require_dataset
)
from datalad.interface.utils import eval_results
from datalad.support.constraints import (
    EnsureChoice,
    EnsureNone,
    EnsureStr,
)
from datalad.interface.results import get_status_dict
from datalad_osf.osfclient.osfclient import OSF
from datalad_osf.utils import create_project
from datalad.downloaders.credentials import (
    Token,
    UserPassword,
)


def _get_credentials():
    """helper to read credentials

    for now go w/ env vars. can be refactored
    to read from datalad configs, credential store, etc.
    """
    # check if anything need to be done still
    if 'OSF_TOKEN' in environ or all(
            k in environ for k in ('OSF_USERNAME', 'OSF_PASSWORD')):
        return dict(
            token=environ.get('OSF_TOKEN', None),
            username=environ.get('OSF_USERNAME', None),
            password=environ.get('OSF_USERNAME', None),
        )

    token_auth = Token(name='https://osf.io', url=None)
    up_auth = UserPassword(name='https://osf.io', url=None)

    # get auth token, form environment, or from datalad credential store
    # if known-- we do not support first-time entry during a test run
    token = environ.get(
        'OSF_TOKEN',
        token_auth().get('token', None) if token_auth.is_known else None)
    username = None
    password = None
    if not token:
        # now same for user/password if there was no token
        username = environ.get(
            'OSF_USERNAME',
            up_auth().get('user', None) if up_auth.is_known else None)
        password = environ.get(
            'OSF_PASSWORD',
            up_auth().get('password', None) if up_auth.is_known else None)

    # place into environment, for now this is the only way the special remote
    # can be supplied with credentials
    for k, v in (('OSF_TOKEN', token),
                 ('OSF_USERNAME', username),
                 ('OSF_PASSWORD', password)):
        if v:
            environ[k] = v
    return dict(token=token, username=username, password=password)


@build_doc
class CreateSiblingOSF(Interface):
    """Create a dataset representation at OSF

    This will create a project on OSF and initialize
    an osf special remote to point to it. There are two modes
    this can operate in: 'annexstore' and 'exporttree'.
    The former uses the OSF project as a key-value store, that
    can be used to by git-annex to copy data to and retrieve
    data from (potentially by any clone of the original dataset).
    The latter allows to use 'git annex export' to publish a
    snapshot of a particular version of the dataset. Such an OSF
    project will - in opposition to the 'annexstore' - be
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
        sibling=Parameter(
            args=("-s", "--name",),
            doc="""name of the to-be initialized osf-special-remote""",
            constraints=EnsureStr()
        ),
        mode=Parameter(
            args=("--mode",),
            doc=""" """,
            constraints=EnsureChoice("annexstore", "exporttree")
        )
    )

    @staticmethod
    @datasetmethod(name='create_sibling_osf')
    @eval_results
    def __call__(title, sibling="osf", dataset=None, mode="annexstore"):
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

        if mode == "exporttree":
            init_opts += ["exporttree=yes"]

        ds.repo.init_remote(sibling, options=init_opts)
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
