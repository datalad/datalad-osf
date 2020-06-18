from datalad.utils import (
    optional_args,
    wraps
)
from datalad_osf.utils import (
    create_project,
    delete_project,
)


@optional_args
def with_project(f, title=None, category="project"):

    @wraps(f)
    def new_func(*args, **kwargs):
        proj_id, proj_url = create_project(title, category=category)
        try:
            return f(*(args + (proj_id,)), **kwargs)
        finally:
            delete_project(proj_id)

    return new_func
