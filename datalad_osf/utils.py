# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See LICENSE file distributed along with the datalad_osf package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##

import json
from os import environ
from datalad.downloaders.credentials import (
    Token,
    UserPassword,
)
from datalad import ui


# Note: This should ultimately go into osfclient
def create_node(osf_session, title, category="data", tags=None,
                public=False, parent=None, description=None):
    """ Create a node on OSF

    Parameters
    ----------
    title: str
        Title of the node
    category: str
        categorization changes how the node is displayed
        on OSF, but doesn't appear to have a "real" function
    tags: list of str
    public: bool
        whether to make the new node public
    parent: str, optional
        ID of an OSF parent node to create a child node for

    Returns
    -------
    str
        ID of the created node
    """

    if parent:
        # we have a parent, use its URL to create children
        url = osf_session.build_url('nodes', parent, 'children')
    else:
        url = osf_session.build_url('nodes')
    post_data = {"data":
                     {"type": "nodes",
                      "attributes":
                          {"title": title,
                           "category": category,
                           "public": public,
                           }
                      }
                 }
    if tags:
        post_data["data"]["attributes"]["tags"] = tags
    if description:
        post_data["data"]["attributes"]["description"] = description

    response = osf_session.post(url, data=json.dumps(post_data))
    # TODO: figure what errors to better deal with /
    #       create a better message from
    response.raise_for_status()

    # TODO: This should eventually return an `node` instance (see osfclient).
    #       Response contains all properties of the created node.
    node_id = response.json()['data']['id']

    # Note: Going for "html" URL here for reporting back to the user, since this
    #       what they would need to go to in order to proceed manually.
    #       There's also the flavor "self" instead, which is the node's
    #       API endpoint.
    proj_url = response.json()["data"]["links"]["html"]
    return node_id, proj_url


def update_node(osf_session, id_, category=None, tags=None, description=None):
    """Updates a node on the osf

    id_: str
        to be updated node ID
    """
    url = osf_session.build_url('nodes', id_)
    patch_data = {"data":
                     {"type": "nodes",
                      "id": id_,
                      "attributes":
                          {}
                      }
                 }
    if category:
        patch_data["data"]["attributes"]["category"] = category
    if tags:
        patch_data["data"]["attributes"]["tags"] = tags
    if description:
        patch_data["data"]["attributes"]["description"] = description

    response = osf_session.patch(url, data=json.dumps(patch_data))
    response.raise_for_status()


def delete_node(osf_session, id_):
    """ Delete a node on OSF

    Parameters
    ----------
    id_: str
        to be deleted node ID
    """

    url = osf_session.build_url('nodes', id_)
    response = osf_session.delete(url)
    response.raise_for_status()


def initialize_osf_remote(remote, node,
                          encryption="none", autoenable="true"):
    """Initialize special remote with a given node

    convenience wrapper for git-annex-initremote w/o datalad

    Parameters
    ----------
    remote: str
        name for the special remote
    node: str
        ID of the node/component to use
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
                 "node={}".format(node)]

    import subprocess
    subprocess.run(["git", "annex", "initremote", remote] + init_opts)


def get_credentials(allow_interactive=True):
    # prefer the environment
    if 'OSF_TOKEN' in environ or all(
            k in environ for k in ('OSF_USERNAME', 'OSF_PASSWORD')):
        return dict(
            token=environ.get('OSF_TOKEN', None),
            username=environ.get('OSF_USERNAME', None),
            password=environ.get('OSF_PASSWORD', None),
        )

    # fall back on DataLad credential manager
    token_auth = Token(
        name='https://osf.io',
        url='https://osf.io/settings/tokens',
    )
    up_auth = UserPassword(
        name='https://osf.io',
        url='https://osf.io/settings/account',
    )

    do_interactive = allow_interactive and ui.is_interactive()

    # get auth token, from environment, or from datalad credential store
    # if known-- we do not support first-time entry during a test run
    token = environ.get(
        'OSF_TOKEN',
        token_auth().get('token', None)
        if do_interactive or token_auth.is_known
        else None)
    username = None
    password = None
    if not token:
        # now same for user/password if there was no token
        username = environ.get(
            'OSF_USERNAME',
            up_auth().get('user', None)
            if do_interactive or up_auth.is_known
            else None)
        password = environ.get(
            'OSF_PASSWORD',
            up_auth().get('password', None)
            if do_interactive or up_auth.is_known
            else None)

    return dict(token=token, username=username, password=password)
