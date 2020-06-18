Export version-controlled data to OSF and code to Github
********************************************************

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

    $ cat << EOT > example.txt
    This is just an example file just to show the different ways of saving data 
    in a DataLad Dataset. EOT

    $ datalad save --to-git -m "created an example.txt"

We now have a Dataset with one file that can be worked on using Github and one 
that should be tracked using `git-annex`. 

Setting up Github Remote
^^^^^^^^^^^^^^^^^^^^^^^^
We can set-up a Github Remote with the same name basically using 

.. code-block:: bash

    datalad create-sibling-github REPRONAME --github-login GITHUB_NAME --github-passwd PASSWORD
    datalad publish --to github


.. _OSF: https://www.osf.io/
.. _Github: https://www.github.com/
