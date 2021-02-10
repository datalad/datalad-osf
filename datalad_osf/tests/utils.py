# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See LICENSE file distributed along with the datalad_osf package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##

from datalad.utils import (
    optional_args,
    wraps
)
from datalad_osf.utils import (
    create_node,
    delete_node,
    get_credentials,
)
from osfclient import OSF


@optional_args
def with_node(f, osf_session=None, title=None, category="data"):
    # we don't want the test hanging, no interaction
    creds = get_credentials(allow_interactive=False)
    # supply all credentials, so osfclient can fall back on user/pass
    # if needed
    osf = OSF(**creds)

    @wraps(f)
    def new_func(*args, **kwargs):
        node_id, proj_url = create_node(
            osf.session,
            'Temporary DataLad CI project: {}'.format(title),
            category=category)
        try:
            return f(*(args + (node_id,)), **kwargs)
        finally:
            delete_node(osf.session, node_id)

    return new_func
