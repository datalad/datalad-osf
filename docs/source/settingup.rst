.. include:: ./links.inc

.. _install:

Quickstart
==========

Requirements
^^^^^^^^^^^^

DataLad and ``datalad-osf`` are available for all major operating systems (Linux, MacOS, Windows 10 [#f1]_).
The relevant requirements are listed below.

   An OSF_ account
       You need an OSF account to be able to interact with it. If you don't have an account yet, `register here <https://osf.io/register>`_ -- its free!

   DataLad
       If you don't have DataLad_ and its underlying tools (`git`_, `git-annex`_) installed yet, please follow the instructions from `the datalad handbook <http://handbook.datalad.org/en/latest/intro/installation.html>`_.

   [optional] An account on a Git repository hosting site
       You should consider having an account on one or more repository hosting sites such as `GitHub <https://github.com/join>`__ , `GitLab <https://gitlab.com/users/sign_up>`_, `Bitbucket <https://bitbucket.org/account/signup/>`_ or similar.

Installation
^^^^^^^^^^^^

``datalad-osf`` is a Python package available on `pypi <https://pypi.org/project/datalad-osf/>`_ and installable via pip_.

.. code-block:: bash

   # create and enter a new virtual environment (optional)
   $ virtualenv --python=python3 ~/env/dl-osf
   $ . ~/env/dl-osf/bin/activate
   # install from PyPi
   $ pip install datalad-osf.

Getting started
^^^^^^^^^^^^^^^

Here's the gist of some of this extension's functionality.
Checkout the :ref:`Tutorial` for more detailed demonstrations.

First, :ref:`provide your credentials <authenticate>`:

.. code-block:: bash

   # provide your OSF credentials, ideally as a token:
   $ datalad osf-credentials
   You need to authenticate with 'https://osf.io' credentials. https://osf.io/settings/tokens provides information on how to gain access
   token: <your token here>
   You need to authenticate with 'https://osf.io' credentials. https://osf.io/settings/tokens provides information on how to gain access
   token (repeat): <your token here>
   osf_credentials(ok): [authenticated as <user> <e-mail>]

Next, create a sibling on the OSF for a DataLad dataset of your choice.
Choose between different sibling modes to adjust how much of your dataset can be published and how it will be displayed, adjust whether your project should be private or public, attach additional meta data, or configure local sibling properties.
The minimal example below will create a new (private) project with minimal metadata on the OSF and apply the necessary configurations to publish your complete dataset to it.

.. code-block:: bash

   # inside of a DataLad dataset
   $ datalad create-sibling-osf --title best-study-ever -s osf
   create-sibling-osf(ok): https://osf.io/czgpf/
   [INFO   ] Configure additional publication dependency on "osf-storage"
   configure-sibling(ok): /home/me/mydataset (sibling)

Afterwards, publish your dataset to the OSF sibling project to share it or collaborate with others:

.. code-block:: bash

   $ datalad push --to osf

Finally, you or others can clone it using its project ID.
All annexed data in this dataset will be available via ``datalad get``.

.. code-block:: bash

   $ datalad clone osf://czgpf/

Curious to find out more?
Read on in the :ref:`tutorial` for more functionality and use cases.


.. admonition:: HELP! I'm new to this!

   If this is your reaction to reading the words DataLad dataset, sibling, or dataset publishing,  please head over to the `DataLad Handbook`_ for an introduction to DataLad.

   .. image:: ./_static/clueless.gif

.. rubric:: Footnotes

.. [#f1] While installable for Windows 10, the extension may not be able to perform all functionality documented here. Please get in touch if you are familiar with Windows `to help us fix bugs <https://github.com/datalad/datalad-osf/issues?q=is%3Aissue+is%3Aopen+windows>`_.
