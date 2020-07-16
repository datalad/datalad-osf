.. include:: ../links.inc
.. _osfsibling:

Step 2: Create an OSF sibling
=============================

Once authenticated, DataLad can -- if called from within a DataLad dataset -- create and modify projects on the OSF and publish annexed data, a single version view, or the complete dataset to it.
The command that enables this is :command:`datalad create-sibling-osf`.
It supports different modes, exposes a large number of features from the OSF web interface and yields a custom dataset configuration for your use case at hand.
This section introduces the command and its functionality, and the upcoming use cases demonstrate several workflow types it can be used for.

What's a sibling?
^^^^^^^^^^^^^^^^^

A sibling is a dataset clone that a given DataLad dataset knows about.
In most cases, changes can be retrieved and pushed between a dataset and its sibling.
It is the equivalent of a *remote* in Git.
The :command:`datalad create-sibling-osf` command can create a dataset clone under an authenticated user account on the OSF as a new project.

General command
^^^^^^^^^^^^^^^

When relying on default parameters, ``create-sibling-osf`` requires only a project name for the resulting OSF project (``--title``) and a sibling name (``-s/--name``, which defaults to ``osf``).

.. code-block:: bash

   # within a dataset mydataset
   $ datalad create-sibling-osf --title <my-new-osf-project-title> -s <my-sibling-name>
   create-sibling-osf(ok): https://osf.io/czgpf/
   [INFO   ] Configure additional publication dependency on "<my-sibling-name>-storage"
   configure-sibling(ok): <path/to/mydataset> (sibling)

In the default modes of operation and in most other modes, this command will create one project on the OSF (reported under its URL in the command summary) and two dataset siblings: One sibling to publish Git history and files stored in Git to, and a *storage* sibling to which annexed data will be published.


.. admonition:: dataset publishing

   Note that data still needs to be *published* to be available on the OSF after sibling creation.
   The relevant commands for this are dependent of the sibling *mode*.
   If used in the default mode, both siblings will be automatically configured such that a single ``datalad push`` is sufficient to publish the complete dataset.
   For general information on publishing datasets, please refer to `this Handbook chapter <http://handbook.datalad.org/en/latest/basics/101-141-push.html>`_, and for more information on publishing depending on sibling mode, please pay close attention to the paragraph :ref:`siblingmode` and the upcoming use cases.

Sibling configuration
^^^^^^^^^^^^^^^^^^^^^

``create-sibling-osf`` has a number of parameters that expose the underlying flexibility of DataLad, git-annex, and the OSF.
The most important one is the *mode* (``--mode``) parameter.
Depending on the mode for your OSF sibling, you will be able to publish different aspects of your dataset to the OSF, and each mode requires different commands for publishing.
Other important parameters include the ``--public`` flag (for access control), and ``--tag``, ``--category`` and ``--description`` for additional project meta data.
For a complete overview of all parameters, see the :ref:`command documentation <cmd>`.

.. _siblingmode:

Sibling modes
"""""""""""""

``create-sibling-osf`` supports several modes that determine the functionality and usage of the resulting sibling.

- ``annex`` (default): **You can publish the complete dataset to the resulting OSF project**. This includes all Git history and annexed data. Afterwards, the OSF project URL can be cloned to retrieve the dataset, and ``datalad get`` will be able retrieve all file contents, even older versions. This mode is the most convenient if you aim to share complete datasets with all data and version history. Note that the dataset representation in the OSF project is not as readable as in a local dataset (clone), but a non-human readable representation [#f1]_ tuned to enable cloning. Publishing the dataset requires only ``datalad push``.
- ``export``: **You can push the Git history of a dataset as well as one snapshot of its data to the resulting OSF project**. Afterwards, the OSF project URL can be cloned to retrieve the dataset and ``datalad get`` will be able to retrieve all file contents *in one version*. Compared to the ``annex`` mode, the dataset representation on the OSF is human-readable, but only one version of each file can be published. This mode is convenient if you want to share a dataset and its history in a human-readable way but only make one version of it available. Publishing Git history requires ``git push`` or ``datalad push``, and exporting a single view of the data must be done via ``git-annex export``.
- ``gitonly``: **You can push the Git history of a dataset, but no annexed data to the resulting OSF project**.  Afterwards, the OSF project URL can be cloned to retrieve the dataset, but ``datalad get`` will not be able to retrieve file contents. This can be convenient if you want to use the OSF as an alternative to GitHub_. Note that the representation of the dataset is not human-readable, but tuned for cloning.  Publishing Git history requires ``git push`` or ``datalad push``.
- ``exportonly``: **You can export the dataset in a human-readable way in one version**. Note that this type of sibling can not be cloned from the OSF. This option is the most convenient if you want to make one snapshot of your dataset available via the OSF. Exporting needs to be done via ``git-annex export`` and your dataset will only get a storage sibling.


In deciding which mode suits your use case you can consider the following questions:

#. Do you want collaborators to be able to ``datalad clone`` your project? If yes, go for ``annex``, ``export``, or ``gitonly``
#. Do you want to share your data? If yes, go for ``annex``, or -- if you're okay with sharing only a one version per file -- ``export`` and ``export only``
#. Do you care how data looks like on the OSF? If not, go for ``annex``, if yes, use one of the ``export`` modes. Find out more about this in the :ref:`tutorial on exporting data <export>`.




Access Management: Public or private projects
"""""""""""""""""""""""""""""""""""""""""""""

By default, any new project created with ``create-sibling-osf`` is a `private OSF project <https://help.osf.io/hc/en-us/articles/360019737894-FAQs#what-if-i-don-t-want-to-make-anything-available-publicly-in-the-osf>`_ that can only be accessed by its creator and collaborators added via OSF's interface.
To make a project public, you can either transform it into a public project via the web interface, or use the ``--public`` flag of ``create-sibling-osf`` to create it publicly from the very start.
This constitutes a convenient access management system for your dataset.

OSF project metadata
""""""""""""""""""""

Meta data helps to make your project discoverable and understandable.
The OSF provides several means of attaching meta data to a project: Tags and Categories.
By default, two tags are created upon project creation: "DataLad dataset" and the unique ID of your dataset.
Any amount of arbitrary additional tags can be specified with one or more ``--tag`` options.
Note that each tag needs to be specified with its own ``--tag`` parameter.

The category of a project determines the small icon displayed in a project and helps search organization.
You can chose one out of several categories ("analysis", "communication", "data", "hypothesis",
"instrumentation", "methods and measures", "procedure", "project", "software", "other") and specify it using the ``--category`` parameter.
By default, the category "data" is used.


.. rubric:: Footnotes

.. [#f1] What exactly is a non-human readable representation? On the OSF, the Git history will be compressed to a text file and a zip file, while all annexed data will appear under the hash it is stored in in the git-annex object tree, i.e., with an obscured file name. If you are interested in finding out more about this, take a look at `this section in the DataLad handbook <http://handbook.datalad.org/en/latest/basics/101-115-symlinks.html>`_. Once cloned from the OSF to a local file system, the dataset will have its usual, human-readable format.