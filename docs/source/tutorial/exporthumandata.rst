.. include:: ../links.inc
.. _export:

Use case 2: Export a human-readable dataset to OSF
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



.. admonition:: Problem statement

    Imagine you have been collecting data and want to share it with others.
    All your colleagues have only sparse experience with the command line, but are frequent OSF users.
    Therefore, you place all data in a dataset and export the latest version of your data to the OSF in a human readable way, for others to view it conveniently in the web interface.

    As you want a human-readable representation and decide to not share the version history, but only the most recent state of the data, you pick the ``exportonly`` sibling mode.


Creating the OSF sibling
""""""""""""""""""""""""

Given OSF credentials are set, we can create a sibling in ``export-only`` mode.
We will also make the project public (``--public``), and attach a custom description (``--description``) to it.

The code below will create a new public OSF project called ``best-data-ever``, a dataset sibling called ``osf-exportonly-storage``. This sibling is a sole storage sibling -- in technical terms, a git-annex_ `special remote`_. It will not contain version history, but all your dataset's files.

.. code-block:: bash

   # inside of the tutorial DataLad dataset
   $ datalad create-sibling-osf --title best-data-ever \
     --mode exportonly \
     -s osf-export \
     --description "This carefully acquired data will bring science forward" \
     --public

   create-sibling-osf(ok): https://osf.io/<id>/
   # note that the sibling name as an appended "storage" suffix!
   $ datalad siblings
    .: here(+) [git]
    .: osf-annex(-) [osf://n6bgd (git)]
    .: osf-export-storage(+) [osf]          # created in this example
    .: osf-annex-storage(+) [osf]


Publishing the dataset
""""""""""""""""""""""

To publish the current state (the ``HEAD``) of the dataset, simply run:

.. code-block:: bash

    $ datalad push  --to osf-export-storage
      copy(ok): .datalad/.gitattributes
      copy(ok): .datalad/config
      copy(ok): .gitattributes
      copy(ok): books/bash_guide.pdf
      copy(ok): code/example.txt
      action summary:
         copy (ok: 5)

The resulting project has a human readable structure, and all its data can be viewed and downloaded via the OSF interface.
It is not possible to clone this dataset with DataLad, however potential users can still download it from the standard OSF interface.

.. image:: ../_static/public_exportonly_sibling.png


