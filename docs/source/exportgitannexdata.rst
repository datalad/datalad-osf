Export a version-controlled dataset to OSF
******************************************

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

In this scenario, you are sharing your dataset via OSF in a version controlled form, that is, how git-annex represents the dataset. This means that your dataset on OSF will not be human-readable, but all different versions of the data will be stored in this way.

Walk through
------------

Installation
^^^^^^^^^^^^
For installation checkout the installation page of the documentation.  

.. toctree::

    settingup.rst


Creating an Example Dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^

As a first step you will want to set up a DataLad Dataset. To do this, run:

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

And we also want to add a text file, which will be saved on Github_. 

.. code-block:: bash

    $ cat << EOT > example.txt
    This is just an example file just to show the different ways of saving data 
    in a DataLad Dataset. EOT

    $ datalad save --to-git -m "created an example.txt"

We now have a Dataset with one file that can be worked on using Git and one 
that should be tracked using `git-annex`.

Setting up the OSF Remote
^^^^^^^^^^^^^^^^^^^^^^^^^^
We can set-up an OSF Remote with the same name basically using 

.. code-block:: bash

    export OSF_TOKEN=YOUR_TOKEN_FROM_OSF.IO

Copying the git-annex dataset to OSF

.. code-block:: bash

datalad create-sibling-osf OSF_PROJECT_NAME YOUR_OSF_REMOTE_NAME
git annex copy . --to YOUR_OSF_REMOTE_NAME


.. _OSF: https://www.osf.io/
.. _Github: https://www.github.com/
