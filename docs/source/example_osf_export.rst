Use cases
*********

Use Case: Exporting a dataset to OSF
====================================

After we finished working on our project, we want to export everything to OSF, with a human readable file structure that makes it easy for others to discover what we did.

Walk through
------------

Installation
^^^^^^^^^^^^
For installation checkout the installation page of the documentation.  

.. toctree::

    settingup.rst


Creating an Example Dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^

As a very first step you want to set up a DataLad Dataset. For this you should
run. In all examples a `$` in front indicates a new line in the Bash-Shell,
copying it will prevent your code from execution.

.. code-block:: bash

    $ datalad create collab_osf

After having created the dataset we want to populate it with some content (just
like in the Handbook).

.. code-block:: bash

    $ cd collab_osf
    $ datalad download-url http://www.tldp.org/LDP/Bash-Beginners-Guide/Bash-Beginners-Guide.pdf \
    --dataset . \
    -m "add beginners guide on bash" \
    -O books/bash_guide.pdf

Setting up the OSF Remote
^^^^^^^^^^^^^^^^^^^^^^^^^

To use OSF as a storage, you need to provide either your OSF credentials or an OSF access token.
You can create such a token in your account settings, make sure to create a `full_write` token to be able to create OSF projects and upload data to OSF. 

.. code-block:: bash

    export OSF_TOKEN=YOUR_TOKEN_FROM_OSF.IO

Now we set up an OSF remote called `YOUR_OST_REMOTE_NAME` that points to the osf.io URL `YOUR_OSF_PROJECT_URL`.

.. code-block:: bash

    git annex initremote YOUR_OSF_REMOTE_NAME type=external externaltype=osf encryption=none project=YOUR_OSF_PROJECT_URL exporttree=yes

After that we can export the current state (the `HEAD`) of our dataset in human readable form to OSF:

.. code-block:: bash

    git annex export HEAD --to YOUR_OSF_REMOTE_NAME

.. _OSF: https://www.osf.io/
.. _Github: https://www.github.com/
