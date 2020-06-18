Introduction
------------


Goal of the extension
^^^^^^^^^^^^^^^^^^^^^

This extension aims to allow DataLad to work with the Open Science Framework (OSF). This is done by creating a `git-annex <https://git-annex.branchable.com/>`_ `special remote <https://git-annex.branchable.com/special_remotes/>`_ that can transform datasets on the OSF into git-annex repositories and vice versa. Files in OSF storage could thus be consumed or exported fast and easily via git-annex or DataLad, and published to repository-hosting services (GitHub, GitLab, Bitbucket, ...) as lightweight repositories that constitute an alternative access to the data stored on the OSF - that is: you can git clone a repository from for example GitHub and get the data from the OSF from the command line or in your scripts.

What can I use this extension for?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The extension is most beneficial for easy access to data stored on OSF via Github. If you are sharing your dataset via OSF and code via Github, this will allow smooth integration of both along with unified version management provided by DataLad.

What can I **not** use this extension for?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This tool does not work for data that is stored in a storage service other than OSF. Please refer `here <https://git-annex.branchable.com/special_remotes/>`_ for a list of supported data storage services via git-annex special remote framework.