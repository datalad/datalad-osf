.. include:: ../links.inc
.. _authenticate:

Step 1: Authentication
======================

``datalad-osf`` needs to communicate with the OSF to create and modify projects under an associated  user account.
To enable this, the associated user needs to be authenticated using the :command:`osf-credentials` command.
Therefore, as the very first step, ``datalad osf-credentials`` needs to be ran to authenticate a user.
Unless credentials expire or change, this command needs to be ran only once per user and system.

Setting credentials
^^^^^^^^^^^^^^^^^^^

To set credentials, run ``datalad osf-credentials`` anywhere on your system.
This command prompts for user credentials and stores them in your system's secure credential store for OSF operations.

.. code-block:: bash

   # the default authentication method is token
   $ datalad osf-credentials
   You need to authenticate with 'https://osf.io' credentials. https://osf.io/settings/tokens provides information on how to gain access
   token: <your token here>
   You need to authenticate with 'https://osf.io' credentials. https://osf.io/settings/tokens provides information on how to gain access
   token (repeat): <your token here>
   osf_credentials(ok): [authenticated as <user> <e-mail>]

Two different methods of authentication are supported and can be set with the ``--method`` flag:

- ``token``: A personal access token. This is the recommended authentication type and default.
  Generate a personal access token under your user account at `osf.io/settings/tokens <https://osf.io/settings/tokens>`_. Make sure to create a ``full_write`` token to be able to create OSF projects and upload data to OSF!
- ``userpassword``: Your username and password combination from the OSF_ web interface.

.. code-block:: bash

   # authenticate with user name and password
   $ datalad osf-credentials --method userpassword
   You need to authenticate with 'https://osf.io' credentials. https://osf.io/settings/account provides information on how to gain access
   user: <your e-mail address>

   password: <your password here>
   password (repeat): <your password here>
   osf_credentials(ok): [authenticated as <user name>]

The credentials are stored within a system's `encrypted keyring <https://en.wikipedia.org/wiki/GNOME_Keyring>`_ and DataLad_ retrieves them automatically for all future interactions with the OSF.
Information on which user's credentials are stored can be found by re-running ``datalad osf-credentials``.

.. code-block:: bash

   $ datalad osf-credentials
   osf_credentials(ok): [authenticated as <user name> <e-mail>]

.. admonition:: Environment variables

   Alternatively, credentials can be set via environment variables:
   ``OSF_TOKEN``, or both ``OSF_USERNAME`` and ``OSF_PASSWORD``, as in

   .. code-block:: bash

      export OSF_TOKEN=YOUR_TOKEN_FROM_OSF


Resetting credentials
^^^^^^^^^^^^^^^^^^^^^

If credentials change they can be re-set using the ``--reset`` flag:

.. code-block:: bash

   # token method is used by default, use --method userpassword for user + password credentials
   $ datalad osf-credentials --reset
   You need to authenticate with 'https://osf.io' credentials. https://osf.io/settings/tokens provides information on how to gain access
   token: <your token here>
   You need to authenticate with 'https://osf.io' credentials. https://osf.io/settings/tokens provides information on how to gain access
   token (repeat): <your token here>
   osf_credentials(ok): [authenticated as <user name> <e-mail>]


Invalid credentials
^^^^^^^^^^^^^^^^^^^

If you supply invalid credentials such as a mismatching user name and password combination or a wrong token, you will see the following error::

   $ osf_credentials(error): None [Invalid credentials]

Please check for spelling mistakes, check your user name and password combination under your user account, or regenerate a token, and reset your credentials to fix this.
