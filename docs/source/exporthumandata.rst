Export a human-readable dataset to OSF
**************************************

Imagine you have been creating a reproducible workflow using DataLad from the
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
We will create a small example DataLad Dataset to show the functionality. 

.. code-block:: bash

    $ datalad create collab_osf
    # collab_osf being the name of your new dataset
    # In all examples a `$` in front indicates a new line in the Bash-Shell
    # Copying the $ will prevent your code from execution. 

After having created the dataset we want to populate it with some content (just
like in the Handbook):

.. code-block:: bash

    $ cd collab_osf
    $ datalad download-url http://www.tldp.org/LDP/Bash-Beginners-Guide/Bash-Beginners-Guide.pdf \
    --dataset . \
    -m "add beginners guide on bash" \
    -O books/bash_guide.pdf

Setting up the OSF Remote
^^^^^^^^^^^^^^^^^^^^^^^^^

To use OSF as a storage, you need to provide either your OSF credentials or an OSF access token.
You can create such a token in your account settings (`Personal access token` and then `Create token`), make sure to create a `full_write` token to be able to create OSF projects and upload data to OSF. 

.. code-block:: bash

    export OSF_TOKEN=YOUR_TOKEN_FROM_OSF.IO

Now we set up an OSF remote called `YOUR_OSF_REMOTE_NAME` that points to the osf.io URL `YOUR_OSF_PROJECT_URL`. If you instead put a name here, the OSF project will automatically 
be created. 

.. code-block:: bash

     $ datalad create-sibling-osf YOUR_OSF_PROJECT_URL YOUR_OSF_REMOTE_NAME --mode exporttree             

After that we can export the current state (the `HEAD`) of our dataset in human readable form to OSF:

.. code-block:: bash

    git annex export HEAD --to YOUR_OSF_REMOTE_NAME

.. _OSF: https://www.osf.io/
.. _Github: https://www.github.com/
