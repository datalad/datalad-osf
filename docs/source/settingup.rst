Setting up
==========

Requirements
------------

- DataLad

Before being able to use the extension, you need to have DataLad installed, which relies on `git-annex <git-annex.branchable.com/>`_, `Git <git-scm.com/>`_ and Python. If you don't have DataLad installed yet, please follow the instructions `here <http://handbook.datalad.org/en/latest/intro/installation.html>`_.


- An account on the OSF

You need an OSF account to be able to interact with it. If you don't have an account yet, `register here <https://osf.io/register>`_.

- An account on repository-hosting accounts

You should consider having an account on one or more repository hosting sites such as `GitHub <https://github.com/join?ref_cta=Sign+up&ref_loc=header+logged+out&ref_page=%2F&source=header-home>`_ , `GitLab <https://gitlab.com/users/sign_up>`_, `Bitbucket <https://bitbucket.org/account/signup/>`_ or similar"


Developer installation
-----------------------

Before you can start using the extension, you have to install it. To do this, open your shell and type:

``pip install -e [--user] git+https://github.com/datalad/datalad-osf#egg=datalad-osf``

Note: once packed up for PyPi and uploaded, use ``pip install datalad-osf``