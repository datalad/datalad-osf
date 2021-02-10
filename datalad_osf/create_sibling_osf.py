# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See LICENSE file distributed along with the datalad_osf package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##

import logging
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
    EnsureBool,
)
from datalad.interface.results import get_status_dict
from osfclient import OSF
from datalad_osf.utils import (
    create_node,
    update_node,
    get_credentials,
)
from datalad.utils import ensure_list
from datalad.log import log_progress

lgr = logging.getLogger('datalad.osf.create_sibling_osf')


@build_doc
class CreateSiblingOSF(Interface):
    """Create a dataset representation at OSF.

    This will create a node on OSF and initialize
    an osf special remote to point to it. There are two modes
    this can operate in: 'annex' and 'export'.
    The former uses the OSF node as a key-value store, that
    can be used by git-annex to copy data to and retrieve
    data from (potentially by any clone of the original dataset).
    The latter allows to use 'git annex export' to publish a
    snapshot of a particular version of the dataset. Such an OSF
    node will - in opposition to the 'annex' - be
    human-readable.

    For authentication with OSF, you can define environment variables: Either
    'OSF_TOKEN', or both 'OSF_USERNAME' and 'OSF_PASSWORD'. If neither of these
    is defined, the tool will fall back to the datalad credential manager and
    inquire for credentials interactively.

    """

    result_renderer = 'tailored'

    _params_ = dict(
        dataset=Parameter(
            args=("-d", "--dataset"),
            doc="""Dataset to create a sibling for.""",
            constraints=EnsureDataset() | EnsureNone()
        ),
        title=Parameter(
            args=("--title",),
            doc="""title of the to-be created OSF node that is displayed
            on the OSF website. Defaults to the basename of the root directory
            of the local dataset.""",
            constraints=EnsureStr() | EnsureNone(),
        ),
        name=Parameter(
            args=("-s", "--name",),
            doc="""Name of the to-be initialized osf-special-remote""",
            constraints=EnsureStr()
        ),
        storage_name=Parameter(
            args=("--storage-name",),
            metavar="NAME",
            doc="""Name of the storage sibling (git-annex special remote).
            Must not be identical to the sibling name. If not specified,
            defaults to the sibling name plus '-storage' suffix.""",
            constraints=EnsureStr() | EnsureNone()),
        existing=Parameter(
            args=("--existing",),
            constraints=EnsureChoice(
                'skip', 'error') | EnsureNone(),
            metavar='MODE',
            doc="""Action to perform, if a (storage) sibling is already
            configured under the given name and/or a target already exists.
            In this case, a dataset can be skipped ('skip'), or the command
            be instructed to fail ('error').""", ),
        trust_level=Parameter(
            args=("--trust-level",),
            metavar="TRUST-LEVEL",
            constraints=EnsureChoice(
                'trust', 'semitrust', 'untrust') | EnsureNone(),
            doc="""specify a trust level for the storage sibling. If not
            specified, the default git-annex trust level is used.""",),
        mode=Parameter(
            args=("--mode",),
            doc=""" """,
            constraints=EnsureChoice(
                "annex", "export", "exportonly", "gitonly")
        ),
        tags=Parameter(
            args=('--tag',),
            dest='tags',
            metavar='TAG',
            doc="""specific one or more tags for the to-be-create OSF node.
            A tag 'DataLad dataset' and the dataset ID (if there is any)
            will be automatically added as additional tags.
            [CMD: This option can be given more than once CMD].""",
            action='append',
        ),
        public=Parameter(
            args=("--public",),
            doc="""make OSF node public""",
            action='store_true',
        ),
        category=Parameter(
            args=("--category",),
            doc="""specific the OSF node category to be used for the
            node. The categorization determines what icon is displayed
            with the node on the OSF, and helps with search organization""",
            # all presently supported categories
            constraints=EnsureChoice(
                "analysis", "communication", "data", "hypothesis",
                "instrumentation", "methods and measures", "procedure",
                "project", "software", "other")
        ),
        description=Parameter(
            args=("--description",),
            metavar="TEXT",
            doc="""Description of the OSF node that will be displayed on
            the associated project page. By default a description will be
            generated based on the mode the sibling is put into.""",
            constraints=EnsureStr() | EnsureNone()),
    )

    @staticmethod
    @datasetmethod(name='create_sibling_osf')
    @eval_results
    def __call__(title=None,
                 name="osf",
                 storage_name=None,
                 dataset=None,
                 mode="annex",
                 existing='error',
                 trust_level=None,
                 tags=None,
                 public=False,
                 category='data',
                 description=None,
                 ):
        ds = require_dataset(dataset,
                             purpose="create OSF remote",
                             check_installed=True)
        res_kwargs = dict(
            ds=ds,
            action="create-sibling-osf",
            logger=lgr,
        )
        # we need an annex
        if not isinstance(ds.repo, AnnexRepo):
            yield get_status_dict(
                type="dataset",
                status="impossible",
                message="dataset has no annex",
                **res_kwargs)
            return

        # NOTES:
        # - we prob. should check osf-special-remote availability upfront to
        #   fail early
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
        #   -> needs to ne returned by create_node

        if not storage_name:
            storage_name = "{}-storage".format(name)

        sibling_conflicts = sibling_exists(
            ds, [name, storage_name],
            # TODO pass through
            recursive=False, recursion_limit=None,
            # fail fast, if error is desired
            exhaustive=existing == 'error',
        )
        if existing == 'error' and sibling_conflicts:
            # we only asked for one
            conflict = sibling_conflicts[0]
            yield get_status_dict(
                status='error',
                message=(
                    "a sibling '%s' is already configured in dataset %s",
                    conflict[1], conflict[0]),
                **res_kwargs,
            )
            return

        if title is None:
            # use dataset root basename
            title = ds.pathobj.name

        tags = ensure_list(tags)
        if 'DataLad dataset' not in tags:
            tags.append('DataLad dataset')
        if ds.id and ds.id not in tags:
            tags.append(ds.id)

        if not description:
            description = \
                "This component was built from a DataLad dataset using the " \
                "datalad-osf extension " \
                "(https://github.com/datalad/datalad-osf)."
            if mode != 'exportonly':
                description += \
                    " With this extension installed, this component can be " \
                    "git or datalad cloned from a 'osf://ID' URL, where " \
                    "'ID' is the OSF node ID that shown in the OSF HTTP " \
                    "URL, e.g. https://osf.io/q8xnk can be cloned from " \
                    "osf://q8xnk. "
        cred = get_credentials(allow_interactive=True)
        osf = OSF(**cred)
        node_id, node_url = create_node(
            osf_session=osf.session,
            title=title,
            category=category,
            tags=tags if tags else None,
            public=EnsureBool()(public),
            description=description,
        )
        if mode != 'gitonly':
            init_opts = ["encryption=none",
                         "type=external",
                         "externaltype=osf",
                         "autoenable=true",
                         "node={}".format(node_id)]

            if mode in ("export", "exportonly"):
                init_opts += ["exporttree=yes"]

            ds.repo.init_remote(storage_name, options=init_opts)
            if trust_level:
                ds.repo.call_git(['annex', trust_level, storage_name])

            yield get_status_dict(
                type="dataset",
                url=node_url,
                id=node_id,
                name=storage_name,
                status="ok",
                **res_kwargs
            )

        if mode == 'exportonly':
            return

        # append how to clone this specific dataset to the description
        description += "This particular project can be cloned using" \
                       " 'datalad clone osf://{}'".format(node_id)
        update_node(osf_session=osf.session,
                    id_=node_id,
                    description=description)

        ds.config.set(
            'remote.{}.annex-ignore'.format(name), 'true',
            where='local')
        yield from ds.siblings(
            # use configure, not add, to not trip over the config that
            # we just made
            action='configure',
            name=name,
            url='osf://{}'.format(node_id),
            fetch=False,
            publish_depends=storage_name if mode != 'gitonly' else None,
            recursive=False,
            result_renderer=None,
        )

    @staticmethod
    def custom_result_renderer(res, **kwargs):
        from datalad.ui import ui
        if res['action'] == "create-sibling-osf":
            msg = res.get('message', None)
            ui.message("{action}({status}): {url}{msg}".format(
                action=ac.color_word(res['action'], ac.BOLD),
                status=ac.color_status(res['status']),
                url=res.get('url', ''),
                msg=' [{}]'.format(msg[0] % msg[1:]
                                   if isinstance(msg, tuple)
                                   else res['message'])
                if msg else '')
            )
        elif res['action'] == "add-sibling-osf":
            ui.message("{action}({status})".format(
                action=ac.color_word(res['action'], ac.BOLD),
                status=ac.color_status(res['status']))
            )
        else:
            from datalad.interface.utils import default_result_renderer
            default_result_renderer(res)


# TODO this could was originally taken from create_sibling_ria() and
# subsequently turned into a standalone function to facilitate re-use by other
# `create_sibling()` implementations
def sibling_exists(ds, names, recursive=False,
                   recursion_limit=None, exhaustive=False):
    # in recursive mode this check could take a substantial amount of
    # time: employ a progress bar (or rather a counter, because we don't
    # know the total in advance
    pbar_id = 'sibling-exists-{}'.format(id(ds))
    if recursive:
        log_progress(
            lgr.info, pbar_id,
            'Start checking pre-existing sibling configuration %s', ds,
            label='Query siblings',
            unit=' Siblings',
        )
    conflicts = []
    for r in ds.siblings(result_renderer=None,
                         recursive=recursive,
                         recursion_limit=recursion_limit):
        if recursive:
            log_progress(
                lgr.info, pbar_id,
                'Discovered sibling %s in dataset at %s',
                r['name'], r['path'],
                update=1,
                increment=True)
        if not r['type'] == 'sibling' or r['status'] != 'ok':
            # this is an internal status query that has no consequences
            continue
        for name in names:
            if r['name'] == name:
                conflicts.append((r['path'], name))
                if not exhaustive:
                    return conflicts
    if recursive:
        log_progress(
            lgr.info, pbar_id,
            'Finished checking pre-existing sibling configuration %s', ds,
        )
    return conflicts
