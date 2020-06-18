Use cases
*********

Use Case 1: Collaborating on OSF
================================

Imagine you are a PhD student and want to collaborate on a fun little side 
project with a student at another institute. It is quite obvious for the two of
you that your code will be hosted on Github_. And you also know enough about 
DataLad, that using it for the whole project will be really beneficial.

But what about the data you are collecting? 
The Dropbox is already full (`DataLad third party providers <http://handbook.datalad.org/en/latest/basics/101-138-sharethirdparty.html>`_). And Amazon services don't seem to be
your best alternative.
Suddenly you remember, that you got an OSF_ account recently, and that there is
`this <https://github.com/datalad/datalad-osf/>`_ nice DataLad extension 
set up a SpecialRemote on OSF_.

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

And we also want to add a text file, which will be saved on Github_.

.. code-block:: bash

    $ mkdir code
    $ cat << EOT > example.txt
    This is just an example file just to show the different ways of saving data 
    in a DataLad Dataset.
    $ datalad save --to-git -m "created an example.txt"

We now have a Dataset with one file that can be worked on using Github and one 
that should be tracked using `git-annex`. 

Setting up Github Remote
^^^^^^^^^^^^^^^^^^^^^^^^
We can set-up a Github Remote with the same name basically using 
TODO: this uses publish, but 

.. code-block:: bash

    datalad create-sibling-github REPRONAME --github-login GITHUB_NAME
    git annex copy code/ --to github

Setting up the OSF Remote
^^^^^^^^^^^^^^^^^^^^^^^^^

To use OSF as a storage, you need to provide either your OSF credentials or an OSF access token.
You can create such a token in your account settings, make sure to create a `full_write` token to be able to create OSF projects and upload data to OSF. 

.. code-block:: bash

    export OSF_TOKEN=YOUR_TOKEN_FROM_OSF.IO

We are now going to use datalad to create a sibling dataset on OSF - this will create a new dataset called `OSF_PROJECT_NAME` on the OSF account associated with the OSF token in `$OSF_TOKEN`.

.. code-block:: bash

    datalad create-sibling-osf OSF_PROJECT_NAME YOUR_OSF_REMOTE_NAME

And finally we are going to copy all files to this new OSF project.
.. code-block:: bash

    git annex copy books/* --to YOUR_OSF_REMOTE_NAME


.. _OSF: https://www.osf.io/
.. _Github: https://www.github.com/
