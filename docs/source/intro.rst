Introduction
------------

Goal of the extension
^^^^^^^^^^^^^^^^^^^^^

This extension aims to allow DataLad to work with the Open Science Framework (OSF). This is done by transforming storage on the Open Science Framework (OSF) into a `git-annex <https://git-annex.branchable.com/>`_  repository.

What can I use this extension for?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can use this extension to use the OSF as a special remote to store data in the annex  of a dataset. With this, you can `datalad publish` a dataset to GitHub or similar services and the data to the OSF (via a publication dependency).
The extension is most beneficial for easy access to data stored on OSF via GitHub. If you are sharing your dataset via OSF and code via GitHub, this will allow smooth integration of both along with unified version management provided by DataLad.

What can I **not** use this extension for?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This tool does not work for data that is stored in a storage service other than OSF.
Please refer to the `list of special remotes <https://git-annex.branchable.com/special_remotes/>`_ as hosted by the git-annex website for other storage services.
