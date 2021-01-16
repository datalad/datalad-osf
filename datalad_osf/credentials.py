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
from datalad.dochelpers import exc_str
from datalad.support.param import Parameter
from datalad.distribution.dataset import (
    datasetmethod,
    EnsureDataset,
)
from datalad.interface.utils import (
    eval_results,
)
from datalad.support.constraints import (
    EnsureChoice,
    EnsureNone,
)
from datalad.downloaders.credentials import (
    Token,
    UserPassword,
)
from osfclient import OSF
from osfclient.exceptions import UnauthorizedException


@build_doc
class OSFCredentials(Interface):
    """Gather OSF credentials for subsequent non-interactive use

    This command enables (re-)entry of OSF credentials for storage in
    a credential manager. Once credentials are known, they will be
    retrieved automatically on demand, and enable non-interactive use
    for the purpose of data transfer to and from OSF.

    Credentials will be verified to enable successful authentication
    before being stored.
    """
    _params_ = dict(
        method=Parameter(
            args=("--method",),
            doc="""authentication method to use. 'token' authentication is
            strongly recommended.""",
            constraints=EnsureChoice("token", "userpassword")
        ),
        reset=Parameter(
            args=("--reset",),
            doc="""reset existing credentials and force re-entry""",
            action='store_true',
        ),
    )

    @staticmethod
    @datasetmethod(name='osf_credentials')
    @eval_results
    def __call__(method="token", reset=False):
        auth = None
        cred_spec = []
        if method == 'token':
            cred_spec = dict(token='token')
            auth = Token(
                name='https://osf.io',
                url='https://osf.io/settings/tokens',
            )
        elif method == 'userpassword':
            cred_spec = dict(user='username', password='password')
            auth = UserPassword(
                name='https://osf.io',
                url='https://osf.io/settings/account',
            )
        else:
            raise ValueError(
                'Unknown authentication method: {}'.format(method))
        if reset and auth.is_known:
            auth.delete()
        cred = {v: auth().get(k, None) for k, v in cred_spec.items()}

        # now verify that the credentials work by querying the
        # logged in user
        osf = OSF(**cred)
        try:
            req = osf.session.get('https://api.osf.io/v2/users/me/')
            req.raise_for_status()
        except UnauthorizedException:
            auth.delete()
            yield dict(
                action='osf_credentials',
                status='error',
                message='Invalid credentials',
                path=None,
            )
            return
        except Exception as e:
            yield dict(
                action='osf_credentials',
                status='impossible',
                message='Could not verify credentials, '
                        'please try again: {}'.format(
                            exc_str(e)),
                # needed to pacify DataLad 0.13.0 and earlier
                path=None,
            )
            return
        # if we get here auth has worked fine
        # get some attributes for an informative message
        attrs = req.json().get('data', {}).get('attributes', {})
        yield dict(
            action='osf_credentials',
            status='ok',
            message='authenticated{}{}{}'.format(
                ' as '
                if any(attrs.get(k, None) for k in ('email', 'full_name'))
                else '',
                attrs.get('full_name', ''),
                ' <{}>'.format(attrs['email'])
                if attrs.get('email', None)
                else ''),
            # needed to pacify DataLad 0.13.0 and earlier
            path=None,
            # report effective credentials
            **cred,
        )
