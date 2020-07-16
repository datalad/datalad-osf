.. include:: ./links.inc
.. _intro:

Introduction
============

The Open Science Framework
--------------------------

The Open Science Framework (OSF_), developed and maintained by the Center for Open Science (COS), is a tool that promotes open, centralized workflows by enabling capture of different aspects and products of the research life-cycle, including developing a research idea, designing a study, storing and analyzing collected data, and writing and publishing reports or papers.
In the scientific community, it is commonly used for registered reports, as a preprint server, and for study archival and data sharing.
In order to use the OSF, a free registration is required.

The core functionality of the OSF_ is its ability to create and develop *projects*, with a project being a private or public workspace for collaboration, data sharing, or data archival.
Projects have an associate storage (either via OSF storage or third party providers) for (large) data, and can have *components*, associated sub-projects.
Each OSF user, project, component, and file is given a unique, persistent uniform resource locator (URL) to enable sharing and promote attribution.
Projects can also be assigned digital object identifiers (DOIs) and archival resource keys (ARKs) if they are made publicly available.

At the moment, a the OSF storage provides virtually unlimited storage capacity.
As long as individual files are smaller than 5GB, any amount of data can be uploaded to the OSF.
This makes the OSF_ a powerful, accessible, and free data sharing and collaboration platform for researchers.


Goal of the extension
---------------------

This extension allows DataLad_ to work with the Open Science Framework (OSF_) to make sharing and collaboration on data or DataLad datasets even easier.
It comes with several features that enable the following main use cases:

#. Export existing datasets to the OSF
#. Clone published datasets from the OSF
#. Utilize OSF projects as a third party storage provider for annexed data
#. Export single-view snapshots of datasets to an OSF project

To enable these use cases, a dataset is published as an OSF project, and its OSF storage is used as a `git-annex`_ `special remote`_ to publish (large) file contents.
Major OSF flexibility is exposed to control whether the resulting project is private (default) or public, and to attach meaningful metadata to it.
You can find out demonstrations of these use cases in the :ref:`Tutorial`.

What can I use this extension for?
----------------------------------

You can use this extension to publish, store, collaborate on, or share your dataset (data) via the OSF_.
Here is some inspiration on what you could do:

- Publish your study (including its version history, data, code, results, and provenance) as a DataLad dataset to the OSF.
  Share the project's OSF URL with colleagues and collaborators to give them easy access to your work with a single ``datalad clone``.
- Clone a friend's dataset -- from the OSF!
- Use the OSF as a `special remote`_ to store data in the annex of your dataset.
  With this, you can publish a dataset to `GitHub`_ or similar Git repository hosting services, and have your data published to the OSF (via a publication dependency).
  Your dataset will be exposed and available on GitHub, while data is stored on and retrieved from the OSF.
- Take a version snapshot of all of your dataset's files and export them to the OSF.
  This publishes one version of your project in a human-readable fashion to the OSF to make it available to the outside world.

``datalad-osf`` comes with a range of hidden convenience functions for OSF interactions.
Importantly, you will not need to create OSF projects via the OSF web interface -- given appropriate credentials, ``datalad create-sibling-osf`` will create new projects under your user account and report back the generated URL.


What can I **not** use this extension for?
------------------------------------------

- This tool does not work for data that is stored in a storage service other than the OSF_, and within the OSF, only OSF storage, no other third party storage, is supported.
  Please refer to the list of `special remotes`_ as hosted by the `git-annex`_ website for other storage services and how to use them with DataLad.
- Also, be mindful that OSF storage imposes a maximum file size of 5GB.
  Individual files larger than 5GB can not be published with this extension.
- Finally, the starting point for working with this extension is a (published) DataLad dataset, not a regular OSF project.
  This extension will not transform normal OSF projects into datasets, but expose DataLad datasets as OSF projects.