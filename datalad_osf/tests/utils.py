from os import environ
from datalad.utils import (
    optional_args,
    wraps
)
from datalad_osf.utils import (
    create_project,
    delete_project,
)
from datalad.downloaders.credentials import (
    Token,
    UserPassword,
)
from datalad_osf.osfclient.osfclient import OSF


def setup_credentials():
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


@optional_args
def with_project(f, osf_session=None, title=None, category="project"):
    creds = setup_credentials()
    # supply all credentials, so osfclient can fall back on user/pass
    # if needed
    osf = OSF(**creds)

    @wraps(f)
    def new_func(*args, **kwargs):
        proj_id, proj_url = create_project(
            osf.session, title, category=category)
        try:
            return f(*(args + (proj_id,)), **kwargs)
        finally:
            delete_project(osf.session, proj_id)

    return new_func
