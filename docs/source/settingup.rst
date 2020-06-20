Setting up
==========

Requirements
------------

- DataLad

Before being able to use the extension, you need to have DataLad installed, which relies on `git-annex <git-annex.branchable.com/>`_, `git <git-scm.com/>`_ and `Python <https://www.python.org/>`_.
If you don't have DataLad installed yet, please follow the instructions from `the datalad handbook <http://handbook.datalad.org/en/latest/intro/installation.html>`_.

- An account on the OSF

You need an OSF account to be able to interact with it. If you don't have an account yet, `register here <https://osf.io/register>`_.

- An account on a git repository hosting site

You should consider having an account on one or more repository hosting sites such as `GitHub <https://github.com/join>`_ , `GitLab <https://gitlab.com/users/sign_up>`_, `Bitbucket <https://bitbucket.org/account/signup/>`_ or similar"

Installation
------------

Before you can start using the extension, you have to install it.

``datalad-osf`` is a package on `pypi <https://pypi.org/project/datalad-osf/>`_, so you can open your shell and type: ``pip install datalad-osf``.

If you want to use the most recent development version, use the following command instead: ``pip install -e git+https://github.com/datalad/datalad-osf#egg=datalad-osf``
