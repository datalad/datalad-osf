from os import environ
from datalad.utils import (
    optional_args,
    wraps
)
from datalad_osf.utils import (
    create_project,
    delete_project,
)
from datalad_osf.osfclient.osfclient import OSF


@optional_args
def with_project(f, osf_session=None, title=None, category="project"):

    # TODO: token auth!
    osf = OSF(username=environ['OSF_USERNAME'],
              password=environ['OSF_PASSWORD'])

    @wraps(f)
    def new_func(*args, **kwargs):
        proj_id, proj_url = create_project(
            osf.session, title, category=category)
        try:
            return f(*(args + (proj_id,)), **kwargs)
        finally:
            delete_project(osf.session, proj_id)

    return new_func
