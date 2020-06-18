import json


# Note: This should ultimately go into osfclient
def create_project(osf_session, title, category="project", tags=None):
    """ Create a project on OSF

    Parameters
    ----------
    title: str
        Title of the project
    category: str
        categorization changes how the project is displayed
        on OSF, but doesn't appear to have a "real" function
    tags: list of str

    Returns
    -------
    str
        ID of the created project
    """

    url = osf_session.build_url('nodes')
    post_data = {"data":
                     {"type": "nodes",
                      "attributes":
                          {"title": title,
                           "category": category
                           }
                      }
                 }
    if tags:
        post_data["data"]["attributes"]["tags"] = tags

    response = osf_session.post(url, data=json.dumps(post_data))
    # TODO: figure what errors to better deal with /
    #       create a better message from
    response.raise_for_status()

    # TODO: This should eventually return an `Project` instance (see osfclient).
    #       Response contains all properties of the created project.
    node_id = response.json()['data']['id']

    # Note: Going for "html" URL here for reporting back to the user, since this
    #       what they would need to go to in order to proceed manually.
    #       There's also the flavor "self" instead, which is the node's
    #       API endpoint.
    proj_url = response.json()["data"]["links"]["html"]
    return node_id, proj_url


def delete_project(osf_session, project):
    """ Delete a project on OSF

    Parameters
    ----------
    project: str
        to be deleted node ID
    """

    url = osf_session.build_url('nodes', project)
    response = osf_session.delete(url)
    response.raise_for_status()


def initialize_osf_remote(remote, project,
                          encryption="none", autoenable="true"):
    """Initialize special remote with a given project

    convenience wrapper for git-annex-initremote w/o datalad

    Parameters
    ----------
    remote: str
        name for the special remote
    project: str
        ID of the project/component to use
    encryption: str
        see git-annex-initremote; mandatory option;
    autoenable: str
        'true' or 'false'; tells git-annex to automatically enable the
        special remote on git-annex-init (particularly after a fresh git-clone
    """

    init_opts = ["type=external",
                 "externaltype=osf",
                 "encryption={}".format(encryption),
                 "autoenable={}".format(autoenable),
                 "project={}".format(project)]

    import subprocess
    subprocess.run(["git", "annex", "initremote", remote] + init_opts)
