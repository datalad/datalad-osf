.. include:: ../links.inc

.. _codealong:

Walk-Trough
^^^^^^^^^^^

The upcoming use cases are walk-throughs and meant as code-along tutorials.
If you want, open a terminal and code along to try out each method.
If you have DataLad and ``datalad-osf`` installed, each tutorial will not take more than 5 minutes.

As a general preparation, build an example dataset and configure OSF credentials for reuse in all usecases.
You can execute all following examples in this dataset.

Create an Example Dataset
"""""""""""""""""""""""""

For the sake of this tutorial, let's create a small example DataLad dataset.

.. code-block:: bash

    # collab_osf being the name of your new dataset
    $ datalad create collab_osf


After dataset creation, populate it with some content (just like in the `Datalad Handbook`_):

.. code-block:: bash

    $ cd collab_osf
    # add a PDF file to git-annex
    $ datalad download-url http://www.tldp.org/LDP/Bash-Beginners-Guide/Bash-Beginners-Guide.pdf \
      --dataset . \
      -m "add beginners guide on bash" \
      -O books/bash_guide.pdf

    download_url(ok): /tmp/collab_osf/books/bash_guide.pdf (file)
    add(ok): /tmp/collab_osf/books/bash_guide.pdf (file)
    save(ok): /tmp/collab_osf dataset)
    action summary:
     add (ok: 1)
     download_url (ok: 1)
     save (ok: 1)
    # add a text file to Git
    $ mkdir code
    $ echo "This is just an example file just to show the different ways of saving data in a DataLad dataset." > code/example.txt
    $ datalad save --to-git -m "created an example.txt"
    add(ok): /tmp/collab_osf/code/example.txt (file)
    save(ok): /tmp/collab_osf(dataset)
    action summary:
      add (ok: 1)
      save (ok: 1)


Authenticate
""""""""""""

First, if you haven't done so yet, configure either your OSF credentials (username and password) or an OSF access token, either as environment variables, or using ``datalad osf-credentials``.
Below, we use an OSF access token:

.. code-block:: bash

   $ datalad osf-credentials
   You need to authenticate with 'https://osf.io' credentials. https://osf.io/settings/tokens provides information on how to gain access
   token: <your token here>
   You need to authenticate with 'https://osf.io' credentials. https://osf.io/settings/tokens provides information on how to gain access
   token (repeat): <your token here>
   osf_credentials(ok): [authenticated as <user> <e-mail>]

More information on authentication is detailed in the section :ref:`authenticate`.
