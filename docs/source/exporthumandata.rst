.. include:: ./links.inc

Export a human-readable dataset to OSF
**************************************

Imagine you have been creating a reproducible workflow using DataLad_ from the
get go. Everything is finished now, code, data, and paper are ready. Last thing
to do: Publish your data.

Using datalad-osf makes this really convenient.

Walk through
------------

Installation
^^^^^^^^^^^^
For installation checkout the installation page of the documentation.

.. toctree::

    settingup.rst


Creating an Example Dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^
We will create a small example DataLad dataset to show the functionality.

.. code-block:: bash

    $ datalad create collab_osf
    # collab_osf being the name of your new dataset
    # In all examples a `$` in front indicates a new line in the Bash-Shell
    # Copying the $ will prevent your code from execution.

After having created the dataset we want to populate it with some content (just
like in the `Datalad Handbook`_):

.. code-block:: bash

    $ cd collab_osf
    $ datalad download-url http://www.tldp.org/LDP/Bash-Beginners-Guide/Bash-Beginners-Guide.pdf \
    --dataset . \
    -m "add beginners guide on bash" \
    -O books/bash_guide.pdf

Setting up the OSF Remote
^^^^^^^^^^^^^^^^^^^^^^^^^

To use OSF as a storage, you first need to provide either your OSF credentials (username and password) or an OSF access token.

If you choose to use your credentials, proceed as follows:

.. code-block:: bash

    export OSF_USERNAME=YOUR_USERNAME_FOR_OSF.IO
    export OSF_PASSWORD=YOUR_PASSWORD_FOR_OSF.IO

In this example, we are going to use an OSF access token instead.
You can create such a token in your account settings (`Personal access token` and then `Create token`).
Make sure to create a `full_write` token to be able to create OSF projects and upload data to OSF.

.. code-block:: bash

    export OSF_TOKEN=YOUR_TOKEN_FROM_OSF.IO

We are now going to use datalad to create a sibling dataset on OSF with name `OSF_PROJECT_NAME`.
This will create a new project called `OSF_PROJECT_NAME` on the OSF account associated with the OSF token in `$OSF_TOKEN`.

Note that the ``-s NAME_OF_REMOTE>`` flag is used to specify how ``git`` internally refers to your OSF project with the name `OSF_PROJECT_NAME`.
It would be completely fine to use `OSF_PROJECT_NAME` also as a value for the ``-s`` flag.

You can later on list your remotes from the command line using the ``git remote -v`` command.

.. code-block:: bash

     $ datalad create-sibling-osf -s NAME_OF_REMOTE OSF_PROJECT_NAME --mode export

After that we can export the current state (the `HEAD`) of our dataset in human readable form to OSF:

.. code-block:: bash

    git annex export HEAD --to NAME_OF_REMOTE
